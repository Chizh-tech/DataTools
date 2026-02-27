"""Plot generator module – creates common chart types from a DataFrame."""

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")  # non-interactive backend, safe for Streamlit / tests


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
) -> plt.Figure:
    """Create a bar chart.

    Args:
        df: Source data.
        x: Column name to use for the x-axis (categories).
        y: Column name to use for bar heights.
        title: Optional chart title.
        xlabel: Optional x-axis label.
        ylabel: Optional y-axis label.

    Returns:
        A :class:`matplotlib.figure.Figure`.
    """
    fig, ax = plt.subplots()
    ax.bar(df[x].astype(str), df[y])
    ax.set_title(title or f"{y} by {x}")
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.tight_layout()
    return fig


def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
) -> plt.Figure:
    """Create a line chart.

    Args:
        df: Source data.
        x: Column name for the x-axis.
        y: Column name for the y-axis (line values).
        title: Optional chart title.
        xlabel: Optional x-axis label.
        ylabel: Optional y-axis label.

    Returns:
        A :class:`matplotlib.figure.Figure`.
    """
    fig, ax = plt.subplots()
    ax.plot(df[x], df[y], marker="o")
    ax.set_title(title or f"{y} over {x}")
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.tight_layout()
    return fig


def scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
) -> plt.Figure:
    """Create a scatter plot.

    Args:
        df: Source data.
        x: Column name for the x-axis.
        y: Column name for the y-axis.
        title: Optional chart title.
        xlabel: Optional x-axis label.
        ylabel: Optional y-axis label.

    Returns:
        A :class:`matplotlib.figure.Figure`.
    """
    fig, ax = plt.subplots()
    ax.scatter(df[x], df[y], alpha=0.6)
    ax.set_title(title or f"{y} vs {x}")
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.tight_layout()
    return fig


def histogram(
    df: pd.DataFrame,
    column: str,
    bins: int = 20,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "Frequency",
) -> plt.Figure:
    """Create a histogram.

    Args:
        df: Source data.
        column: Column name to plot as a histogram.
        bins: Number of histogram bins.
        title: Optional chart title.
        xlabel: Optional x-axis label.
        ylabel: Optional y-axis label.

    Returns:
        A :class:`matplotlib.figure.Figure`.
    """
    fig, ax = plt.subplots()
    ax.hist(df[column].dropna(), bins=bins, edgecolor="black")
    ax.set_title(title or f"Histogram of {column}")
    ax.set_xlabel(xlabel or column)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    return fig
