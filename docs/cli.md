# CLI Reference

py-prompt-injection exposes a single command through its CLI.

## Installation

    git clone https://github.com/DodiBadshah/py-prompt-injection
    cd py-prompt-injection
    python -m venv .venv
    .venv\Scripts\activate
    pip install -e ".[dev]"

## Environment variables

For cloud models:

    export ANTHROPIC_API_KEY=your_anthropic_key
    export OPENAI_API_KEY=your_openai_key

For local Ollama models no API key is required.

## run command

Fires all payloads at a target LLM and generates a report.

    .venv\Scripts\python.exe -m llm_probe.cli.main [OPTIONS]

## Options

| Option | Type | Default | Description |
|---|---|---|---|
| --model | text | required | Model name to target e.g. claude-haiku-4-5, gpt-4o-mini, phi3:mini |
| --owasp | text | None | Filter payloads by OWASP category e.g. LLM01 |
| --output | path | reports/ | Path to write the HTML report |
| --pdf | flag | False | Also export a PDF report |
| --verbose | flag | False | Enable debug logging |

## Examples

Run all payloads against Claude Haiku:

    .venv\Scripts\python.exe -m llm_probe.cli.main --model claude-haiku-4-5

Run only LLM01 payloads against GPT-4o-mini:

    .venv\Scripts\python.exe -m llm_probe.cli.main --model gpt-4o-mini --owasp LLM01

Run against a local Ollama model (no API key needed):

    .venv\Scripts\python.exe -m llm_probe.cli.main --model phi3:mini
    .venv\Scripts\python.exe -m llm_probe.cli.main --model mistral:7b

Run a single OWASP category against a local model:

    .venv\Scripts\python.exe -m llm_probe.cli.main --model phi3:mini --owasp LLM06

## Supported models

| Provider | Examples |
|---|---|
| Anthropic | claude-haiku-4-5, claude-sonnet-4-6 |
| OpenAI | gpt-4o-mini, gpt-4o |
| Ollama (local) | phi3:mini, mistral:7b, llama3.1:8b, llama3.2:3b, gemma2:2b, gemma2:9b |

## Output files

After a run completes the HTML report is written to the reports/ directory. Use --pdf to also export a PDF.

MLflow logs are written to the mlruns/ directory. Run `mlflow ui` to browse them.