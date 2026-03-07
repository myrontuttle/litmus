# Product Requirements Document (PRD)

## Opportunity Tracker

**Version:** 0.2.0
**Status:** Draft
**Author:** Solo / Personal
**Stack:** Python FastAPI · MongoDB (Docker) · HTMX
**Last Updated:** 2026-03-06

---

## 1. Purpose & Vision

Litmus is a personal tool for systematically capturing, exploring, and validating ideas. It operationalises the **Lean Startup / Build-Measure-Learn** loop at the level of individual opportunities — turning vague needs and desires into structured hypotheses, tests, and evidence.

The app acts as an AI-powered intelligent notebook: an LLM-driven conversational interface helps the user articulate and analyse thoughts quickly, while a hierarchical tree view lets them navigate relationships and see the bigger picture at a glance. The AI layer proactively surfaces suggestions — such as missing assumptions, untested risks, or patterns across opportunities — to deepen the user's thinking over time.

---

## 2. Problem Statement

When exploring new ideas, the user currently loses track of:

- What problem they were originally trying to solve
- Which solutions have already been considered (and discarded, and why)
- What assumptions underpin each solution
- Which assumptions have been tested, and what the outcomes were

The result is repeated thinking, forgotten insights, and decisions made without evidence. This app provides a single, structured home for the full opportunity-to-evidence chain — with an AI layer that actively helps the user think more rigorously.

---

## 3. Users & Context

| Attribute | Detail |
|-----------|--------|
| Primary user | Single person (the owner/developer) |
| Usage pattern | Irregular, burst-mode — capturing ideas when they arise, reviewing during planning sessions |
| Access | Local or self-hosted web app (Docker); no auth required initially |
| Data sensitivity | Personal/private; no sharing features needed in v1 |
| Devices | Desktop primary; mobile-optimised for quick capture on the go |

---

## 4. Core Concepts & Data Model

The app tracks a hierarchy of entities. Each level belongs to the one above it.

```text
Opportunity
└── Solution (one or more per Opportunity)
    └── Assumption (one or more per Solution)
        └── Test (one or more per Assumption)
            └── Result (one or more per Test)
```

Tags / Categories can be applied to any entity at any level.

### 4.1 Entity Definitions

#### Opportunity

A need, desire, pain point, or gap that is worth exploring. It is the root of every chain. Beyond a basic description, the Opportunity entity captures a structured analyst Q&A to ensure the opportunity is well-understood before solutions are proposed.

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | Auto-generated |
| `title` | string | Short label, ≤ 120 chars |
| `description` | string | Freeform narrative of the need or desire |
| `who` | string | Who experiences this need or desire? (person, role, or group) |
| `context` | string | In what situation or context does this need arise? |
| `desired_outcome` | string | What does success look like for the person experiencing it? |
| `current_approach` | string | How is the need being addressed today, if at all? |
| `pain_points` | string | What is frustrating or insufficient about the current approach? |
| `frequency` | string | How often does this need arise? (e.g., daily, occasionally, at a specific trigger) |
| `impact` | string | What is the consequence if the need goes unmet? |
| `prior_attempts` | string | Have solutions been tried before? What happened? |
| `constraints` | string | Are there known constraints a solution must work within? (time, cost, tech, etc.) |
| `open_questions` | string | What is still unknown or unclear about this opportunity? |
| `status` | enum | `open` · `in_progress` · `validated` · `invalidated` · `parked` |
| `tags` | string[] | Refs to Tag entities |
| `created_at` | datetime | |
| `updated_at` | datetime | |

> **Note:** Analyst Q&A fields are optional individually, but the chat flow will prompt for each. The LLM prioritises which fields to ask about based on what has already been shared and what gaps remain.

#### Solution

A proposed approach that could address an Opportunity.

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | |
| `opportunity_id` | UUID | Parent |
| `title` | string | |
| `description` | string | How this solution addresses the opportunity |
| `status` | enum | `proposed` · `active` · `validated` · `invalidated` · `parked` |
| `tags` | string[] | |
| `created_at` / `updated_at` | datetime | |

#### Assumption

A belief that must be true for a Solution to work. Assumptions are the units of risk.

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | |
| `solution_id` | UUID | Parent |
| `statement` | string | Stated as a falsifiable belief, e.g. "Users will pay ≥ $10/mo" |
| `importance` | enum | `critical` · `major` · `minor` |
| `confidence` | enum | `low` · `medium` · `high` |
| `status` | enum | `untested` · `testing` · `supported` · `refuted` · `moot` |
| `tags` | string[] | |
| `created_at` / `updated_at` | datetime | |

#### Test

A single planned or executed investigation of an Assumption. Tests attach directly to Assumptions with no intermediate grouping layer.

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | |
| `assumption_id` | UUID | Parent |
| `title` | string | |
| `hypothesis` | string | "We believe that … [measurable outcome] … because …" |
| `method` | string | How the test will be or was run |
| `success_criteria` | string | What result would support the assumption |
| `description` | string | What was actually done (filled in on completion) |
| `date_run` | date | |
| `status` | enum | `planned` · `running` · `completed` · `abandoned` |
| `tags` | string[] | |
| `created_at` / `updated_at` | datetime | |

