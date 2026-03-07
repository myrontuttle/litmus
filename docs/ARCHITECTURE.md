# Architecture Document

## Opportunity Tracker

**Version:** 0.2.0
**Status:** Draft
**Stack:** Python FastAPI (vibetuner) · MongoDB + Beanie ODM (Docker) · HTMX · Tailwind + DaisyUI · Ollama (local LLM, Docker)
**Last Updated:** 2026-03-06

---

## 1. Overview

Opportunity Tracker is a server-rendered web application built on the **vibetuner** scaffolding framework. The backend is a Python FastAPI application that owns all business logic, data access, and LLM orchestration. The frontend is driven by HTMX — the browser receives HTML fragments from the server in response to user interactions, with minimal custom JavaScript. MongoDB provides document storage via the **Beanie ODM**, running in Docker alongside the app. Styling uses Tailwind CSS + DaisyUI as provided by vibetuner.

### 1.1 Architecture Style

**Server-side rendering with HTMX partial updates.** This means:

- Pages are rendered as Jinja2 HTML templates on the server
- User interactions trigger HTMX requests (`hx-post`, `hx-get`, etc.) that return HTML fragments
- The browser swaps the returned fragments into the DOM without a full page reload
- JavaScript is used only where HTMX alone cannot achieve the required behaviour (e.g., tree expand/collapse state, mobile keyboard handling)

This approach was chosen to keep the codebase simple and the client thin — appropriate for a solo personal tool where development velocity and maintainability matter more than SPA-style interactivity.

### 1.2 High-Level Component Diagram

```text
┌─────────────────────────────────────────────────────┐
│                     Browser                         │
│                                                     │
│  ┌─────────────────┐   ┌────────────────────────┐  │
│  │   Chat Panel    │   │   Tree / Detail View   │  │
│  │  (HTMX + SSE)   │   │   (HTMX partials)      │  │
│  └────────┬────────┘   └───────────┬────────────┘  │
└───────────┼────────────────────────┼────────────────┘
            │ HTTP / SSE             │ HTTP
            ▼                        ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Application                    │
│                                                     │
│  ┌──────────────┐  ┌────────────┐  ┌─────────────┐ │
│  │ Chat Router  │  │ Entity     │  │  Tree       │ │
│  │ + LLM        │  │ Routers    │  │  Router     │ │
│  │ Orchestrator │  │ (CRUD)     │  │             │ │
│  └──────┬───────┘  └─────┬──────┘  └──────┬──────┘ │
│         │                │                │        │
│  ┌──────▼────────────────▼────────────────▼──────┐ │
│  │              Service Layer                    │ │
│  │  (OpportunityService, SolutionService, …)     │ │
│  └──────────────────────┬────────────────────────┘ │
│                         │                          │
│  ┌──────────────────────▼────────────────────────┐ │
│  │            Beanie ODM                         │ │
│  │  (Document models with async MongoDB access)  │ │
│  └──────────────────────┬────────────────────────┘ │
└─────────────────────────┼───────────────────────────┘
                          │
            ┌─────────────▼─────────────┐
            │   MongoDB (Docker)        │
            │   Collections per entity  │
            └───────────────────────────┘

┌─────────────────────────────────────────────────────┐
│          Ollama (Docker, local network)             │
│  OpenAI-compatible API at http://ollama:11434       │
│  Future: swap/add hosted providers (Anthropic, etc) │
└─────────────────────────────────────────────────────┘
```

---

## 2. Project Structure

The project follows the vibetuner scaffolding layout. Application code lives under `src/app/`; the `vibetuner` package (installed as a dependency) provides the framework core — auth, database init, auto-discovery, and more.

