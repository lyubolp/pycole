"""Command-line interface for pycole."""

import sys
from pathlib import Path

import click

from .analyzer import analyze_path
from .formatter import format_metrics_output


@click.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["text", "csv"], case_sensitive=False),
    default="text",
    help="Output format (text or csv)",
)
def main(path: Path, output_format: str):
    """
    Analyze Python code metrics for a file or directory.

    PATH: Path to a Python file or directory to analyze
    """
    try:
        metrics = analyze_path(path)
        output = format_metrics_output(path, metrics, output_format)
        click.echo(output)

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
