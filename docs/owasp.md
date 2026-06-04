# OWASP LLM Top 10 Mapping

py-prompt-injection covers four categories from the OWASP LLM Top 10 (2025 edition).

## Coverage summary

| OWASP ID | Name | Payloads | Status |
|---|---|---|---|
| LLM01 | Prompt Injection | 12 | Covered |
| LLM02 | Insecure Output Handling | 8 | Covered |
| LLM06 | Sensitive Information Disclosure | 10 | Covered |
| LLM08 | Excessive Agency | 10 | Covered |
| LLM03 | Training Data Poisoning | 0 | Not in scope |
| LLM04 | Model Denial of Service | 0 | Not in scope |
| LLM05 | Supply Chain Vulnerabilities | 0 | Not in scope |
| LLM07 | Insecure Plugin Design | 0 | Not in scope |
| LLM09 | Overreliance | 0 | Not in scope |
| LLM10 | Model Theft | 0 | Not in scope |

## Why these four

LLM01, LLM02, LLM06, and LLM08 are the categories testable through black-box API interaction alone. The remaining six require access to training pipelines, deployment infrastructure, or plugin systems outside the scope of a black-box harness.

## LLM01 - Prompt Injection

The highest severity category. An attacker manipulates a model through crafted input, causing it to ignore its system prompt or execute unintended instructions.

## LLM02 - Insecure Output Handling

Occurs when model output is passed downstream to another system without validation. py-prompt-injection probes whether a model can be coaxed into generating dangerous output.

## LLM06 - Sensitive Information Disclosure

Tests whether a model can be prompted into revealing its system prompt, training data, or other confidential information. A passing model refuses these probes or returns a generic non-answer.

## LLM08 - Excessive Agency

Tests whether a model can be manipulated into claiming capabilities or taking actions beyond its intended scope. Relevant for agentic deployments where the model has access to tools or external systems.
