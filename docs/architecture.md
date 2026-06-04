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
Wraps the OpenAI and Anthropic SDKs behind a common `BaseAdapter` interface. The runner does not know or care which LLM it is talking to.

### Scoring Engine
Takes a raw model response and a Payload and returns a scored Result. Uses heuristics to detect refusals, compliance with injection instructions, and sensitive data leakage.

### Runner
Orchestrates the full test run. Iterates over payloads, calls the adapter, routes responses to the scoring engine, logs results to MLflow, and collects the final list of Results.

### CLI
Built with Typer. Exposes a single `run` command that accepts adapter, model, category filter, and output path arguments. Calls the runner and then the reporting layer.

## Data flow

    YAML catalogs -> Payload objects -> Runner -> Adapter -> LLM API
                                           |
                                      Raw response
                                           |
                                     Scoring Engine -> Result objects
                                           |
                                      Reporter -> HTML + PDF
                                           |
                                       MLflow log