```text
opportunity-tracker/
├── compose.yml                 # Docker Compose (vibetuner convention)
├── Dockerfile
├── .env.example
├── pyproject.toml              # uv-managed dependencies
├── justfile                    # Task runner (just dev, just test, etc.)
├── README.md
├── ARCHITECTURE.md
├── PRD.md
├── AGENTS.md
│
├── src/app/                    # All application code lives here
│   ├── config.py               # App settings (extends vibetuner base config)
│   │
│   ├── models/                 # Beanie Document models (auto-discovered)
│   │   ├── opportunity.py
│   │   ├── solution.py
│   │   ├── assumption.py
│   │   ├── test.py
│   │   ├── result.py
│   │   ├── tag.py
│   │   └── chat_session.py     # Chat session and message models
│   │
│   ├── services/               # Business logic; calls Beanie models directly
│   │   ├── opportunity.py
│   │   ├── solution.py
│   │   ├── assumption.py
│   │   ├── test.py
│   │   ├── result.py
│   │   └── tag.py
│   │
│   ├── llm/                    # LLM orchestration layer
│   │   ├── client.py           # Anthropic API wrapper, retry/fallback logic
│   │   ├── orchestrator.py     # Conversation state machine and flow routing
│   │   ├── prompts.py          # System prompts and prompt templates
│   │   ├── flows/              # One file per guided conversation flow
│   │   │   ├── opportunity.py
│   │   │   ├── solution.py
│   │   │   ├── assumption.py
│   │   │   ├── test.py
│   │   │   └── result.py
│   │   └── suggestions.py      # Post-save AI insight generation
│   │
│   └── frontend/
│       └── routes/             # FastAPI routers (auto-discovered by vibetuner)
│           ├── pages.py        # Full-page renders (GET /, GET /tags, etc.)
│           ├── chat.py         # Chat endpoints (POST /chat/message, SSE)
│           ├── tree.py         # Tree partial renders
│           ├── opportunity.py  # CRUD partials
│           ├── solution.py
│           ├── assumption.py
│           ├── test.py
│           ├── result.py
│           └── tag.py
│
├── templates/                  # Jinja2 HTML templates (vibetuner convention)
│   └── frontend/
│       ├── base.html           # Root layout (extends vibetuner base)
│       ├── index.html          # Main two-panel layout
│       └── partials/
│           ├── chat/
│           │   ├── message.html          # Single chat bubble
│           │   ├── insight.html          # AI suggestion bubble
│           │   └── preview.html          # Record preview before save
│           ├── tree/
│           │   ├── node.html             # Recursive tree node
│           │   ├── detail_panel.html     # Entity detail slide-in
│           │   └── mobile_list.html      # Simplified mobile list view
│           └── entities/
│               ├── opportunity_detail.html
│               ├── solution_detail.html
│               ├── assumption_detail.html
│               ├── test_detail.html
│               └── result_detail.html
│
├── assets/statics/             # Static files (CSS overrides, JS snippets)
│
└── tests/
    ├── conftest.py             # Pytest fixtures (vibetuner test helpers + app)
    ├── unit/
    │   ├── test_models.py
    │   ├── test_services.py
    │   └── test_llm_flows.py
    └── integration/
        ├── test_api_opportunities.py
        ├── test_api_solutions.py
        ├── test_api_assumptions.py
        ├── test_api_tests.py
        ├── test_api_results.py
        └── test_api_chat.py
```

---

## 3. Data Layer

### 3.1 MongoDB Collections

One collection per entity type, managed by Beanie. Beanie uses `PydanticObjectId` as the `id` field, automatically mapping MongoDB's `_id`. Parent references are stored as `PydanticObjectId` fields on child documents.

| Collection | Key Fields | Indexes |
|------------|-----------|---------|
| `opportunities` | `title`, `status`, `tags`, `archived` | `status`, `tags`, `archived`, text index on `title`+`description` |
| `solutions` | `opportunity_id`, `status`, `tags`, `archived` | `opportunity_id`, `status`, `archived` |
| `assumptions` | `solution_id`, `status`, `importance`, `confidence`, `tags`, `archived` | `solution_id`, `status`, `archived` |
| `tests` | `assumption_id`, `status`, `tags`, `archived` | `assumption_id`, `status`, `archived` |
| `results` | `test_id`, `outcome`, `tags`, `archived` | `test_id`, `outcome`, `archived` |
| `tags` | `name`, `color` | unique index on `name` |
| `chat_sessions` | `created_at`, `flow_type`, `flow_state` | `created_at` |

