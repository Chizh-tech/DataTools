"""Unit tests for the plot_generator module."""

import pandas as pd
import pytest
import matplotlib.pyplot as plt

from src.plot_generator import bar_chart, histogram, line_chart, scatter_chart


@pytest.fixture()
def sample_df():
    return pd.DataFrame(
        {
            "category": ["A", "B", "C", "D"],
            "value": [10, 25, 15, 30],
            "x": [1, 2, 3, 4],
            "y": [4, 3, 2, 1],
        }
    )


class TestBarChart:
    def test_returns_figure(self, sample_df):
        fig = bar_chart(sample_df, x="category", y="value")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_custom_title(self, sample_df):
        fig = bar_chart(sample_df, x="category", y="value", title="My Chart")
        ax = fig.axes[0]
        assert ax.get_title() == "My Chart"
        plt.close(fig)

    def test_default_title(self, sample_df):
        fig = bar_chart(sample_df, x="category", y="value")
        ax = fig.axes[0]
        assert "value" in ax.get_title() and "category" in ax.get_title()
        plt.close(fig)


class TestLineChart:
    def test_returns_figure(self, sample_df):
        fig = line_chart(sample_df, x="x", y="value")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_has_one_line(self, sample_df):
        fig = line_chart(sample_df, x="x", y="value")
        ax = fig.axes[0]
        assert len(ax.lines) == 1
        plt.close(fig)


class TestScatterChart:
    def test_returns_figure(self, sample_df):
        fig = scatter_chart(sample_df, x="x", y="y")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_has_scatter_collection(self, sample_df):
        fig = scatter_chart(sample_df, x="x", y="y")
        ax = fig.axes[0]
        assert len(ax.collections) > 0
        plt.close(fig)


class TestHistogram:
    def test_returns_figure(self, sample_df):
        fig = histogram(sample_df, column="value")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_custom_bins(self, sample_df):
        fig = histogram(sample_df, column="value", bins=5)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_default_title_contains_column(self, sample_df):
        fig = histogram(sample_df, column="value")
        ax = fig.axes[0]
        assert "value" in ax.get_title()
        plt.close(fig)
