"""Core analyzer module for counting lines and statements in Python code."""

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CodeMetrics:
    """Metrics for a Python file or project."""

    total_lines: int
    code_lines: int  # Lines without comments and blank lines
    statements: int
    test_lines: int
    test_code_lines: int  # Test lines without comments and blank lines


def is_test_file(filepath: Path) -> bool:
    """Check if a file is a test file based on naming conventions."""
    name = filepath.name
    parent = filepath.parent.name
    return name.startswith("test_") or name.endswith("_test.py") or parent == "tests" or parent == "test"


def count_statements(code: str) -> int:
    """Count the number of statements in Python code using AST."""
    try:
        tree = ast.parse(code)
        return sum(1 for _ in ast.walk(tree) if isinstance(_, ast.stmt))
    except SyntaxError:
        return 0


def analyze_file(filepath: Path) -> CodeMetrics:
    """Analyze a single Python file and return metrics."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        return CodeMetrics(0, 0, 0, 0, 0)

    lines = content.splitlines()
    total_lines = len(lines)

    # Count code lines (non-blank, non-comment lines)
    file_code_lines = sum(1 for line in lines if (stripped := line.strip()) and not stripped.startswith("#"))

    # Count statements
    file_statements = count_statements(content)

    # Determine if this is a test file
    is_test = is_test_file(filepath)

    if is_test:
        # For test files: don't count in main metrics, only in test metrics
        test_lines = total_lines
        test_code_lines = file_code_lines
        code_lines = 0
        statements = 0
    else:
        # For non-test files: count in main metrics, not in test metrics
        test_lines = 0
        test_code_lines = 0
        code_lines = file_code_lines
        statements = file_statements

    return CodeMetrics(
        total_lines=total_lines,
        code_lines=code_lines,
        statements=statements,
        test_lines=test_lines,
        test_code_lines=test_code_lines,
    )


def analyze_directory(dirpath: Path) -> CodeMetrics:
    """Analyze all Python files in a directory recursively."""
    total_lines = 0
    code_lines = 0
    statements = 0
    test_lines = 0
    test_code_lines = 0

    # Find all Python files recursively
    python_files = list(dirpath.rglob("*.py"))

    for filepath in python_files:
        # Skip virtual environments and common ignore patterns
        skip_patterns = [".venv", "venv", "__pycache__", ".git", "node_modules"]
        if any(part in filepath.parts for part in skip_patterns):
            continue

        metrics = analyze_file(filepath)
        total_lines += metrics.total_lines
        code_lines += metrics.code_lines
        statements += metrics.statements
        test_lines += metrics.test_lines
        test_code_lines += metrics.test_code_lines

    return CodeMetrics(
        total_lines=total_lines,
        code_lines=code_lines,
        statements=statements,
        test_lines=test_lines,
        test_code_lines=test_code_lines,
    )


def analyze_path(path: Path) -> CodeMetrics:
    """Analyze a file or directory and return metrics."""
    if path.is_file():
        return analyze_file(path)
    if path.is_dir():
        return analyze_directory(path)
    raise ValueError(f"Path {path} is neither a file nor a directory")