### 3.2 Beanie Document Models

All documents extend a shared `BaseDocument` class that provides common fields. Beanie handles collection registration, index creation, and async CRUD operations.

```python
# src/app/models/base.py
from beanie import Document
from datetime import datetime
from pydantic import Field

class BaseDocument(Document):
    archived: bool = False
    tags: list[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        use_revision = False  # override per model if needed
```

Each entity model extends `BaseDocument` and declares its own fields, collection name, and indexes via the inner `Settings` class:

```python
# src/app/models/opportunity.py (illustrative)
from beanie import Document, Indexed
from pydantic import Field
from .base import BaseDocument

class Opportunity(BaseDocument):
    title: str
    description: str
    who: str | None = None
    context: str | None = None
    desired_outcome: str | None = None
    current_approach: str | None = None
    pain_points: str | None = None
    frequency: str | None = None
    impact: str | None = None
    prior_attempts: str | None = None
    constraints: str | None = None
    open_questions: str | None = None
    status: str = "open"

    class Settings:
        name = "opportunities"
        indexes = ["status", "tags", "archived"]
```

Beanie models are **auto-discovered** by vibetuner at startup — any `Document` subclass in `src/app/models/` is registered automatically. No manual registration is needed.

### 3.3 Querying Patterns

Services call Beanie's async API directly. Common patterns:

```python
# Fetch with filter
opportunities = await Opportunity.find(
    Opportunity.archived == False,
    Opportunity.status == status
).to_list()

# Fetch single with children
solution = await Solution.get(solution_id)
assumptions = await Assumption.find(
    Assumption.solution_id == solution.id,
    Assumption.archived == False
).to_list()

# Update
await opportunity.set({Opportunity.status: "validated", Opportunity.updated_at: datetime.utcnow()})

# Soft delete
await entity.set({BaseDocument.archived: True, BaseDocument.updated_at: datetime.utcnow()})
```

---

## 4. API Layer

### 4.1 Route Conventions

All routes follow a consistent pattern and are **auto-discovered** by vibetuner from `src/app/frontend/routes/`:

- **Full-page routes** (`GET /`, `GET /tags`) — return complete HTML pages
- **HTMX partial routes** (`GET /tree`, `POST /chat/message`) — return HTML fragments for DOM swapping
- **JSON API routes** (`GET /api/v1/opportunities`) — return JSON; used for internal tooling and future extensibility

HTMX routes detect whether the request is from HTMX (`HX-Request` header) and return a partial or full page accordingly.

### 4.2 Route Index

#### Pages

| Method | Path | Returns | Description |
|--------|------|---------|-------------|
| GET | `/` | Full page | Main two-panel layout (chat + tree) |
| GET | `/tags` | Full page | Tag management screen |

#### Chat

| Method | Path | Returns | Description |
|--------|------|---------|-------------|
| POST | `/chat/message` | HTML partial | Send a message; returns assistant reply bubble(s) |
| GET | `/chat/stream/{session_id}` | SSE stream | Stream LLM tokens to chat panel |
| POST | `/chat/session` | HTML partial | Start a new chat session (resets context) |
| GET | `/chat/history/{session_id}` | HTML partial | Re-render chat history |

#### Tree

| Method | Path | Returns | Description |
|--------|------|---------|-------------|
| GET | `/tree` | HTML partial | Full tree (all opportunities, collapsed by default) |
| GET | `/tree/node/{entity_type}/{id}` | HTML partial | Single node with its children |
| GET | `/tree/detail/{entity_type}/{id}` | HTML partial | Detail panel for a node |

