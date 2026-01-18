"""Command-line interface for pycole."""

import sys
from pathlib import Path

import click

from .analyzer import analyze_path


@click.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
def main(path: Path):
    """
    Analyze Python code metrics for a file or directory.

    PATH: Path to a Python file or directory to analyze
    """
    try:
        metrics = analyze_path(path)

        click.echo(f"\n{'=' * 60}")
        click.echo(f"Python Code Analysis: {path}")
        click.echo(f"{'=' * 60}\n")

        click.echo(f"Total lines of code:                    {metrics.total_lines:>10,}")
        click.echo(f"Lines without comments/blanks:          {metrics.code_lines:>10,} (excl. tests)")
        click.echo(f"Number of statements:                   {metrics.statements:>10,} (excl. tests)")
        click.echo(f"Total lines of test code:               {metrics.test_lines:>10,}")
        click.echo(f"Test lines without comments/blanks:     {metrics.test_code_lines:>10,}")
        click.echo(f"\n{'=' * 60}\n")

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
