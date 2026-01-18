"""Tests for the pycole analyzer module."""

import tempfile
from pathlib import Path

from pycole.analyzer import (
    analyze_file,
    analyze_directory,
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
        assert metrics.test_code_lines == 6  # All code lines go to test metrics
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