#### Opportunities

| Method | Path | Returns | Description |
|--------|------|---------|-------------|
| GET | `/api/v1/opportunities` | JSON | List all (supports `?status=`, `?tag=`, `?archived=`) |
| POST | `/api/v1/opportunities` | JSON | Create |
| GET | `/api/v1/opportunities/{id}` | JSON | Get one |
| PATCH | `/api/v1/opportunities/{id}` | JSON | Update fields |
| DELETE | `/api/v1/opportunities/{id}` | JSON | Soft delete |

*Same pattern for `/solutions`, `/assumptions`, `/tests`, `/results`.*

#### Tags

| Method | Path | Returns | Description |
|--------|------|---------|-------------|
| GET | `/api/v1/tags` | JSON | List all tags |
| POST | `/api/v1/tags` | JSON | Create tag |
| PATCH | `/api/v1/tags/{id}` | JSON | Update name/color |
| DELETE | `/api/v1/tags/{id}` | JSON | Delete tag |

### 4.3 Request / Response Models

Pydantic models are used for API input validation and output serialisation. Because Beanie `Document` models serve as the DB layer, only two additional model variants are needed per entity (rather than three):

- `{Entity}Create` — fields accepted on POST (no `id`, `created_at`, `updated_at`); used for input validation before creating a Beanie document
- `{Entity}Response` — full outbound shape derived from the Beanie model (includes `id` as string, timestamps)

`PATCH` operations accept a dict of partial updates directly and call Beanie's `.set()` method.

---

## 5. LLM Orchestration Layer

### 5.1 Overview

The LLM layer sits between the chat router and the service layer. It manages multi-turn conversation state, constructs prompts, calls the configured LLM provider, parses structured output, and triggers post-save suggestion generation.

**Provider abstraction.** The LLM client (`src/app/llm/client.py`) presents a single interface regardless of which backend is in use. The active provider is selected at startup via `LLM_PROVIDER` in `.env`. Currently supported:

| Provider | Value | Notes |
|----------|-------|-------|
| Ollama (local Docker) | `ollama` | **Default.** OpenAI-compatible API at `http://ollama:11434` |
| Anthropic Claude | `anthropic` | Future; requires `LLM_API_KEY` |

The Ollama OpenAI-compatible endpoint (`/v1/chat/completions`) means the client can use the `openai` Python SDK pointed at the local Ollama host, making the future switch to a hosted provider a configuration change rather than a code change.

### 5.2 Conversation State Machine

Each active chat session has a `flow_type` and a `flow_state`. The orchestrator routes incoming messages based on these values and advances state after each LLM response.

```text
States for "create opportunity" flow:

  start
    ↓ LLM asks opening question
  collecting_description
    ↓ user replies; LLM extracts fields, asks next analyst Q
  collecting_analyst_qa       ←──┐
    ↓ all priority fields done  │ loop until sufficient
  collecting_tags               │
    ↓                           │
  preview                     (LLM may loop back here)
    ↓ user confirms
  saving
    ↓ record saved
  complete → trigger suggestions
```

Similar state machines exist for each flow type (`create_solution`, `create_assumption`, `create_test`, `log_result`, `update_{entity}`).

### 5.3 Prompt Architecture

Prompts are assembled from three layers:

1. **System prompt** — establishes the assistant's role, app context, output format rules, and the full current entity hierarchy for the active session (injected as JSON context)
2. **Flow prompt** — per-flow instructions: what fields to collect, how to prioritise Q&A, how to detect implicit field values
3. **Conversation history** — the full message array for the current session

The LLM is instructed to always return a structured JSON envelope alongside its user-facing reply:

```json
{
  "reply": "The conversational message shown to the user",
  "extracted_fields": { "field_name": "value", ... },
  "next_state": "collecting_analyst_qa | preview | complete",
  "suggestion": null
}
```

