# My Project

My awesome Python project.

## Installation

```bash
pip install -e .
```

## Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Lint code
flake8

# Type checking
mypy .
```

## Usage

```python
from src.main import main

main()
```

## Project Structure

```
my-project/
├── src/           # Source code
├── tests/         # Test files
├── docs/          # Documentation
├── pyproject.toml # Project configuration
└── README.md      # This file
```