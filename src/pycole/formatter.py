"""Formatting utilities for pycole metrics output."""

from pathlib import Path


def format_metrics_output(path: Path, metrics, output_format: str = "text") -> str:
    """
    Format metrics into a readable string output.

    Args:
        path: Path that was analyzed
        metrics: Metrics object containing analysis results
        output_format: Output format ('text' or 'csv')

    Returns:
        Formatted string with metrics
    """
    if output_format == "csv":
        return format_metrics_csv(path, metrics)

    lines = [
        f"\n{'=' * 60}",
        f"Python Code Analysis: {path}",
        f"{'=' * 60}\n",
        "",
        f"Total lines of code:                    {metrics.total_lines:>10,}",
        f"Lines without comments/blanks:          {metrics.code_lines:>10,} (excl. tests)",
        f"Number of statements:                   {metrics.statements:>10,} (excl. tests)",
        f"Total lines of test code:               {metrics.test_lines:>10,}",
        f"Test lines without comments/blanks:     {metrics.test_code_lines:>10,}",
        f"\n{'=' * 60}\n",
    ]
    return "\n".join(lines)


def format_metrics_csv(path: Path, metrics) -> str:
    """
    Format metrics as CSV output.

    Args:
        path: Path that was analyzed
        metrics: Metrics object containing analysis results

    Returns:
        CSV formatted string with metrics
    """
    header = "path,total_lines,code_lines,statements,test_lines,test_code_lines"
    data = f"{path},{metrics.total_lines},{metrics.code_lines},{metrics.statements},{metrics.test_lines},{metrics.test_code_lines}"
    return f"{header}\n{data}"