The orchestrator strips the JSON envelope before sending `reply` to the browser.

**Why JSON-in-reply rather than tool/function calling?** Tool calling is not consistently supported across all local Ollama models. Using a JSON envelope in the reply text works with any instruction-tuned model and keeps prompts portable across Ollama and future hosted providers. If the JSON envelope cannot be parsed, the orchestrator falls back to treating the entire reply as the user-facing message and does not advance state.

**Model selection.** The `LLM_MODEL` env var controls which model Ollama serves. A capable instruction-tuned model is required for reliable JSON extraction — recommended starting point: `llama3.1:8b` or `mistral:7b-instruct`. Larger models (`llama3.1:70b`) will produce better structured extraction at the cost of latency.

### 5.4 Fallback Behaviour

If the LLM is unavailable or returns an error (e.g., Ollama container is down, model not pulled, JSON parse failure):

- The chat router catches the exception
- The session falls back to rule-based prompts (a static question sequence per flow)
- A banner is shown in the chat panel: "AI features unavailable — using basic mode"
- Suggestions are silently skipped

On startup, the app checks Ollama reachability via `GET http://ollama:11434/api/tags` and logs a warning if unreachable, but does not block startup.

### 5.5 Suggestion Generation

After a successful save, the orchestrator asynchronously calls `suggestions.py` with:

- The newly saved entity
- Its parent chain (fetched from the DB)
- The suggestion type (e.g., `post_solution_save`, `post_result_save`)

The suggestions module calls the LLM with a targeted prompt and appends any returned insight as an "Insight" message in the chat session.

---

## 6. Frontend Layer

### 6.1 HTMX Interaction Patterns

| Interaction | HTMX trigger | Target | Server returns |
|-------------|-------------|--------|----------------|
| Send chat message | `hx-post="/chat/message"` | `#chat-messages` | New message bubble(s) appended |
| Expand tree node | `hx-get="/tree/node/{type}/{id}"` | node's child container | Children HTML |
| Click tree node | `hx-get="/tree/detail/{type}/{id}"` | `#detail-panel` | Detail panel HTML |
| Edit entity | button inside detail panel triggers chat flow | `#chat-messages` | Opening chat message |
| Filter tree | `hx-get="/tree?status=..."` on filter change | `#tree-container` | Filtered tree HTML |

### 6.2 LLM Streaming (SSE)

LLM responses stream token-by-token to the chat panel using Server-Sent Events. Ollama's OpenAI-compatible streaming endpoint is used:

1. `POST /chat/message` is received; the orchestrator starts an async streaming LLM call
2. The server responds immediately with an HTML partial containing an empty assistant bubble and an HTMX SSE listener pointing at `/chat/stream/{session_id}`
3. As tokens arrive from Ollama (or any configured provider), the SSE endpoint pushes them; HTMX appends them into the bubble
4. On stream completion, the server sends a final SSE event with the structured JSON envelope; the client triggers a follow-up HTMX request to fetch any extracted fields or updated tree state

### 6.3 JavaScript Usage

JavaScript is kept to a minimum. The following behaviours require small Alpine.js or vanilla JS snippets:

- **Tree node expand/collapse state** — persisted in `sessionStorage` so state survives HTMX swaps
- **Mobile chat input positioning** — `visualViewport` resize listener to keep input above keyboard
- **Chat auto-scroll** — scroll `#chat-messages` to bottom after each new message
- **SSE stream handling** — HTMX's built-in SSE extension handles this; no custom JS needed

Alpine.js (loaded from CDN) is used for local UI state (e.g., tag color picker open/closed).

### 6.4 Responsive Layout

