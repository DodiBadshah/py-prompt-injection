# Contributing

## Setup

    git clone https://github.com/DodiBadshah/py-prompt-injection
    cd py-prompt-injection
    python -m venv .venv
    .venv\Scripts\activate
    pip install -e ".[dev]"

## Running tests

    pytest --tb=short

All 40 tests must pass before submitting a pull request.

## Project structure

    py-prompt-injection/
    ├── llm_probe/
    │   ├── core/
    │   ├── schemas/
    │   ├── payloads/
    │   ├── adapters/
    │   ├── scoring/
    │   ├── runner/
    │   ├── reporting/
    │   └── cli/
    ├── tests/
    ├── docs/
    └── .github/workflows/

## Adding a new adapter

1. Create a new file in `llm_probe/adapters/` named `yourprovider_adapter.py`
2. Subclass `BaseAdapter` from `adapters/base.py`
3. Implement the `send` method following the existing adapter pattern
4. Add the adapter name to the CLI choices in `cli/main.py`
5. Write tests in `tests/test_adapters.py`

## Adding new payloads

1. Open the relevant YAML file in `llm_probe/payloads/catalog/`
2. Add a new entry following the existing schema
3. Run the test suite to confirm the loader picks it up cleanly

## Pull request checklist

- All 40 existing tests pass
- New tests added for any new functionality
- Docstrings added for new public classes and functions
- mkdocs build passes with no warnings
