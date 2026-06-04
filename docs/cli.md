# CLI Reference

py-prompt-injection exposes a single command through its CLI.

## Installation

    git clone https://github.com/DodiBadshah/py-prompt-injection
    cd py-prompt-injection
    python -m venv .venv
    .venv\Scripts\activate
    pip install -e ".[dev]"

## Environment variables

    export ANTHROPIC_API_KEY=your_anthropic_key
    export OPENAI_API_KEY=your_openai_key

## run command

Fires all payloads at a target LLM and generates a report.

    python -m llm_probe.cli run [OPTIONS]

## Options

| Option | Type | Default | Description |
|---|---|---|---|
| --adapter | text | anthropic | Adapter to use: anthropic or openai |
| --model | text | claude-3-haiku-20240307 | Model name to target |
| --category | text | None | Filter payloads by OWASP category e.g. LLM01 |
| --output | path | reports/ | Directory to write HTML and PDF reports |

## Examples

Run all payloads against Claude Haiku:

    python -m llm_probe.cli run --adapter anthropic --model claude-3-haiku-20240307

Run only LLM01 payloads against GPT-4o:

    python -m llm_probe.cli run --adapter openai --model gpt-4o --category LLM01

Write reports to a custom directory:

    python -m llm_probe.cli run --adapter anthropic --model claude-3-haiku-20240307 --output my-reports/

## Output files

After a run completes two files are written to the output directory:

- `report.html` - styled report viewable in any browser
- `report.pdf` - same report exported to PDF for sharing

MLflow logs are written to the `mlruns/` directory. Run `mlflow ui` to browse them.