#### Result

The outcome of a Test — observations, data, and interpretation.

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | |
| `test_id` | UUID | Parent |
| `summary` | string | What happened |
| `data` | string / JSON | Raw observations or metrics |
| `interpretation` | string | What this means for the assumption |
| `outcome` | enum | `supports` · `refutes` · `inconclusive` |
| `tags` | string[] | |
| `created_at` / `updated_at` | datetime | |

#### Tag / Category

A label that can be applied to any entity for cross-cutting navigation.

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | |
| `name` | string | Unique, slugified |
| `color` | string | Hex color for UI display |
| `created_at` | datetime | |

---

## 5. Feature Requirements

### 5.1 Chat Interface (Primary Input)

The chat panel is the primary way to create and update records. It is powered by an LLM that interprets natural language responses, maps them to structured fields, asks intelligent follow-ups, and proactively surfaces suggestions.

**FR-CHAT-01** — On load, the chat panel shows a context-aware greeting and a menu of actions: "Capture a new opportunity", "Add a solution", "Log a test result", etc.

**FR-CHAT-02** — When the user selects an action, the LLM runs a short guided conversation collecting the required fields for the target entity. The LLM adapts follow-up questions based on prior answers rather than following a rigid script.

**FR-CHAT-03** — The LLM parses each user response and maps it to the appropriate field(s). Where a single response contains information for multiple fields, it extracts them all. Ambiguous answers surface a clarifying follow-up.

**FR-CHAT-04** — At the end of a conversation flow, the system shows a structured preview of the record to be created and asks for confirmation before saving.

**FR-CHAT-05** — The user can say "go back" or "cancel" at any point to restart or abort the flow.

**FR-CHAT-06** — Saved records trigger a success message in chat with a link to the new record in the tree view.

**FR-CHAT-07** — The chat interface supports updating existing records: the user can say "update [entity]" and the system fetches the current values, presenting them for amendment.

**FR-CHAT-08** — For Opportunity capture, the LLM works through the analyst Q&A fields (§4.1), prioritising the most important questions given what has already been shared, and skipping fields that have been implicitly answered.

### 5.2 AI Suggestions

The LLM layer proactively analyses the user's data and surfaces actionable suggestions.

**FR-AI-01** — After saving a new Solution, the LLM suggests assumptions the user may not have considered, based on the opportunity context and solution description.

**FR-AI-02** — After saving a set of Assumptions, the LLM identifies which are highest-risk (high importance + low confidence) and recommends prioritising tests for those first.

**FR-AI-03** — After logging a Result, the LLM reflects on what the outcome means for the parent Assumption and Solution, and suggests whether to pivot, persevere, or abandon.

**FR-AI-04** — Periodically (or on request), the LLM surfaces cross-opportunity patterns: e.g., recurring assumptions across solutions, or opportunities with no recent activity.

**FR-AI-05** — AI suggestions are shown inline in the chat panel as distinct "Insight" messages, clearly labelled as AI-generated. The user can dismiss, act on, or save them.

**FR-AI-06** — The LLM has read access to the full data store so suggestions are grounded in actual records, not generic advice.

### 5.3 Tree / Hierarchy View (Navigation & Context)

The tree view provides a persistent spatial overview of all entities and their relationships.

**FR-TREE-01** — The tree renders the full Opportunity → Solution → Assumption → Test → Result hierarchy as a collapsible/expandable tree.

**FR-TREE-02** — Each node shows: title, status badge (color-coded), and tag chips.

**FR-TREE-03** — Clicking a node opens an inline detail panel showing all fields for that entity, including all analyst Q&A fields for Opportunities.

**FR-TREE-04** — The detail panel has an "Edit" button that launches the appropriate chat update flow.

**FR-TREE-05** — The tree supports filtering by: status, tag, entity type, and free-text search on title/description.

**FR-TREE-06** — The tree supports collapsing all children of a node to reduce visual noise.

**FR-TREE-07** — Status badges propagate upward as summary indicators: e.g., an Opportunity node shows how many of its Assumptions are `supported` vs `refuted`.

### 5.4 Tag Management

**FR-TAG-01** — Tags can be created inline during any chat flow or via a dedicated tag management screen.

**FR-TAG-02** — Tags are shown as colored chips on tree nodes and detail panels.

**FR-TAG-03** — Clicking a tag in any context filters the tree to show only entities with that tag.

### 5.5 Data Persistence

**FR-DATA-01** — All entities are persisted in MongoDB running in Docker (see §7).

**FR-DATA-02** — `created_at` and `updated_at` are set automatically by the backend.

**FR-DATA-03** — Soft-delete: entities are marked `archived: true` rather than physically deleted. Archived entities are hidden by default but can be revealed via a toggle.

**FR-DATA-04** — The API exposes full CRUD for all entity types.

---

