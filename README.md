# pycole

**Python Code Length Analyzer** - A command-line tool to analyze Python files and projects for code metrics.

Disclaimer: This tool is created using Claude Sonnet 4.5.

## Features

`pycole` analyzes Python files or directories and provides:

- **Total lines of code** - All lines in the file(s) (including tests)
- **Lines without comments/blanks** - Only actual code lines (excluding test files)
- **Number of statements** - Count of Python statements using AST parsing (excluding test files)
- **Total lines of test code** - Lines in test files (files starting with `test_` or in `tests/` directory)
- **Test lines without comments/blanks** - Code-only lines in test files

This separation allows you to see production code metrics separately from test code metrics.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repository
git clone https://github.com/lyubolp/pycole.git
cd pycole

# Install with uv
uv sync

# Install in development mode
uv pip install -e .
```

## Usage

Analyze a single Python file:

```bash
uv run pycole path/to/file.py
```

Analyze an entire directory:

```bash
uv run pycole path/to/project/
```

Or if installed globally:

```bash
pycole path/to/file.py
pycole path/to/project/
```

### Example Output

```
============================================================
Python Code Analysis: src/pycole
============================================================

Total lines of code:                           156
Lines without comments/blanks:                 128
Number of statements:                           89
Total lines of test code:                       95
Test lines without comments/blanks:             82

============================================================
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_analyzer.py
```

### Project Structure

```
pycole/
├── src/
│   └── pycole/
│       ├── __init__.py
│       ├── analyzer.py    # Core analysis logic
│       └── cli.py         # Command-line interface
├── tests/
│   └── test_analyzer.py   # Unit tests
├── pyproject.toml         # Project configuration
└── README.md
```

## How It Works

- **Line Counting**: Counts total lines and filters out blank lines and comment-only lines
- **Statement Counting**: Uses Python's `ast` module to parse and count statement nodes
- **Test Detection**: Identifies test files by naming conventions (`test_*.py`, `*_test.py`) or location (`tests/` directory)
- **Directory Analysis**: Recursively scans directories, skipping virtual environments and common ignore patterns

## Requirements

- Python >= 3.14
- click >= 8.1.7

## License

See LICENSE file for details.
Python Code Length
