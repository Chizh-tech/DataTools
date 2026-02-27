"""AI evaluator module – statistical analysis and optional OpenAI integration."""

import os
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
from scipy import stats

try:
    from openai import OpenAI
except ImportError:  # openai not installed; will raise at call time
    OpenAI = None  # type: ignore[assignment,misc]


def compute_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute descriptive statistics for all numeric columns in a DataFrame.

    For each numeric column the following metrics are computed:

    - ``mean``
    - ``median``
    - ``std`` – standard deviation
    - ``min`` / ``max``
    - ``skewness``
    - ``kurtosis``

    Args:
        df: Source data.

    Returns:
        A nested dictionary ``{column_name: {metric: value, ...}, ...}``.
    """
    result: Dict[str, Any] = {}
    numeric_df = df.select_dtypes(include="number")

    for col in numeric_df.columns:
        series = numeric_df[col].dropna()
        result[col] = {
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std": float(series.std()),
            "min": float(series.min()),
            "max": float(series.max()),
            "skewness": float(stats.skew(series)),
            "kurtosis": float(stats.kurtosis(series)),
        }

    return result


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Return the Pearson correlation matrix for all numeric columns.

    Args:
        df: Source data.

    Returns:
        A :class:`pandas.DataFrame` with the correlation coefficients.
    """
    return df.select_dtypes(include="number").corr()


def ask_openai(prompt: str, api_key: Optional[str] = None, model: str = "gpt-4o-mini") -> str:
    """Send a prompt to the OpenAI Chat Completions API and return the reply.

    The API key is resolved in order:

    1. The *api_key* argument.
    2. The ``OPENAI_API_KEY`` environment variable.

    Args:
        prompt: The user message to send.
        api_key: Optional OpenAI API key.  Falls back to the environment
            variable ``OPENAI_API_KEY`` when not provided.
        model: The OpenAI model to use (default ``"gpt-4o-mini"``).

    Returns:
        The assistant's reply as a plain string.

    Raises:
        ValueError: If no API key is available.
        RuntimeError: If the OpenAI call fails.
    """
    resolved_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not resolved_key:
        raise ValueError(
            "No OpenAI API key provided.  Pass api_key= or set the "
            "OPENAI_API_KEY environment variable."
        )

    try:
        if OpenAI is None:
            raise ImportError("openai package is not installed")
        client = OpenAI(api_key=resolved_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or ""
    except Exception as exc:
        raise RuntimeError(f"OpenAI API call failed: {exc}") from exc
