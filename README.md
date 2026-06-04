# py-prompt-injection

[![CI](https://github.com/DodiBadshah/py-prompt-injection/actions/workflows/ci.yml/badge.svg)](https://github.com/DodiBadshah/py-prompt-injection/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-live-brightgreen)](https://dodibadshah.github.io/py-prompt-injection/)

A black-box prompt injection test harness for LLMs, mapped to the OWASP LLM Top 10.

Fire structured attack payloads at any OpenAI or Anthropic model, score responses automatically, and generate HTML and PDF security reports.

**[Full documentation](https://dodibadshah.github.io/py-prompt-injection/)**

## Why this exists

Prompt injection is the number one risk in the OWASP LLM Top 10 (LLM01). There is no standard open-source tool for systematically testing LLMs against a curated payload catalog the way Nessus tests network services. This project fills that gap.

## Architecture

```text
payloads/catalog/*.yaml  -->  payloads/loader.py  -->  runner/runner.py
                                                          /          \
                                               openai_adapter   anthropic_adapter
                                                          \          /
                                                       scoring/engine.py
                                                              |
                                               reporting/ (HTML + PDF)  +  MLflow
```

## OWASP LLM Top 10 coverage

| ID | Category | Payloads |
|----|----------|----------|
| LLM01 | Prompt Injection | 10 |
| LLM02 | Insecure Output Handling | 5 |
| LLM06 | Sensitive Information Disclosure | 5 |
| LLM08 | Excessive Agency | 5 |

## Quickstart

Requirements: Python 3.11+, an OpenAI or Anthropic API key.

```bash
git clone https://github.com/DodiBadshah/py-prompt-injection.git
cd py-prompt-injection
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Run all payloads against GPT-4o-mini:

```bash
python -m llm_probe run --adapter openai --model gpt-4o-mini
```

Run a single OWASP category:

```bash
python -m llm_probe run --adapter anthropic --model claude-3-haiku-20240307 --category LLM01
```

Output: HTML and PDF reports written to `reports/`.

## Example output

```text
Running 25 payloads against openai/gpt-4o-mini
Results: 18 flagged / 7 passed
Report written to reports/report_20250601_143022.html
PDF written to reports/report_20250601_143022.pdf
```

## Project structure

```text
llm_probe/
  adapters/        API adapters (OpenAI, Anthropic)
  core/            Config, logging, exceptions
  payloads/        YAML catalog + loader
  reporting/       HTML/PDF renderer
  runner/          Orchestration + MLflow
  schemas/         Pydantic models
  scoring/         Heuristics + scoring engine
  cli/             Typer CLI entrypoint
tests/             pytest suite (40 tests)
.github/workflows/ CI pipeline
docs/              MkDocs source
```

## Development

```bash
pytest        # run all 40 tests
pytest -v     # verbose
```

CI runs automatically on every push via GitHub Actions.

## License

MIT