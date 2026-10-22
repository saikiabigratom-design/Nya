# ঞ (Nya) — Vocal for Local

*Search beyond language.*

**Product promise:** Find useful information in your language, explore trustworthy sources, and understand answers grounded in evidence.

---

## 1. Overview

**ঞ (Nya)** is an Assamese-first, regional-language-aware search engine combining lexical web retrieval with source-grounded AI answers. It is specifically designed to overcome language barriers for native-script Assamese, English, Romanized Assamese (Latin-script phonetic Assamese), and mixed-language queries.

### Key Differentiators

- **Regional-Language-Aware Search:** Normalizes Assamese Unicode characters (ৱ, ৰ, ক্ষ, য়, ড়, ঢ়, diacritics, and ZWJ/ZWNJ cleanup) and maps Romanized Assamese phonetic queries (e.g. *axom*, *namaskar*, *bhal*, *khobor*, *guwahati*) to native concepts.
- **Grounded AI Answers:** Generates concise answers strictly from retrieved documents, with claim-level interactive citations `[1]`, `[2]` linking directly to real sources.
- **Zero Hallucinated Citations:** Automated citation validation prevents models from citing sources that were not retrieved.
- **Domain Diversity & Balanced Discovery:** Prevents single-domain monopolization of search results via progressive domain suppression penalties.
- **Privacy by Default:** Raw user search queries are **never** logged to server access logs. User feedback query hashes are anonymized using SHA-256. Guest-first with zero behavioral advertising profiles.
- **Lawful Ingestion & SSRF Protection:** Respects `robots.txt`, enforces rate limits, restricts crawls to permitted registries, and blocks Server-Side Request Forgery (SSRF) into private networks.

---

## 2. Technology Stack

- **Web Frontend:** Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Lucide icons.
- **Search & API Service:** Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy 2.0, asyncio.
- **Database & Storage:**
  - **Local Development / Windows:** Zero-config SQLite with asynchronous `aiosqlite`.
  - **Production / Container:** PostgreSQL 16 with `pgvector` and `tsvector` full-text search.
- **AI Gateway:** Provider-agnostic inference layer supporting Google Gemini API, OpenAI, Ollama, and deterministic offline mock fallback.
- **Ingestion & Crawler:** Python crawler with robots.txt compliance and SSRF defense.
- **Evaluation Harness:** nDCG@10 multilingual evaluation benchmark.

---

## 3. Brand Identity

- **Brand Mark:** `ঞ` (Accessible name: "Nya")
- **Color Palette:**
  - Midnight Indigo: `#111D35`
  - Signal Teal: `#5CE1D0`
  - Paper White: `#F8FAFC`
  - Supporting Slate: `#64748B`

---

## 4. Project Structure

```text
nya-search/
├── apps/
│   └── web/                   # Next.js 14 frontend application
│       ├── src/app/           # App router pages (homepage, search results)
│       ├── src/components/    # BrandMark, SearchBox, AIAnswerPanel, SearchFilters, etc.
│       └── test-runner.js     # Frontend verification test runner
├── services/
│   └── search-api/            # FastAPI backend service
│       ├── api/               # API routes and privacy middleware
│       ├── nlp/               # Assamese normalizer, transliterator, script detector
│       ├── search/            # Retrieval engine, multi-signal ranking, domain diversity
│       ├── ai/                # Provider-agnostic gateway, citation validator, prompt defense
│       └── db/                # Database models and async session
├── ingestion/                 # Source registry, crawler, extractor, indexer
├── evaluation/                # Benchmark dataset and nDCG@10 evaluation harness
├── tests/                     # Unit and integration test suites
├── infra/                     # Docker Compose & PostgreSQL init.sql
├── docs/                      # Product specification (specs.md)
└── .github/workflows/         # Continuous integration pipeline
```