## 6. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-01 | **Performance** — Tree view renders up to 500 nodes without perceptible lag |
| NFR-02 | **Responsiveness** — Fully usable on desktop (≥ 1280px) and mobile (≥ 375px); mobile optimised for quick capture via chat |
| NFR-03 | **Reliability** — No data loss on page refresh or navigation; all writes confirmed before UI updates |
| NFR-04 | **Maintainability** — Code follows consistent style, is covered by tests, and is documented for AI coding agents (see AGENTS.md) |
| NFR-05 | **Extensibility** — Data model and API designed so new entity types or fields can be added without breaking existing records |
| NFR-06 | **LLM resilience** — If the LLM API is unavailable, the app degrades gracefully: chat falls back to simple rule-based prompts, and AI suggestions are disabled with a clear status message |

---

## 7. Infrastructure & Hosting

The app runs entirely on the developer's local machine or a self-hosted server via Docker Compose.

**Docker Compose services:**

- `app` — FastAPI application server
- `mongo` — MongoDB instance with a named volume for data persistence
- `mongo-express` *(optional dev tool)* — Web UI for inspecting the database

**Environment configuration** (via `.env`):

- `MONGO_URI` — MongoDB connection string (default: `mongodb://mongo:27017`)
- `LLM_API_KEY` — API key for the LLM provider (e.g., Anthropic)
- `LLM_MODEL` — Model identifier (e.g., `claude-sonnet-4-20250514`)

**FR-INFRA-01** — A single `docker compose up` command starts the full stack from a cold state.

**FR-INFRA-02** — MongoDB data is persisted in a named Docker volume; it survives container restarts.

**FR-INFRA-03** — The app is accessible at `http://localhost:8000` by default.

---

## 8. Mobile Experience

Mobile is optimised for **capture** (quick input via chat) rather than full tree navigation.

**FR-MOB-01** — On narrow viewports (< 768px), the chat panel occupies the full screen by default.

**FR-MOB-02** — The tree view is accessible on mobile via a bottom navigation tab, but renders as a simplified list rather than a full tree.

**FR-MOB-03** — All interactive targets (buttons, inputs, node taps) meet minimum touch target size (44×44px).

**FR-MOB-04** — The chat input box is fixed to the bottom of the viewport on mobile, above the system keyboard.

**FR-MOB-05** — The app works as a mobile web app in the browser; no native app install required.

---

## 9. User Flows

### 9.1 Capture a New Opportunity

1. User opens app → chat panel loads
2. User selects "Capture a new opportunity"
3. LLM asks an opening question: *"What's the need or desire you've noticed?"* → seeds `description`
4. LLM follows up with analyst Q&A questions (§4.1), adapting based on what has already been shared
5. LLM asks: *"Any tags? (optional)"* → maps to `tags`
6. System shows structured preview → user confirms → record saved
7. Tree view updates; new Opportunity node highlighted
8. LLM may surface an initial suggestion: e.g., *"You haven't described the current approach yet — want to add that?"*

### 9.2 Add Solutions to an Opportunity

1. User clicks an Opportunity node in the tree → detail panel opens
2. User clicks "Recommend Solutions" or initiates via chat
3. LLM recommends 3-5 solutions with `title` and `description` to potentially resolve the opportunity
4. LLM asks to select solutions to investigate and or add more user-provided solutions with `title` and `description`
5. Preview → confirm → save → tree updates
6. LLM suggests initial assumptions to consider for each solution

### 9.3 Log a Test Result

1. User navigates to a Test node in the tree (or initiates via chat)
2. User clicks "Log Result"
3. LLM asks: *"What did you observe?"* → `summary`
4. LLM asks: *"Any raw data or metrics?"* → `data` (optional)
5. LLM asks: *"What does this mean for the assumption?"* → `interpretation`
6. LLM asks: *"Does this support, refute, or leave the assumption inconclusive?"* → `outcome`
7. Preview → confirm → save → parent Assumption `confidence` and `status` updated
8. LLM reflects on the result and suggests next steps

---

## 10. Success Metrics (Personal)

Since this is a solo tool, success is qualitative:

- The user captures opportunities without friction — a new record in < 2 minutes
- No ideas are lost because the input felt too heavy
- The tree view provides genuine "at a glance" understanding of where each idea stands
- The user references the app when making decisions, rather than relying on memory
- AI suggestions feel genuinely useful, not generic or noisy

---

## 11. Open Questions

| # | Question | Owner | Due |
|---|----------|-------|-----|
| 1 | Should status transitions be enforced (state machine) or free-form? | Owner | Before data model implementation |
| 2 | Should AI suggestions be generated eagerly (after every save) or lazily (on request)? | Owner | Before AI feature implementation |
| 3 | Should analyst Q&A fields on Opportunity be a fixed list or user-extensible? | Owner | Before Opportunity implementation |

---

## 12. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-03-06 | Initial draft |
| 0.2.0 | 2026-03-06 | Removed Experiment layer (Tests attach directly to Assumptions); added LLM-powered chat and AI suggestions (§5.1, §5.2); added Docker/local hosting section (§7); added mobile experience section (§8); expanded Opportunity entity with analyst Q&A fields; renamed CLAUDE.md → AGENTS.md throughout |
