# Roadmap

This project is Phase 1 of a four-phase LLM security portfolio.

## Phase overview

| Phase | Repository | OWASP Coverage | Status |
|---|---|---|---|
| Phase 1 | [py-prompt-injection](https://github.com/DodiBadshah/py-prompt-injection) | LLM01, LLM02, LLM06, LLM08 (2023-24) | Complete |
| Phase 2 | [py-prompt-injection-2025](https://github.com/DodiBadshah/py-prompt-injection-2025) | LLM01, LLM02, LLM05, LLM06, LLM07 (2025) | Complete |
| Phase 3 | py-rag-security | LLM08, LLM09 (2025) | Planned |
| Phase 4 | py-llm-load | LLM10 (2025) | Planned |

## Phase 1 - Prompt Injection Harness (this project)

Covers the four OWASP LLM Top 10 2023-24 categories testable via black-box payload
firing against any OpenAI, Anthropic, or local Ollama model:

- LLM01 - Prompt Injection
- LLM02 - Insecure Output Handling
- LLM06 - Sensitive Information Disclosure
- LLM08 - Excessive Agency

**Stack:** pydantic v2, typer, loguru, weasyprint, mlflow, anthropic and openai SDKs, Ollama.

**Published outputs:** [Phase 1 Findings Report](phase1-findings.html) and [Security Advisory ADV-001](advisory-001.html).

## Phase 2 - OWASP 2025 Payload Coverage with LangChain

Target repository: `github.com/DodiBadshah/py-prompt-injection-2025`

Same black-box harness architecture as Phase 1, extended to cover OWASP LLM Top 10
2025 categories including system prompt leakage, improper output handling, and
updated excessive agency. Primary purpose is LangChain orchestration replacing raw API calls.

**New in Phase 2:**

- `chains/` - LangChain model adapters and chain execution layer
- OWASP 2025 YAML payload catalog (new categories, same schema as Phase 1)
- Async execution via asyncio for reduced total run time

**Reused from Phase 1:**

- pydantic v2 schemas (payload, result)
- MLflow experiment tracking
- HTML report generation
- GitHub Actions CI/CD

## Phase 3 - RAG Security Evaluation Framework

Target repository: `github.com/DodiBadshah/py-rag-security`

A production RAG pipeline built over compliance and security document corpora
(HIPAA, NIST SP 800-53, CIS Controls v8). Tests for RAG-specific security
vulnerabilities including poisoned document injection and manipulated retrieval
context, covering OWASP LLM08 and LLM09. Full stack deployment to Azure Container Apps.

- **LLM08 - Vector and Embedding Weaknesses:** Injects adversarial documents into
  the retrieval store and measures whether the pipeline retrieves and surfaces the
  poisoned content
- **LLM09 - Misinformation:** Tests whether grounded RAG responses can be
  manipulated to produce false but confident-sounding output

**New in Phase 3:**

- `store/` - Pinecone vector store, OpenAI embeddings, BM25 hybrid retrieval, Cohere reranking
- `scoring/judge.py` - LLM-as-judge scorer replacing keyword heuristics
- FastAPI backend with Docker containerization
- Azure Container Apps deployment via GitHub Actions

## Phase 4 - Load and Resource Testing

Target repository: `github.com/DodiBadshah/py-llm-load`

Adds load testing infrastructure covering resource-exhaustion attacks: concurrent
request flooding, token consumption, and cost amplification. Brings suite coverage
to eight of the ten OWASP LLM Top 10 2025 categories, with LLM03 (Supply Chain) and
LLM04 (Data and Model Poisoning) documented as out of scope for a black-box and
RAG-runtime harness.

- **LLM10 - Unbounded Consumption:** Concurrent load, token flooding, and
  denial-of-wallet cost attacks against models and the Phase 3 RAG endpoint

**New in Phase 4:**

- `load/` - asyncio-based concurrent request engine
- `monitor/` - token consumption tracking and cost curve analysis
- HTML token consumption dashboard
- Cross-phase research: security behaviour under load (Phase 1/2 payloads fired under Phase 4 load)