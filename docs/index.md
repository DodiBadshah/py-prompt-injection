# py-prompt-injection

A black-box prompt injection test harness for LLMs, mapped to the OWASP LLM Top 10 2023-24.

> **Work in Progress:** This project is under active development. Results, scoring methodology, and documentation may change as Phase 1 findings are refined and Phase 2 development progresses.

## What it does

py-prompt-injection fires structured attack payloads at any LLM API and scores the responses automatically. It tells you whether a model is vulnerable to prompt injection, jailbreaks, sensitive data exposure, and other OWASP-classified threats.

Think of it as Nessus for LLMs.

## Key features

- 24 curated attack payloads across 4 OWASP LLM Top 10 2023-24 categories
- Adapter layer supporting OpenAI, Anthropic, and local Ollama models
- Two-generation heuristic scoring engine with documented improvements between generations
- Pass/fail verdicts with per-payload scoring
- HTML and PDF reports
- MLflow experiment tracking
- Single CLI command to run a full audit

## Project status

All 13 components complete. CI passing on GitHub Actions.
