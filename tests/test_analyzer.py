"""Tests for the pycole analyzer module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from pycole.analyzer import (
    analyze_file,
    analyze_directory,
    analyze_path,
    is_test_file,
    count_statements,
)


def test_is_test_file():
    """Test identification of test files."""
    assert is_test_file(Path("test_example.py"))
    assert is_test_file(Path("example_test.py"))
    assert is_test_file(Path("tests/example.py"))
    assert is_test_file(Path("test/example.py"))
    assert not is_test_file(Path("example.py"))
    assert not is_test_file(Path("src/module.py"))


def test_count_statements():
    """Test statement counting."""
    code = """
def hello():
    x = 1
    y = 2
    return x + y

if __name__ == '__main__':
    print(hello())
"""
    statements = count_statements(code)
    assert statements > 0  # Should count function def, assignments, return, if, print


def test_analyze_file_simple():
    """Test analyzing a simple Python file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(
            """# This is a comment
def hello():
    return 'world'

# Another comment
x = hello()
"""
        )
        f.flush()
        filepath = Path(f.name)

    try:
        metrics = analyze_file(filepath)
        assert metrics.total_lines == 6
        assert metrics.code_lines == 3  # def, return, x = lines
        assert metrics.statements > 0
        assert metrics.test_lines == 0  # Not a test file
    finally:
        filepath.unlink()


def test_analyze_file_test():
    """Test analyzing a test file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, prefix="test_") as f:
        f.write(
            """def test_example():
    assert True

def test_another():
    x = 1
    assert x == 1
"""
        )
        f.flush()
        filepath = Path(f.name)

    try:
        metrics = analyze_file(filepath)
        assert metrics.total_lines == 6
        assert metrics.test_lines == 6  # Is a test file
        assert metrics.test_code_lines == 5  # Code lines exclude blank line (line 3)
        assert metrics.code_lines == 0  # Test files don't count in main code_lines
        assert metrics.statements == 0  # Test files don't count in main statements
    finally:
        filepath.unlink()


def test_analyze_directory():
    """Test analyzing a directory of Python files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dirpath = Path(tmpdir)

        # Create a regular file
        (dirpath / "module.py").write_text(
            """def func():
    return 42
"""
        )

        # Create a test file
        (dirpath / "test_module.py").write_text(
            """def test_func():
    assert True
"""
        )

        metrics = analyze_directory(dirpath)
        assert metrics.total_lines == 4  # 2 lines each
        assert metrics.code_lines == 2  # Only from non-test file
        assert metrics.test_lines == 2  # Only from test file
        assert metrics.test_code_lines == 2  # Only from test file


def test_analyze_file_with_blank_lines():
    """Test that blank lines are not counted as code lines."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(
            """def hello():
    x = 1

    y = 2

    return x + y
"""
        )
        f.flush()
        filepath = Path(f.name)

    try:
        metrics = analyze_file(filepath)
        assert metrics.total_lines == 6
        assert metrics.code_lines == 4  # def, x=1, y=2, return (blanks excluded)
    finally:
        filepath.unlink()


def test_count_statements_with_syntax_error():
    """Test that count_statements returns 0 for invalid Python code."""
    invalid_code = """
def broken(:
    return x +
"""
    assert count_statements(invalid_code) == 0


def test_analyze_file_unicode_decode_error():
    """Test handling of files that can't be decoded as UTF-8."""
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".py", delete=False) as f:
        # Write invalid UTF-8 bytes
        f.write(b"\xff\xfe\xfd")
        filepath = Path(f.name)

    try:
        metrics = analyze_file(filepath)
        assert metrics.total_lines == 0
        assert metrics.code_lines == 0
        assert metrics.statements == 0
        assert metrics.test_lines == 0
        assert metrics.test_code_lines == 0
    finally:
        filepath.unlink()


def test_analyze_file_permission_error():
    """Test handling of files without read permissions."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("def hello(): pass")
        filepath = Path(f.name)

    try:
        # Mock read_text to raise PermissionError
        with patch.object(Path, "read_text", side_effect=PermissionError("Permission denied")):
            metrics = analyze_file(filepath)
            assert metrics.total_lines == 0
            assert metrics.code_lines == 0
            assert metrics.statements == 0
    finally:
        filepath.unlink()


def test_analyze_directory_skips_venv():
    """Test that virtual environment directories are skipped."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dirpath = Path(tmpdir)

        # Create a regular file
        (dirpath / "module.py").write_text("def func(): return 42")

        # Create files in directories that should be skipped
        venv_dir = dirpath / ".venv" / "lib"
        venv_dir.mkdir(parents=True)
        (venv_dir / "ignored.py").write_text("def ignored(): pass")

        pycache_dir = dirpath / "__pycache__"
        pycache_dir.mkdir()
        (pycache_dir / "cached.py").write_text("def cached(): pass")

        git_dir = dirpath / ".git"
        git_dir.mkdir()
        (git_dir / "config.py").write_text("def config(): pass")

        node_modules_dir = dirpath / "node_modules"
        node_modules_dir.mkdir()
        (node_modules_dir / "package.py").write_text("def package(): pass")

        metrics = analyze_directory(dirpath)
        # Should only count module.py, not the files in ignored directories
        assert metrics.total_lines == 1
        assert metrics.code_lines == 1


def test_analyze_path_with_file():
    """Test analyze_path with a file argument."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("def func(): return 42")
        filepath = Path(f.name)

    try:
        metrics = analyze_path(filepath)
        assert metrics.total_lines == 1
        assert metrics.code_lines == 1
    finally:
        filepath.unlink()


def test_analyze_path_with_directory():
    """Test analyze_path with a directory argument."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dirpath = Path(tmpdir)
        (dirpath / "module.py").write_text("def func(): return 42")

        metrics = analyze_path(dirpath)
        assert metrics.total_lines == 1
        assert metrics.code_lines == 1


def test_analyze_path_with_invalid_path():
    """Test analyze_path with a path that doesn't exist."""
    # Create a path that doesn't exist
    invalid_path = Path("/nonexistent/path/to/file.py")

    with pytest.raises(ValueError, match="neither a file nor a directory"):
        analyze_path(invalid_path)
