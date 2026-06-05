# Roadmap

This project is Phase 1 of a three-phase LLM security portfolio.

## Phase overview

| Phase | Repository | OWASP Coverage | Status |
|---|---|---|---|
| Phase 1 | [py-prompt-injection](https://github.com/DodiBadshah/py-prompt-injection) | LLM01, LLM02, LLM06, LLM08 | Complete |
| Phase 2 | [py-rag-security](https://github.com/DodiBadshah/py-rag-security) | LLM03, LLM09 | In Development |
| Phase 3 | py-llm-load | LLM04, LLM10 | Planned |

## Phase 1 - Prompt Injection Harness (this project)

Covers the four OWASP LLM Top 10 categories testable via black-box payload
firing against any OpenAI, Anthropic, or local Ollama model:

- LLM01 - Prompt Injection
- LLM02 - Insecure Output Handling
- LLM06 - Sensitive Information Disclosure
- LLM08 - Excessive Agency

**Stack:** pydantic v2, typer, loguru, weasyprint, mlflow, anthropic and openai SDKs, Ollama.

## Phase 2 - RAG Security Evaluation Framework

Target repository: `github.com/DodiBadshah/py-rag-security`

Extends this harness with a ChromaDB vector store and retrieval pipeline to
test LLM vulnerabilities that require document context:

- **LLM03 - Training Data Poisoning:** Injects manipulated documents into the
  retrieval store and measures whether the model surfaces poisoned content
- **LLM09 - Misinformation:** Tests whether grounded RAG responses can be
  manipulated to produce false but confident-sounding output

**New in Phase 2:**

- `store/` - ChromaDB vector store, OpenAI embeddings, retriever
- `poisoner/` - document builder and injector for attack context
- `scoring/judge.py` - LLM-as-judge scorer (documented upgrade path from Phase 1)

**Reused from Phase 1:**

- `adapters/` - OpenAI, Anthropic, Ollama unchanged
- `scoring/heuristics.py` - extended, not replaced
- `reporting/` - new RAG-specific template added alongside existing one
- MLflow experiment tracking spans both phases for cross-phase comparison

## Phase 3 - Load and Resource Testing

Target repository: `github.com/DodiBadshah/py-llm-load`

Adds load testing infrastructure to cover the two remaining OWASP categories
that require concurrency and resource monitoring:

- **LLM04 - Model Denial of Service**
- **LLM10 - Unbounded Consumption**

**New in Phase 3:**

- `load/` - concurrent request engine using asyncio
- `monitor/` - token counting and resource tracking layer
- Integration with locust for load scenario definition