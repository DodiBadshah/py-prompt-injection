# py-prompt-injection

A black-box prompt injection test harness for LLMs, mapped to the OWASP LLM Top 10.

## What it does

py-prompt-injection fires structured attack payloads at any LLM API and scores the responses automatically. It tells you whether a model is vulnerable to prompt injection, jailbreaks, sensitive data exposure, and other OWASP-classified threats.

Think of it as Nessus for LLMs.

## Key features

- 40+ curated attack payloads across 4 OWASP LLM Top 10 categories
- Adapter layer supporting OpenAI and Anthropic APIs
- Heuristic scoring engine with pass/fail verdicts
- HTML and PDF reports
- MLflow experiment tracking
- Single CLI command to run a full audit

## Project status

All 13 components complete. CI passing on GitHub Actions.
