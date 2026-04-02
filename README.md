# RAG Mongo Demo v7

End-to-end Retrieval-Augmented Generation (RAG) demo for QA assets, built with:
- **React (MUI)** frontend for data ingestion, embeddings, search, reranking, summarization, and prompt/schema workflows
- **Node.js + Express** backend API
- **MongoDB Atlas Vector Search + Atlas Search (BM25)**
- **Mistral AI** for embedding generation
- **Groq** for reranking and summarization

This project is optimized for test-case intelligence workflows (especially healthcare-style QA content), with support for both test cases and user stories.

---

## What this project does

- Convert Excel test case files into JSON (`/api/upload-excel`)
- Create embeddings in batch and store into MongoDB (`/api/create-embeddings-batch`)
- Run multiple retrieval modes:
  - Vector semantic search (`/api/search`)
  - BM25 keyword search (`/api/search/bm25`)
  - Hybrid score fusion (`/api/search/hybrid`)
  - LLM reranking (`/api/search/rerank`)
- Preprocess and expand user queries (`/api/search/preprocess`, `/api/search/analyze`)
- Deduplicate and summarize result sets (`/api/search/deduplicate`, `/api/search/summarize`)
- Test prompt templates against Groq (`/api/test-prompt`)
- Evaluate generated/reference test cases with Metrics Evaluation (Sprint 4/5/6 rollout completed)
- Manage runtime `.env` values from UI (`/api/env` GET/POST)

---

## Repository structure

```text
.
├── client/                         # React app (UI)
│   └── src/components/
│       ├── data/                   # Convert + Embeddings screens
│       ├── search/                 # Vector/BM25/Hybrid/Rerank screens
│       ├── processing/             # Preprocessing, summarization, prompt/schema
│       └── settings/               # .env editor UI
├── server/
│   └── index.js                    # Express API (single-file backend)
├── src/
│   ├── config/                     # Atlas index definitions (vector + BM25)
│   ├── data/                       # JSON source files for ingestion
│   └── scripts/
│       ├── data-conversion/        # Excel/Jira data scripts
│       ├── embeddings/             # Batch embedding + Mongo insert scripts
│       ├── query-preprocessing/    # Normalization/synonym pipeline
│       ├── search/                 # CLI search experiments
│       └── utilities/              # Mistral/Groq/Mongo helpers
└── releases/                       # Release-specific story inputs
```

---

## Prerequisites

- **Node.js**: 18+
- **npm**: 9+
- **MongoDB Atlas** cluster with:
  - one vector index for test cases
  - one BM25 Atlas Search index for test cases
  - optional vector index for user stories
- API keys:
  - Mistral (`MISTRAL_API_KEY`)
  - Groq (`GROQ_API_KEY`) for reranking/summarization/prompt testing

---

## Environment setup

1. Copy env template:

```bash
cp .env.example .env
```

2. Update `.env` values:

```env
MONGODB_URI="..."
DB_NAME="..."
COLLECTION_NAME="..."
VECTOR_INDEX_NAME="..."
BM25_INDEX_NAME="..."
USER_STORIES_COLLECTION_NAME="..."
USER_STORIES_VECTOR_INDEX_NAME="..."
MISTRAL_API_KEY="..."
MISTRAL_EMBEDDING_MODEL="mistral-embed"
GROQ_API_KEY="..."
GROQ_RERANK_MODEL="openai/gpt-oss-120b"
GROQ_SUMMARIZATION_MODEL="openai/gpt-oss-120b"
```

> You can also edit these from the UI (**Settings** page), which reads/writes root `.env` via `/api/env`.

---

## Install & run

From repo root:

```bash
npm install
npm run dev
```

