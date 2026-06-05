# py-prompt-injection

[![CI](https://github.com/DodiBadshah/py-prompt-injection/actions/workflows/ci.yml/badge.svg)](https://github.com/DodiBadshah/py-prompt-injection/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-live-brightgreen)](https://dodibadshah.github.io/py-prompt-injection/)

A black-box prompt injection test harness for LLMs, mapped to the OWASP LLM Top 10.

Fire structured attack payloads at any OpenAI, Anthropic, or local Ollama model, score responses automatically, and generate HTML and PDF security reports.

**[Full documentation](https://dodibadshah.github.io/py-prompt-injection/)**

## Why this exists

Prompt injection is the number one risk in the OWASP LLM Top 10 (LLM01). There is no standard open-source tool for systematically testing LLMs against a curated payload catalog the way Nessus tests network services. This project fills that gap.

## Architecture

```text
payloads/catalog/*.yaml  -->  payloads/loader.py  -->  runner/runner.py
                                                          /          \
                                    openai_adapter   anthropic_adapter   ollama_adapter
                                                          \          /
                                                       scoring/engine.py
                                                              |
                                               reporting/ (HTML + PDF)  +  MLflow
```

## OWASP LLM Top 10 coverage

| ID | Category | Payloads |
|----|----------|----------|
| LLM01 | Prompt Injection | 6 |
| LLM02 | Insecure Output Handling | 6 |
| LLM06 | Sensitive Information Disclosure | 6 |
| LLM08 | Excessive Agency | 6 |

## Quickstart

### Cloud models

Requirements: Python 3.11+, an OpenAI or Anthropic API key.

```bash
git clone https://github.com/DodiBadshah/py-prompt-injection.git
cd py-prompt-injection
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Run all payloads against Claude Haiku:

```bash
.venv\Scripts\python.exe -m llm_probe.cli.main --model claude-haiku-4-5
```

Run a single OWASP category:

```bash
.venv\Scripts\python.exe -m llm_probe.cli.main --model claude-haiku-4-5 --owasp LLM01
```

### Local models via Ollama

No API key required. Runs entirely on your machine.

```bash
# Install Ollama from https://ollama.com
ollama pull phi3:mini
ollama pull mistral:7b
```

Run the full suite against a local model:

```bash
.venv\Scripts\python.exe -m llm_probe.cli.main --model phi3:mini
.venv\Scripts\python.exe -m llm_probe.cli.main --model mistral:7b
```

Supported local models: `phi3:mini`, `mistral:7b`, `llama3.2`, `gemma2:2b`

Output: HTML reports written to `reports/`.

## Example output

```text
Running 24 payloads against ollama/phi3:mini
Results: 24/24 payloads passed.
Report written to reports/report-20260605-051442-phi3-mini.html
```

## Project structure

```text
llm_probe/
  adapters/        API adapters (OpenAI, Anthropic, Ollama)
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

## Security

This project handles LLM API keys and executes prompt injection payloads against live models. The following checks were run against the codebase:

- `bandit` - 0 issues across 892 lines of code
- `pip-audit` - no known CVEs in any dependency
- `detect-secrets` - no credentials or secrets detected
- YAML loading uses `safe_load` throughout, preventing arbitrary code execution
- `.env` verified absent from all git history

## License

MIT