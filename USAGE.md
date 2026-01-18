# Quick Start Guide

## Installation

```bash
# Install dependencies
uv sync

# Or install the package
uv pip install -e .
```

## Basic Usage

### Analyze a single file

```bash
uv run pycole example.py
```

### Analyze a directory

```bash
uv run pycole src/
```

### Analyze the entire project

```bash
uv run pycole .
```

## Understanding the Output

The tool reports five key metrics:

1. **Total lines of code**: All lines including comments, blank lines, and code
2. **Lines without comments/blanks**: Pure code lines (excludes comments and empty lines)
3. **Number of statements**: Count of Python statements parsed from AST
4. **Total lines of test code**: All lines in test files
5. **Test lines without comments/blanks**: Pure code lines in test files only

## Test File Detection

Files are considered test files if they:
- Start with `test_` (e.g., `test_analyzer.py`)
- End with `_test.py` (e.g., `analyzer_test.py`)
- Are located in a `tests/` or `test/` directory

## Example

```bash
$ uv run pycole example.py

============================================================
Python Code Analysis: example.py
============================================================

Total lines of code:                                22
Lines without comments/blanks:                      14
Number of statements:                               12
Total lines of test code:                            0
Test lines without comments/blanks:                  0

============================================================
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=pycole tests/
```
