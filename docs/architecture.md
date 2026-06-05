# Architecture

py-prompt-injection is built in seven layers. Each layer has a single responsibility and depends only on the layers below it.

## Layer diagram

    CLI (cli/main.py)
        |
    Runner (runner/runner.py)
        |
    Adapter Layer (adapters/)
        |
    Scoring Engine (scoring/)
        |
    Schemas (schemas/)
        |
    Payload Loader (payloads/)
        |
    Core (core/)

## Layers explained

### Core
Handles configuration, logging, and custom exceptions. Every other layer imports from here. Config is loaded from environment variables via a Pydantic Settings model.

### Payload Loader
Reads YAML files from `payloads/catalog/` and deserializes them into `Payload` objects. Each YAML file maps to one OWASP category.

### Schemas
Two Pydantic models define the data contracts for the entire project:

- `Payload` - one attack prompt with its category, expected behavior, and severity
- `Result` - the outcome after firing a payload, including the raw response, score, and verdict

### Adapter Layer
Wraps the OpenAI, Anthropic, and Ollama APIs behind a common `BaseAdapter` interface. The runner does not know or care which LLM it is talking to.

Three adapters are available:

| Adapter | Provider | API key required |
|---|---|---|
| AnthropicAdapter | Anthropic cloud | Yes |
| OpenAIAdapter | OpenAI cloud | Yes |
| OllamaAdapter | Local Ollama instance | No |

The correct adapter is selected automatically based on the model name passed to the CLI.

### Scoring Engine
Takes a raw model response and a Payload and returns a scored Result. Uses heuristics to detect refusals, compliance with injection instructions, and sensitive data leakage.

### Runner
Orchestrates the full test run. Iterates over payloads, calls the adapter, routes responses to the scoring engine, logs results to MLflow, and collects the final list of Results.

### CLI
Built with Typer. Exposes a single command that accepts model, OWASP category filter, output path, and verbosity arguments. Auto-detects the correct adapter from the model name.

## Data flow

    YAML catalogs -> Payload objects -> Runner -> Adapter -> LLM API (cloud or local)
                                           |
                                      Raw response
                                           |
                                     Scoring Engine -> Result objects
                                           |
                                      Reporter -> HTML + PDF
                                           |
                                       MLflow log