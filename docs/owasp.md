# OWASP LLM Top 10 Mapping

py-prompt-injection covers four categories from the OWASP LLM Top 10 (2023-24).

## Coverage summary

| OWASP ID | Name | Payloads | Status |
|---|---|---|---|
| LLM01 | Prompt Injection | 6 | Covered |
| LLM02 | Insecure Output Handling | 6 | Covered |
| LLM06 | Sensitive Information Disclosure | 6 | Covered |
| LLM08 | Excessive Agency | 6 | Covered |
| LLM03 | Training Data Poisoning | 0 | Not in scope |
| LLM04 | Model Denial of Service | 0 | Not in scope |
| LLM05 | Supply Chain Vulnerabilities | 0 | Not in scope |
| LLM07 | Insecure Plugin Design | 0 | Not in scope |
| LLM09 | Overreliance | 0 | Not in scope |
| LLM10 | Model Theft | 0 | Not in scope |

## Payload alignment with 2023-24

21 of 24 payloads map directly to named OWASP LLM Top 10 2023-24 attack scenarios or common vulnerability examples. 2 payloads (llm01-005, llm02-006) are practical extensions within the same attack classes, covering encoding-based evasion and spreadsheet formula injection respectively. 1 payload (llm06-005) partially maps to the general unintended disclosure class, covering model configuration metadata specifically.

## Why these four

LLM01, LLM02, LLM06, and LLM08 are the categories testable through black-box API interaction alone. The remaining six require access to training pipelines, deployment infrastructure, or plugin systems outside the scope of a black-box harness.

## LLM01 - Prompt Injection

The highest severity category. An attacker manipulates a model through crafted input, causing it to ignore its system prompt or execute unintended instructions.

Payloads cover: classic instruction override, role reassignment via DAN framing, nested injection inside a translation task, fictional framing, base64 encoded instructions (practical extension beyond 2023-24 named scenarios), and completion attacks.

## LLM02 - Insecure Output Handling

Occurs when model output is passed downstream to another system without validation. py-prompt-injection probes whether a model can be coaxed into generating dangerous output.

Payloads cover: XSS script injection, markdown exfiltration via remote image URL, SQL injection in generated queries, shell command injection, HTML javascript protocol handlers, and CSV formula injection (practical extension beyond 2023-24 named scenarios).

## LLM06 - Sensitive Information Disclosure

Tests whether a model can be prompted into revealing its system prompt, training data, or other confidential information. A passing model refuses these probes or returns a generic non-answer.

Payloads cover: direct system prompt extraction, training data memorization, credential extraction via authority claim, PII generation via database roleplay, configuration metadata disclosure (partial match to general unintended disclosure class), and indirect system prompt summarization.

## LLM08 - Excessive Agency

Tests whether a model can be manipulated into claiming capabilities or taking actions beyond its intended scope. Relevant for agentic deployments where the model has access to tools or external systems.

Payloads cover: destructive file system actions, financial transactions, privilege escalation with assumed admin role, server-side code execution, autonomous HR decisions, and chained multi-step task execution without human approval. All 6 payloads map directly to named 2023-24 scenarios.