This starts:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:3001/api`

### Other useful commands

```bash
npm run client    # start only React app
npm run server    # start only API server
npm run build     # build frontend bundle
```

---

## Data + index prerequisites

### 1) Ingest data

- Use UI **Convert to JSON** to upload `.xlsx/.xls`
- Converted files are written to `src/data/`
- Use **Embeddings & Store** to batch embed and insert into MongoDB

### 2) Create Atlas indexes

Use definitions under:
- `src/config/testcases-vector-index.json`
- `src/config/testcases-bm25-index.json`
- `src/config/user-stories-vector-index.json`
- `src/config/user-stories-bm25-index.json`

Current vector config expects **1024 dimensions** (`mistral-embed`).

---

## Main UI modules

- **Convert to JSON**: Excel-to-JSON transformation
- **Embeddings & Store**: Batch embedding jobs with progress polling
- **Query Preprocessing**: normalization/abbreviation/synonym expansion
- **Vector Search**: semantic retrieval
- **BM25 Search**: keyword retrieval
- **Hybrid Search**: weighted fusion of BM25 + vector
- **Score Fusion / Rerank**: Groq-powered semantic reranking
- **Summarize & Dedup**: duplicate reduction + LLM summary
- **Prompt & Schema**: prompt-template and schema workflow experiments
- **Metrics Evaluation**: scorecard-based quality assessment for selected test cases
- **Settings**: environment variable management

---

## API overview

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Health check |
| `/api/files` | GET | List JSON files in `src/data` |
| `/api/upload-excel` | POST | Upload & convert Excel to JSON |
| `/api/create-embeddings` | POST | Start embedding job |
| `/api/create-embeddings-batch` | POST | Start optimized batch embedding job |
| `/api/jobs/active` | GET | List active jobs |
| `/api/jobs/:jobId` | GET | Check job status |
| `/api/metadata/distinct` | GET | Distinct metadata for filters |
| `/api/search` | POST | Vector search |
| `/api/search/bm25` | POST | BM25 search |
| `/api/search/hybrid` | POST | Hybrid retrieval |
| `/api/search/rerank` | POST | Groq reranking |
| `/api/search/preprocess` | POST | Query preprocessing |
| `/api/search/analyze` | POST | Query transform analysis |
| `/api/search/deduplicate` | POST | Deduplicate result list |
| `/api/search/summarize` | POST | Groq summary generation |
| `/api/test-prompt` | POST | Prompt/template test endpoint |
| `/api/evaluate` | POST | Metrics evaluation bridge endpoint (introduced in Sprint 4 foundation) |
| `/api/env` | GET/POST | Read/update `.env` |
| `/api/testcases/latest-id` | GET | Compute latest test case ID |

---

## Typical workflow

1. Configure `.env` (Mongo + API keys)
2. Ensure Atlas vector + BM25 indexes exist
3. Convert input Excel to JSON
4. Run embedding batch job
5. Use Vector/BM25/Hybrid/Rerank searches
6. Run dedup + summarization on retrieved results
7. Iterate prompt/schema strategy for generated outputs
8. Run Metrics Evaluation on selected test cases (Sprint 6 sign-off complete)

---

## Metrics Evaluation (Sprint 4/5/6 Rollout)

The UI already includes a **Metrics Evaluation** tab in Prompt and Schema workflows.

Current architecture:
- UI -> `POST /api/evaluate` on main Express backend
- Express backend -> evaluator selection chain (Ragas/DeepEval)
- Backend returns normalized metric payload with observability metadata

Metric families in the UI flow:
- Faithfulness
- Answer relevancy
- Contextual precision
- Contextual recall
- Hallucination score

Current note:
- Metrics UI now routes through backend bridge (`/api/evaluate`) only.
- Sprint 4 backend bridge and normalized contract foundation are complete.
- Sprint 5 is complete: timeout/retry, evaluator fallback chain, observability fields, and UI failure diagnostics are enabled.
- Sprint 6 is complete: regression verification, Ragas completion validation, and release-readiness sign-off evidence are documented.
- Metrics cards display evaluator source and per-metric diagnostics (`explanation`, `input_arguments`, `score_breakdown`).
- UI metric selector includes DeepEval and Ragas contextual metric naming (`contextual_precision` / `context_precision`, `contextual_recall` / `context_recall`).

Evaluator control and routing env vars:
- `DEEPEVAL_URL` default: `http://localhost:8000/eval`
- `RAGAS_URL` default: `http://localhost:8000/eval-ragas`
- `PRIMARY_EVALUATOR` values: `deepeval` (default) or `ragas`

`/api/evaluate` response details now include:
- `request_id`
- `latency_ms`
- `error_class`
- `retries`
- `evaluator`
- `fallback_used`

---

## Technical lead review

### Strengths

- Clear functional UI separation across ingestion, retrieval, and LLM post-processing
- Good operational UX: async job tracking, resumable polling, user feedback via snackbars
- Supports multiple retrieval paradigms (vector/BM25/hybrid/rerank), which is excellent for relevance tuning
- Query preprocessing pipeline is modular and reusable (`src/scripts/query-preprocessing/`)
- Atlas index JSON definitions are versionable and explicit

### Risks / gaps

- `server/index.js` is a large monolith (2k+ lines), making maintainability and testing difficult
- Backend and frontend currently assume localhost URLs in multiple components (limited deployment flexibility)
- `.env` write endpoint is powerful; needs stronger hardening/authorization before shared deployments
- No centralized validation layer for API payloads (risk of drift and runtime failures)
- Limited automated test coverage for API and UI critical flows

### Recommended next improvements (priority order)

1. **Refactor backend by domain**: split routes/services (`search`, `embeddings`, `config`, `jobs`)
2. **Introduce config abstraction**: environment-aware API base URL for frontend
3. **Add validation + contract schemas**: `zod`/`joi` for all request payloads
4. **Secure config endpoints**: lock down `/api/env` with auth + allowlist
5. **Add test baseline**:
   - Backend: health, search, and embedding job API tests
   - Frontend: smoke tests for main screens
6. **Observability**: structured logging and per-endpoint timing metrics

---

## Troubleshooting

- **`GROQ_API_KEY is required`**: add valid key in `.env` and restart server
- **No metadata options shown**: collection may be empty; run embeddings first
- **Index not found errors**: verify Atlas Search/vector index names match `.env`
- **No search results**: confirm documents contain `embedding` field and expected searchable fields
- **Metrics evaluation fails**: verify evaluator service is reachable and backend `/api/evaluate` route is configured
- **Metrics tab shows service error**: check evaluator URL config and backend timeout/error mapping
- **macOS DNS/connectivity issues**: server/scripts already set DNS fallback (`8.8.8.8`, `8.8.4.4`)

---

## Notes

- This repo includes generated build artifacts under `client/build/` and local `node_modules/` in workspace snapshots; avoid committing environment-specific noise in production repos.
- For production hardening, add auth, rate limiting, request size limits, and secret-management strategy.
