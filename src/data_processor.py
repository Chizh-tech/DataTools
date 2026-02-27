"""Data processor module for CSV and Excel file parsing."""

from typing import Optional

import pandas as pd


def load_csv(source) -> pd.DataFrame:
    """Load a CSV file from a file path or file-like object and return a DataFrame.

    Args:
        source: A file path string or a file-like object (e.g. ``io.BytesIO``).

    Returns:
        A :class:`pandas.DataFrame` with the parsed data.

    Raises:
        ValueError: If the source cannot be read as a CSV.
    """
    try:
        return pd.read_csv(source)
    except Exception as exc:
        raise ValueError(f"Failed to read CSV: {exc}") from exc


def load_excel(source, sheet_name: Optional[str] = 0) -> pd.DataFrame:
    """Load an Excel file from a file path or file-like object and return a DataFrame.

    Args:
        source: A file path string or a file-like object (e.g. ``io.BytesIO``).
        sheet_name: Optional sheet name to read.  If *0* (the default) the first sheet is used.

    Returns:
        A :class:`pandas.DataFrame` with the parsed data.

    Raises:
        ValueError: If the source cannot be read as an Excel file.
    """
    try:
        return pd.read_excel(source, sheet_name=sheet_name)
    except Exception as exc:
        raise ValueError(f"Failed to read Excel: {exc}") from exc


def get_summary(df: pd.DataFrame) -> dict:
    """Return a summary dictionary for a DataFrame.

    The summary contains:
    - ``shape``: tuple ``(rows, columns)``
    - ``columns``: list of column names
    - ``dtypes``: mapping of column → dtype string
    - ``missing``: mapping of column → count of missing values
    - ``describe``: the result of ``df.describe(include='all')`` as a dict

    Args:
        df: The DataFrame to summarise.

    Returns:
        A dictionary with summary information.
    """
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing": df.isnull().sum().to_dict(),
        "describe": df.describe(include="all").to_dict(),
    }
