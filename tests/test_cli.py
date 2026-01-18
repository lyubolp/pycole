"""Tests for the pycole CLI module."""

import tempfile
from pathlib import Path

from click.testing import CliRunner

from pycole.cli import main


def test_cli_analyze_file_text_format():
    """Test CLI with a single file and text format."""
    runner = CliRunner()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(
            """# Comment
def hello():
    return 'world'
"""
        )
        filepath = Path(f.name)

    try:
        result = runner.invoke(main, [str(filepath)])
        assert result.exit_code == 0
        assert "Total lines of code:" in result.output
        assert "Lines without comments/blanks:" in result.output
        assert "Number of statements:" in result.output
    finally:
        filepath.unlink()


def test_cli_analyze_file_csv_format():
    """Test CLI with a single file and CSV format."""
    runner = CliRunner()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(
            """def hello():
    return 'world'
"""
        )
        filepath = Path(f.name)

    try:
        result = runner.invoke(main, [str(filepath), "--format", "csv"])
        assert result.exit_code == 0
        assert "path,total_lines,code_lines,statements,test_lines,test_code_lines" in result.output
        assert str(filepath) in result.output
    finally:
        filepath.unlink()


def test_cli_analyze_directory_text_format():
    """Test CLI with a directory and text format."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        dirpath = Path(tmpdir)
        (dirpath / "module.py").write_text(
            """def func():
    return 42
"""
        )
        (dirpath / "test_module.py").write_text(
            """def test_func():
    assert True
"""
        )

        result = runner.invoke(main, [str(dirpath)])
        assert result.exit_code == 0
        assert "Total lines of code:" in result.output
        assert "Lines without comments/blanks:" in result.output


def test_cli_analyze_directory_csv_format():
    """Test CLI with a directory and CSV format."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        dirpath = Path(tmpdir)
        (dirpath / "module.py").write_text(
            """def func():
    return 42
"""
        )

        result = runner.invoke(main, [str(dirpath), "--format", "csv"])
        assert result.exit_code == 0
        assert "path,total_lines,code_lines,statements,test_lines,test_code_lines" in result.output


def test_cli_invalid_path():
    """Test CLI with a non-existent path."""
    runner = CliRunner()

    result = runner.invoke(main, ["/nonexistent/path/file.py"])
    assert result.exit_code == 2  # Click returns 2 for invalid arguments
    assert "does not exist" in result.output.lower() or "error" in result.output.lower()


def test_cli_value_error_handling():
    """Test CLI handling of ValueError from analyzer."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a special file (not regular file or directory)
        from unittest.mock import patch
        import sys

        # We'll use a temporary file and patch analyze_path to raise ValueError
        dirpath = Path(tmpdir)
        (dirpath / "test.py").write_text("pass")

        with patch("pycole.cli.analyze_path", side_effect=ValueError("Test error")):
            result = runner.invoke(main, [str(dirpath)])
            assert result.exit_code == 1
            assert "Error:" in result.output
            assert "Test error" in result.output


def test_cli_unexpected_error_handling():
    """Test CLI handling of unexpected exceptions."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        dirpath = Path(tmpdir)
        (dirpath / "test.py").write_text("pass")

        from unittest.mock import patch

        with patch("pycole.cli.analyze_path", side_effect=RuntimeError("Unexpected error")):
            result = runner.invoke(main, [str(dirpath)])
            assert result.exit_code == 1
            assert "Unexpected error:" in result.output
            assert "Unexpected error" in result.output


def test_cli_format_option_case_insensitive():
    """Test that format option is case insensitive."""
    runner = CliRunner()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("def hello(): pass")
        filepath = Path(f.name)

    try:
        result = runner.invoke(main, [str(filepath), "--format", "CSV"])
        assert result.exit_code == 0
        assert "path,total_lines,code_lines,statements,test_lines,test_code_lines" in result.output
    finally:
        filepath.unlink()