Two layouts are defined in CSS using **Tailwind CSS + DaisyUI** (vibetuner's default styling stack, compiled via bun):

**Desktop (≥ 768px):** Two-column split — tree on left (35%), chat on right (65%).

**Mobile (< 768px):** Single column, bottom-tab navigation switching between chat and list views. Chat input fixed to bottom of viewport.

---

## 7. Infrastructure

### 7.1 Docker Compose

vibetuner uses `compose.yml` (not `docker-compose.yml`) as the filename convention.

The Ollama container is assumed to already be running as a separate Docker service on the local machine (not managed by this project's `compose.yml`). The app connects to it over the Docker network by hostname.

```yaml
# compose.yml (illustrative — align with vibetuner generated file)
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - mongo
    volumes:
      - ./src:/app/src   # hot reload in dev
    extra_hosts:
      - "host.docker.internal:host-gateway"  # reach host if Ollama runs there

  mongo:
    image: mongo:7
    volumes:
      - mongo_data:/data/db
    ports:
      - "27017:27017"    # exposed for local tooling; omit in prod

  mongo-express:
    image: mongo-express
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_SERVER: mongo
    depends_on:
      - mongo
    profiles: ["dev"]    # only starts with: docker compose --profile dev up

volumes:
  mongo_data:
```

> **Ollama connectivity:** If Ollama runs as a named container on the same Docker network, set `LLM_BASE_URL=http://ollama:11434`. If it runs directly on the host (outside Docker), use `LLM_BASE_URL=http://host.docker.internal:11434`.

### 7.2 Environment Variables

Defined in `.env` (never committed; `.env.example` is committed). Variable names follow vibetuner conventions where they overlap:

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGODB_URL` | `mongodb://mongo:27017/opportunity_tracker` | Full MongoDB connection string (vibetuner convention) |
| `LLM_PROVIDER` | `ollama` | Active LLM provider: `ollama` or `anthropic` |
| `LLM_BASE_URL` | `http://ollama:11434` | Ollama base URL (ignored when provider is `anthropic`) |
| `LLM_MODEL` | `llama3.1:8b` | Model name served by Ollama (or Anthropic model ID when using that provider) |
| `LLM_MAX_TOKENS` | `1024` | Max tokens per LLM response |
| `LLM_API_KEY` | *(optional)* | Required only when `LLM_PROVIDER=anthropic` |
| `APP_ENV` | `development` | `development` or `production` |
| `SECRET_KEY` | *(required)* | App secret key (vibetuner session signing) |

### 7.3 Dockerfile

vibetuner uses **uv** for dependency management and **Granian** as the ASGI server (replacing uvicorn). The generated Dockerfile follows a multi-stage pattern:

```dockerfile
# Align with the vibetuner-generated Dockerfile; key differences from vanilla FastAPI:
# - uv for dependency installation (fast, lockfile-based)
# - granian as the ASGI server (higher performance than uvicorn)
# - src/ layout with proper PYTHONPATH

FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen
COPY . .
CMD ["uv", "run", "granian", "--interface", "asgi", "src.app:create_app", "--host", "0.0.0.0", "--port", "8000"]
```

> Always defer to the vibetuner-generated `Dockerfile` as the source of truth. The above is illustrative.

---

## 8. Testing Strategy

Tests are written with **pytest** and **pytest-asyncio**. vibetuner provides built-in test fixtures for mock auth and a temporary test database. The test database is a separate MongoDB instance that is initialised and torn down per test session.

### 8.1 Test Layers

**Unit tests** (`tests/unit/`) test individual functions in isolation:

- Beanie model validation and field defaults
- Service layer logic (Beanie calls mocked with `unittest.mock`)
- LLM flow prompt assembly and field extraction logic (LLM calls mocked)

**Integration tests** (`tests/integration/`) test the full request/response cycle:

- Each router is tested against a real (test) MongoDB instance using vibetuner's temp DB fixture
- LLM calls are mocked at the `client.py` level with pre-canned responses
- Tests assert on HTTP status, returned HTML content, and database state

### 8.2 Test Fixtures

```python
# tests/conftest.py (key fixtures)
# vibetuner provides: mock_auth, temp_db, async_client
# App-specific additions:

@pytest.fixture
def mock_llm():
    """Patches LLMClient.complete() to return a canned JSON response."""

@pytest.fixture
async def sample_opportunity(temp_db):
    """Creates and yields a test Opportunity document; cleans up after."""
```

### 8.3 Test Naming Convention

Tests follow the pattern `test_{action}_{entity}_{condition}`:

- `test_create_opportunity_success`
- `test_create_opportunity_missing_title_returns_422`
- `test_soft_delete_opportunity_hides_from_tree`

---

## 9. Key Design Decisions

### 9.1 Why HTMX over a SPA framework?

This is a solo personal tool. HTMX keeps the stack thin — there is no separate frontend build process, no JSON API contract to maintain between a React app and a FastAPI backend, and no JavaScript framework to upgrade. The tree view's interactivity requirements (expand/collapse, filter, detail panel) are well within HTMX's capabilities.

### 9.2 Why Beanie ODM?

Beanie is vibetuner's native MongoDB integration and the right choice here for two reasons. First, it eliminates the need for a separate repository layer — Beanie `Document` models are themselves the data access objects, providing async CRUD, query building, and index management in one place. Second, staying with the vibetuner-provided stack minimises deviation from the scaffold, keeping future `vibetuner scaffold update` runs clean. The slightly reduced query-level control compared to raw Motor is an acceptable trade-off given the straightforward data access patterns in this app.

### 9.3 Why store chat sessions in MongoDB?

Persisting chat sessions allows the user to close the browser and resume a conversation in progress. It also gives the LLM full access to conversation history without relying on client-side state, which is important for HTMX's stateless partial rendering model.

### 9.4 Why Ollama first, with a provider abstraction?

Running LLM inference locally via Ollama has two key advantages for a personal tool: no per-token cost and no data leaving the machine. The trade-off is lower quality output from smaller models compared to frontier hosted models.

The `LLMClient` abstraction means this is not a permanent commitment — switching to Anthropic or another hosted provider at a later stage is a single env var change (`LLM_PROVIDER=anthropic`) with no changes to orchestration or flow logic. Using Ollama's OpenAI-compatible API endpoint as the initial implementation further reduces future migration effort, since the same `openai` SDK call works against both Ollama and OpenAI-compatible hosted providers.

---

## 10. Open Questions

| # | Question | Impact |
|---|----------|--------|
| 1 | Should the tree be rendered server-side (full re-render on filter) or should filter state be managed client-side with Alpine.js hiding/showing nodes? | Performance vs. simplicity |
| 2 | Should chat sessions expire after a period of inactivity, or persist indefinitely? | Storage growth over time |
| 3 | Which Ollama model to use as the default? `llama3.1:8b` is fast; `llama3.1:70b` or `mistral-small` will produce better JSON extraction at higher latency. | Output quality vs. response speed |
| 4 | Should `data` field on Result support structured JSON input (e.g., key-value metrics), or remain freeform string? | Complexity vs. future analytics |
| 5 | Is the Ollama container on the same Docker network as the app, or running on the host? Determines whether `LLM_BASE_URL` uses `http://ollama:11434` or `http://host.docker.internal:11434`. | Infrastructure config |

---

## 11. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-03-06 | Initial draft |
| 0.2.0 | 2026-03-06 | Aligned with vibetuner framework: Beanie ODM replaces Motor + repository layer; project structure updated to `src/app/` layout; Granian replaces uvicorn; uv for dependency management; `compose.yml` filename; `MONGODB_URL` env var; DaisyUI noted; test fixtures updated |
| 0.3.0 | 2026-03-06 | LLM backend changed to Ollama (local Docker) as primary provider; added provider abstraction (`LLM_PROVIDER`, `LLM_BASE_URL`); Anthropic documented as future option; model selection guidance added; Ollama startup health check noted; Open Question 5 added for network topology |
