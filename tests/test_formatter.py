"""Tests for the formatter module."""

from pathlib import Path
from dataclasses import dataclass

import pytest

from pycole.formatter import format_metrics_output, format_metrics_csv


@dataclass
class MockMetrics:
    """Mock metrics object for testing."""

    total_lines: int
    code_lines: int
    statements: int
    test_lines: int
    test_code_lines: int


class TestFormatMetricsOutput:
    """Tests for format_metrics_output function."""

    def test_format_text_output(self):
        """Test text format output."""
        path = Path("/test/path/project")
        metrics = MockMetrics(total_lines=1000, code_lines=800, statements=250, test_lines=200, test_code_lines=150)

        result = format_metrics_output(path, metrics, "text")

        assert "Python Code Analysis: /test/path/project" in result
        assert "Total lines of code:                         1,000" in result
        assert "Lines without comments/blanks:                 800" in result
        assert "Number of statements:                          250" in result
        assert "Total lines of test code:                      200" in result
        assert "Test lines without comments/blanks:            150" in result
        assert "=" * 60 in result

    def test_format_text_output_default(self):
        """Test that text format is the default."""
        path = Path("/test/path")
        metrics = MockMetrics(100, 80, 25, 20, 15)

        result_default = format_metrics_output(path, metrics)
        result_explicit = format_metrics_output(path, metrics, "text")

        assert result_default == result_explicit

    def test_format_csv_output(self):
        """Test CSV format output."""
        path = Path("/test/path/project")
        metrics = MockMetrics(total_lines=1000, code_lines=800, statements=250, test_lines=200, test_code_lines=150)

        result = format_metrics_output(path, metrics, "csv")

        lines = result.strip().split("\n")
        assert len(lines) == 2
        assert lines[0] == "path,total_lines,code_lines,statements,test_lines,test_code_lines"
        assert lines[1] == "/test/path/project,1000,800,250,200,150"

    def test_format_with_zero_values(self):
        """Test formatting with zero values."""
        path = Path("/empty/project")
        metrics = MockMetrics(0, 0, 0, 0, 0)

        result_text = format_metrics_output(path, metrics, "text")
        assert "0" in result_text

        result_csv = format_metrics_output(path, metrics, "csv")
        assert "0,0,0,0,0" in result_csv

    def test_format_with_large_numbers(self):
        """Test formatting with large numbers."""
        path = Path("/large/project")
        metrics = MockMetrics(
            total_lines=1234567, code_lines=987654, statements=123456, test_lines=234567, test_code_lines=198765
        )

        result_text = format_metrics_output(path, metrics, "text")
        # Check that thousands separators are present in text format
        assert "1,234,567" in result_text
        assert "987,654" in result_text

        result_csv = format_metrics_output(path, metrics, "csv")
        # CSV should have raw numbers without separators
        assert "1234567,987654,123456,234567,198765" in result_csv


class TestFormatMetricsCsv:
    """Tests for format_metrics_csv function."""

    def test_csv_header(self):
        """Test that CSV output has correct header."""
        path = Path("/test")
        metrics = MockMetrics(100, 80, 25, 20, 15)

        result = format_metrics_csv(path, metrics)

        lines = result.strip().split("\n")
        assert lines[0] == "path,total_lines,code_lines,statements,test_lines,test_code_lines"

    def test_csv_data_row(self):
        """Test that CSV output has correct data row."""
        path = Path("/my/project")
        metrics = MockMetrics(500, 400, 120, 100, 80)

        result = format_metrics_csv(path, metrics)

        lines = result.strip().split("\n")
        assert lines[1] == "/my/project,500,400,120,100,80"

    def test_csv_with_relative_path(self):
        """Test CSV output with relative path."""
        path = Path("src/module")
        metrics = MockMetrics(200, 150, 50, 50, 40)

        result = format_metrics_csv(path, metrics)

        assert "src/module,200,150,50,50,40" in result

    def test_csv_single_file(self):
        """Test CSV output for a single file."""
        path = Path("main.py")
        metrics = MockMetrics(50, 40, 15, 0, 0)

        result = format_metrics_csv(path, metrics)

        lines = result.strip().split("\n")
        assert len(lines) == 2
        assert "main.py,50,40,15,0,0" in result
