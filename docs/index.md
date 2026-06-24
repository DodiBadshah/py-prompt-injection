# py-prompt-injection

A black-box prompt injection test harness for LLMs, mapped to the OWASP LLM Top 10 2023-24.

> **Status:** Phase 1 and Phase 2 complete. Phase 1 findings and responsible disclosure advisory published. Phase 3 (py-rag-security) in development.

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

Phase 1: All 13 components complete. CI passing on GitHub Actions.

Phase 2 (py-prompt-injection-2025) complete. OWASP LLM Top 10 2025 payload catalog built, LangChain orchestration wired.

[View Phase 2 on GitHub](https://github.com/DodiBadshah/py-prompt-injection-2025)