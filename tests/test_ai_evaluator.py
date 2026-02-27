"""Unit tests for the ai_evaluator module."""

import unittest.mock as mock

import pandas as pd
import pytest

from src.ai_evaluator import ask_openai, compute_statistics, correlation_matrix


@pytest.fixture()
def numeric_df():
    return pd.DataFrame(
        {
            "a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "b": [5.0, 4.0, 3.0, 2.0, 1.0],
            "c": [2.0, 2.0, 2.0, 2.0, 2.0],
        }
    )


@pytest.fixture()
def mixed_df(numeric_df):
    df = numeric_df.copy()
    df["text"] = ["x", "y", "z", "w", "v"]
    return df


# ---------------------------------------------------------------------------
# compute_statistics
# ---------------------------------------------------------------------------

class TestComputeStatistics:
    def test_returns_dict(self, numeric_df):
        result = compute_statistics(numeric_df)
        assert isinstance(result, dict)

    def test_only_numeric_columns(self, mixed_df):
        result = compute_statistics(mixed_df)
        assert "text" not in result
        assert "a" in result

    def test_expected_keys(self, numeric_df):
        result = compute_statistics(numeric_df)
        for col in ["a", "b", "c"]:
            assert set(result[col].keys()) == {
                "mean", "median", "std", "min", "max", "skewness", "kurtosis"
            }

    def test_mean_value(self, numeric_df):
        result = compute_statistics(numeric_df)
        assert result["a"]["mean"] == pytest.approx(3.0)

    def test_empty_df_returns_empty(self):
        result = compute_statistics(pd.DataFrame())
        assert result == {}

    def test_no_numeric_columns_returns_empty(self):
        df = pd.DataFrame({"text": ["a", "b", "c"]})
        result = compute_statistics(df)
        assert result == {}


# ---------------------------------------------------------------------------
# correlation_matrix
# ---------------------------------------------------------------------------

class TestCorrelationMatrix:
    def test_returns_dataframe(self, numeric_df):
        corr = correlation_matrix(numeric_df)
        assert isinstance(corr, pd.DataFrame)

    def test_shape(self, numeric_df):
        corr = correlation_matrix(numeric_df)
        assert corr.shape == (3, 3)

    def test_diagonal_is_one(self, numeric_df):
        corr = correlation_matrix(numeric_df)
        for col in corr.columns:
            val = corr.loc[col, col]
            # constant columns produce NaN correlation; skip them
            if not pd.isna(val):
                assert val == pytest.approx(1.0)

    def test_perfect_negative_correlation(self, numeric_df):
        corr = correlation_matrix(numeric_df)
        assert corr.loc["a", "b"] == pytest.approx(-1.0)

    def test_ignores_non_numeric(self, mixed_df):
        corr = correlation_matrix(mixed_df)
        assert "text" not in corr.columns


# ---------------------------------------------------------------------------
# ask_openai
# ---------------------------------------------------------------------------

class TestAskOpenai:
    def test_raises_without_key(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="No OpenAI API key"):
            ask_openai("hello", api_key=None)

    def test_uses_env_var(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        fake_response = mock.MagicMock()
        fake_response.choices[0].message.content = "Hello!"

        with mock.patch("src.ai_evaluator.OpenAI") as mock_client_cls:
            mock_instance = mock_client_cls.return_value
            mock_instance.chat.completions.create.return_value = fake_response
            result = ask_openai("hi")

        assert result == "Hello!"

    def test_uses_provided_key(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        fake_response = mock.MagicMock()
        fake_response.choices[0].message.content = "World!"

        with mock.patch("src.ai_evaluator.OpenAI") as mock_client_cls:
            mock_instance = mock_client_cls.return_value
            mock_instance.chat.completions.create.return_value = fake_response
            result = ask_openai("hi", api_key="explicit-key")

        assert result == "World!"

    def test_raises_runtime_error_on_api_failure(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        with mock.patch("src.ai_evaluator.OpenAI") as mock_client_cls:
            mock_instance = mock_client_cls.return_value
            mock_instance.chat.completions.create.side_effect = Exception("API down")
            with pytest.raises(RuntimeError, match="OpenAI API call failed"):
                ask_openai("hi")
