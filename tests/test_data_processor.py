"""Unit tests for the data_processor module."""

import io

import pandas as pd
import pytest

from src.data_processor import get_summary, load_csv, load_excel


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SAMPLE_CSV = b"name,age,score\nAlice,30,95.5\nBob,25,88.0\nCarol,35,72.3\n"


def _make_csv_buffer(content: bytes = SAMPLE_CSV) -> io.BytesIO:
    return io.BytesIO(content)


def _make_excel_buffer() -> io.BytesIO:
    buf = io.BytesIO()
    df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25], "score": [95.5, 88.0]})
    df.to_excel(buf, index=False)
    buf.seek(0)
    return buf


# ---------------------------------------------------------------------------
# load_csv
# ---------------------------------------------------------------------------

class TestLoadCsv:
    def test_returns_dataframe(self):
        df = load_csv(_make_csv_buffer())
        assert isinstance(df, pd.DataFrame)

    def test_correct_shape(self):
        df = load_csv(_make_csv_buffer())
        assert df.shape == (3, 3)

    def test_column_names(self):
        df = load_csv(_make_csv_buffer())
        assert list(df.columns) == ["name", "age", "score"]

    def test_values(self):
        df = load_csv(_make_csv_buffer())
        assert df.iloc[0]["name"] == "Alice"
        assert df.iloc[0]["age"] == 30

    def test_invalid_source_raises(self):
        with pytest.raises(ValueError):
            load_csv(None)


# ---------------------------------------------------------------------------
# load_excel
# ---------------------------------------------------------------------------

class TestLoadExcel:
    def test_returns_dataframe(self):
        df = load_excel(_make_excel_buffer())
        assert isinstance(df, pd.DataFrame)

    def test_correct_shape(self):
        df = load_excel(_make_excel_buffer())
        assert df.shape == (2, 3)

    def test_column_names(self):
        df = load_excel(_make_excel_buffer())
        assert list(df.columns) == ["name", "age", "score"]

    def test_invalid_source_raises(self):
        with pytest.raises(ValueError):
            load_excel(None)


# ---------------------------------------------------------------------------
# get_summary
# ---------------------------------------------------------------------------

class TestGetSummary:
    @pytest.fixture()
    def df(self):
        return pd.DataFrame({"a": [1, 2, None], "b": ["x", "y", "z"]})

    def test_shape(self, df):
        summary = get_summary(df)
        assert summary["shape"] == (3, 2)

    def test_columns(self, df):
        summary = get_summary(df)
        assert summary["columns"] == ["a", "b"]

    def test_missing_count(self, df):
        summary = get_summary(df)
        assert summary["missing"]["a"] == 1
        assert summary["missing"]["b"] == 0

    def test_dtypes_are_strings(self, df):
        summary = get_summary(df)
        for dtype_str in summary["dtypes"].values():
            assert isinstance(dtype_str, str)

    def test_describe_keys(self, df):
        summary = get_summary(df)
        assert "a" in summary["describe"]
        assert "b" in summary["describe"]
