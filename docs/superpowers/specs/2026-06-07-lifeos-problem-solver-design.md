# LifeOS — Personal Problem-Solving AI Agent

**Design spec** · 2026-06-07 · v1 (local-first MVP with a clean path to a hosted web app)

---

## 1. Purpose

A personal AI agent that helps me move **from confusion to clarity, and from clarity to action** on the real problems in my life. It uses:

- **Structured reasoning** (a fixed multi-step problem-solving process),
- **My personal knowledge base** (transcripts, books, notes, philosophy, psychology, etc.),
- **My past problem history** (to detect repeated patterns and learn what works),
- **Wisdom across many subjects of life** (Stoic + Indian philosophy, psychology, productivity, science).

Tone: calm, honest, direct, practical, supportive. No vague motivation, no flattery. It does not just explain problems — it helps me solve them.

### Guiding principle

> Build v1 as a **local-first Markdown LifeOS**, but treat **every file as a future database row, every command as a future API endpoint, and every tag/rating/status as future analytics data.**

The MVP runs inside Claude Code (Markdown + YAML + slash commands). It is structured from day one so it can later become a hosted, multi-feature **LifeOS web app** — a port, not a rewrite.

---

## 2. Scope

### In scope (v1)

A local-first system in this repo consisting of:

1. A **constitution** (`CLAUDE.md`) defining persona, tone, the problem-solving process, and safety rules.
2. A **controlled vocabulary** (`taxonomy.md`) — the spine of analytics.
3. A **strict data contract** (`SCHEMA.md`) every file must conform to, with validation from day one.
4. **Slash commands** for the 11 core actions, each behaving like a future API endpoint.
5. **Markdown data stores** for problems, knowledge, reflections, decisions, and systems, with structured YAML frontmatter.

### Out of scope (v1) — but designed for

Hosted web app, authentication, relational + vector database, file-upload/RAG pipelines, dashboards, calendar/reminder integration. These are described in §9 (Future Hosted Architecture) so the MVP data model and command surface map cleanly onto them.

### Command priority for the first build

Conceptually **none of the 11 actions are dropped**. Build order:

- **Must-have v1:** `/solve`, `/add-knowledge`, `/outcome`, `/analytics`, `/search`, `/ask`, `/actions`, `/export`
- **Included but lighter in v1:** `/decide`, `/reflect`, `/systems`

**Pattern-warning is not a user command.** It runs automatically inside `/solve`, `/reflect`, and `/decide` whenever a repeated pattern is detected.

---

## 3. Directory layout

```
AI Problem Solver/
├── CLAUDE.md            # Constitution: persona, tone, the problem-solving process, safety rules
├── README.md            # What this is + how to use it
├── SCHEMA.md            # The data contract — strict frontmatter schema per entity + validation rules
├── taxonomy.md          # Controlled vocabulary (the spine of analytics)
├── .claude/commands/    # One file per action (the 11 verbs)
│   ├── solve.md  add-knowledge.md  outcome.md  analytics.md
│   ├── search.md  ask.md  decide.md  reflect.md
│   ├── actions.md  systems.md  export.md
├── problems/            # PRB-*.md   (actions + outcomes live inline as child entities)
├── knowledge/           # KND-*.md
├── reflections/         # REF-*.md
├── decisions/           # DEC-*.md
├── systems/             # SYS-*.md
├── analytics/           # Generated snapshots (snapshot-YYYY-MM-DD.md)
└── exports/             # Generated JSON bundles (full data ownership)
```

**Source of truth = the YAML frontmatter in each file.** No separate database/index in v1 — analytics and search read across these files. This avoids sync bugs while the dataset is small, and the strict schema means a future migration script parses frontmatter → DB rows.

---

## 4. Stable ID scheme

IDs are readable, sortable, and **permanent once assigned** (they survive the DB migration unchanged and become primary keys).

| Entity | ID format | Example |
|---|---|---|
| Problem | `PRB-YYYYMMDD-NN` | `PRB-20260607-01` |
| Knowledge doc | `KND-YYYYMMDD-NN` | `KND-20260607-01` |
| Reflection | `REF-YYYYMMDD-NN` | `REF-20260607-01` |
| Decision | `DEC-YYYYMMDD-NN` | `DEC-20260607-01` |
| System | `SYS-YYYYMMDD-NN` | `SYS-20260607-01` |
| Action (child of problem) | `ACT-<problemID>-NN` | `ACT-PRB-20260607-01-01` |
| Outcome (child of problem) | `OUT-<problemID>-NN` | `OUT-PRB-20260607-01-01` |

- `NN` is a 2-digit daily sequence. A command computes it by listing same-day files of that type and incrementing (no randomness/timestamps required).
- Every cross-link (related problems, cited knowledge, spawned systems, people) is stored **by ID or controlled term** — these become foreign keys / join rows later.

---

## 5. The data contract (`SCHEMA.md`)

All entities share: `id`, `type`, `created`, `updated`, controlled-vocab classification fields, structured fields, and a human-readable Markdown body. Actions and outcomes are **child entities** of a problem — inline in v1 for readability, but modeled so they split cleanly into separate tables with a `problem_id` foreign key later.

### 5.1 Problem

`problems/PRB-20260607-01-overthinking-job-offer.md`

```yaml
---
id: PRB-20260607-01
type: problem
title: "Paralyzed deciding on the new job offer"
created: 2026-06-07
updated: 2026-06-07
status: open                 # open | in_progress | resolved | abandoned
subjects: [mind_and_psychology, career_and_work]   # from the 15 (taxonomy.md)
life_areas: [career_and_work]
problem_types: [decision_problem, emotional_problem]
deeper_issue: emotional      # the single dominant layer
emotions: [anxiety, self_doubt]
people: [manager]            # tracked for recurrence
tags: [overthinking, fear_of_failure]
ratings:
  urgency: 7
  importance: 8
  emotional_intensity: 6
  controllability: 5
  long_term_impact: 7
  recurrence_likelihood: 6
  effort_required: 5
root_cause: "Fear of an irreversible choice → avoidance via over-analysis"
related_problems: [PRB-20251101-02]   # repeated-pattern links
knowledge_refs: [KND-20260510-03]     # documents cited
systems: []                           # preventive systems spawned
actions:
  - id: ACT-PRB-20260607-01-01
    what: "List the 3 things you are actually afraid of"
    why: "Names the vague fear so it can be examined"
    when: 2026-06-08
    difficulty: easy          # easy | medium | hard
    expected_result: "Fear becomes concrete and smaller"
    status: not_started       # not_started | in_progress | completed | failed | postponed | not_relevant
    updated: 2026-06-07
outcomes: []                  # appended later by /outcome
immediate_next_action: "Write the 3 fears, 10 minutes tonight"
---

# (Body — human-readable analysis in the default output format, see §7)
```

### 5.2 Knowledge document

`knowledge/KND-20260607-01-seneca-on-anxiety.md`

```yaml
---
id: KND-20260607-01
type: knowledge
title: "Letters from a Stoic — on anxiety"
created: 2026-06-07
source_type: book            # youtube_transcript | book | article | pdf | personal_note | reflection
source: "Seneca, Letters from a Stoic, Letter XIII"
subjects: [philosophy_and_wisdom]      # can span multiple of the 15
subtopics: [stoicism, acceptance]
life_areas: [self_and_inner_life]
problem_types: [emotional_problem, identity_problem]
related_subjects: [mind_and_psychology]
tags: [control, fear, discipline]
---

# Key Ideas
# Practical Lessons
# Philosophical Lessons
# Emotional Lessons
# Possible Use Cases
# Summary
# Important Quotes or Concepts
```

### 5.3 Reflection

```yaml
---
id: REF-20260607-01
type: reflection
created: 2026-06-07
period: daily                # daily | weekly
mood: [tired, restless]      # controlled emotion vocab
subjects: [self_and_inner_life]
life_areas: [career_and_work, body_and_health]
detected_problems: [PRB-20260607-01]   # problems surfaced/created from this reflection
patterns_detected: [avoidance]
people: [manager]
---

# Journal entry + what the agent noticed (hidden problems, emotional patterns, unresolved issues)
```

### 5.4 Decision

```yaml
---
id: DEC-20260607-01
type: decision
title: "Accept offer vs. stay"
created: 2026-06-07
status: open                 # open | decided | reversed
options: ["Accept offer", "Stay in current role"]
chosen: null
related_problems: [PRB-20260607-01]
values_considered: [security, growth, autonomy]
subjects: [career_and_work, philosophy_and_wisdom]
life_areas: [career_and_work]
tags: [opportunity_cost, dharma]
---

# Comparison: pros/cons, risks, values, dharma/duty, long-term consequences, opportunity cost, emotional bias
```

### 5.5 System (preventive)

```yaml
---
id: SYS-20260607-01
type: system
title: "48-hour rule for big decisions"
created: 2026-06-07
status: active               # active | paused | retired
kind: rule                   # routine | rule | checklist | habit | boundary
prevents_problem_types: [decision_problem]
addresses_patterns: [overthinking]
source_problems: [PRB-20260607-01]   # which recurring problems triggered this
subjects: [systems_and_thinking]
life_areas: [career_and_work]
tags: [decision_making]
---

# The system: trigger, the rule/steps, how to follow it, how to review it
```

### 5.6 Validation rules (from day one)

Every command that writes a file **validates against `SCHEMA.md` before saving**:

- All **required fields** present and correctly typed.
- Every value in a **controlled field** (`subjects`, `life_areas`, `problem_types`, `emotions`, `status`, `difficulty`, etc.) exists in `taxonomy.md`. If a tag is outside the vocabulary, the agent either maps it to the closest valid term **or** proposes adding it to `taxonomy.md` as a deliberate edit — it never writes a silent off-vocabulary tag.
- All **ID references** (`related_problems`, `knowledge_refs`, `systems`, etc.) resolve to existing files.
- On any violation, the agent **warns and fixes** before writing. `SCHEMA.md` doubles as the validation checklist.

---

## 6. The controlled vocabulary (`taxonomy.md`)

The single most important file for making analytics work. Fixed enumerations so semantically identical tags never fragment (e.g. "fear" never splits into five synonyms).

**The 15 subjects of life:**

1. `self_and_inner_life`
2. `mind_and_psychology`
3. `body_and_health`
4. `relationships_and_people`
5. `career_and_work`
6. `money_and_resources`
7. `philosophy_and_wisdom`
8. `science_and_reality`
9. `society_and_civilization`
10. `practical_life_skills`
11. `creativity_and_expression`
12. `morality_ethics_and_character`
13. `life_stages_and_human_journey`
14. `problem_types`
15. `systems_and_thinking`

Plus controlled lists for: **life areas**, **problem types** (emotional, practical, decision, relationship, money, career, health, identity, discipline, moral, spiritual, crisis, repeated_pattern), **emotions**, **statuses** (problem / action / decision / system), and **difficulty** (easy/medium/hard).

`people` and free `tags` are not enumerated but **are tracked** (for recurrence analytics). Extending any controlled list is a deliberate edit to `taxonomy.md`, not something that happens silently mid-task.

---

## 7. Commands (each = future API endpoint + UI feature)

Every command shares `CLAUDE.md`: persona, tone, the problem-solving process, and the **safety rule** — the agent is not a substitute for a doctor, therapist, lawyer, or financial advisor; on serious mental-health, medical, legal, financial, or harm risk it clearly advises contacting a qualified professional or trusted person.

| Command | Action | Future web feature |
|---|---|---|
| `/solve` | Full problem-solving flow (§7.1). **Auto pattern-warning.** Suggests a system when recurrence is high. | "New Problem" |
| `/add-knowledge` | Classify a transcript/note/PDF/text into the knowledge schema and file it. | "Upload Knowledge" |
| `/outcome` | Append a structured outcome to a problem; update status & lessons. | "Record Outcome" |
| `/analytics` | Aggregate structured fields into an insights report; includes **review** of open/unresolved items. | "Insights Dashboard" |
| `/search` | Query past problems by category, emotion, person, life area, date, tag, outcome, or pattern. | "Problem History Search" |
| `/ask` | Q&A over `knowledge/` with source citations (RAG-style; v1 reads files). | "Ask Knowledge Base" |
| `/decide` | Compare options on pros/cons, risk, values, dharma/duty, long-term consequences, opportunity cost, emotional bias. **Auto pattern-warning.** | "Decision Support" |
| `/reflect` | Journal check-in; detects hidden problems, emotional patterns, unresolved issues. **Auto pattern-warning.** | "Reflection Journal" |
| `/actions` | Aggregate open actions across all problems by status; **review** stalled/overdue actions. | "Action Tracker" |
| `/systems` | Build a preventive routine/rule/checklist/habit/boundary for a recurring pattern. | "Preventive Systems" |
| `/export` | Emit a JSON bundle of everything (data ownership / migration). | "Export My Data" |

### 7.1 The `/solve` process (default flow)

1. **Restate the problem clearly** — turn messy input into a clear statement.
2. **Identify the deeper issue** — emotional / practical / relational / financial / health / discipline / identity / spiritual / moral / decision.
3. **Rate the problem** — 1–10 on urgency, importance, emotional intensity, controllability, long-term impact, recurrence likelihood, effort required.
4. **Classify** — subjects, life areas, problem types (from `taxonomy.md`).
5. **Compare with past problems (pattern-warning)** — which past problem it resembles, what pattern is repeating, the trigger, what was tried, what worked, what didn't, what to do differently now.
6. **Use the knowledge base** — search relevant subjects; bring in specific saved ideas with source citations; no generic advice when the base has something relevant.
7. **Analyze the root cause** — psychology + philosophy + systems thinking + practical reasoning.
8. **Separate control from non-control** — fully in control / partly in control / outside control.
9. **Possible solutions** — multiple, ranked most-practical to least.
10. **Ordered action plan** — each action: what, why, when, difficulty, expected result.
11. **Immediate next action** — one small thing doable today.
12. **Save** a structured problem entry (§5.1).
13. **Update life analytics** — feed the structured fields that `/analytics` reads.

### 7.2 Default output format

```
Problem Summary:        [clear restatement]
Deeper Issue:           [root layer]
Problem Ratings:        [the 7 scores, 1–10]
Category and Tags:      [subject, life area, problem type]
Similar Past Problems:  [past patterns, if any]
Root Cause Analysis:    [structured explanation]
Relevant Wisdom From My Knowledge Database:  [ideas + source names]
What Is In My Control:  [control analysis]
Possible Solutions:     [ranked]
Recommended Action Plan:[ordered steps]
Immediate Next Action:  [one small action for today]
Tracking Note:          [the saved memory entry]
```

---

## 8. Relationships layer

The system explicitly tracks relationships, stored as YAML ID-references in v1 and designed to become a graph view in the hosted app:

- **Problem ↔ knowledge** — `knowledge_refs`
- **Problem ↔ actions** — inline `actions[]` (child entities)
- **Problem ↔ outcomes** — inline `outcomes[]` (child entities)
- **Problem ↔ repeated patterns** — `related_problems`, `patterns_detected`
- **Problem ↔ people/situations** — `people`
- **Problem ↔ preventive systems** — `systems` / `source_problems`
- **Reflection/Decision ↔ problems** — `detected_problems`, `related_problems`

These references are the edges of a future relationship graph; in v1 they power pattern-warning, recurrence analytics, and review.

---

## 9. Analytics & review

Computed **purely from structured frontmatter fields** (not free text), so the same logic ports to SQL `GROUP BY` later:

- Most common `subjects` / `problem_types` / `life_areas`.
- Recurring `emotions` and `people` (triggers; people/situations that keep appearing).
- Action `status` distribution — what I start vs. finish.
- **Avoided areas** — problems abandoned or with no completed actions.
- **Improving areas** — resolved with positive outcomes.
- **Areas needing better systems** — recurring problem types with no active `system`.
- Recurrence clusters via `related_problems`.

**Review behavior** (surfaced through `/analytics` and `/actions`): open problems, unfinished/overdue actions, recurring patterns, and old unresolved issues — so the tool keeps me accountable over time, not just at the moment of solving.

---

## 10. Privacy & data ownership (core principles, from day one)

Treated as first-class design constraints because this holds very personal life data.

**Data ownership (true in v1 already):**

- All data lives as local Markdown + YAML that I can read and edit directly.
- `/export` emits a full JSON bundle; v1 is also already Markdown. I always own my data in **both** Markdown and JSON, even after the hosted version exists.

**Privacy (designed in now, enforced in the hosted phase):**

- Private user account; secure authentication.
- Encrypted storage where possible.
- Export **and delete** my data on demand.
- No sharing without explicit permission.
- Clear separation between personal data storage and AI processing.

---

## 11. Future hosted architecture & migration path

The MVP is built so the hosted "LifeOS" is a **port, not a rewrite**.

### Data model → database

- Entities → tables: `problems`, `actions` (FK → problem), `outcomes` (FK → problem), `documents`, `reflections`, `decisions`, `systems`.
- Controlled vocabulary → enum tables / tag tables; `people` → a tracked entity with join rows.
- Relationships (§8) → foreign keys + a join table that backs a **graph view**.
- Frontmatter fields are already typed → columns map directly. Stable IDs become primary keys.

### Knowledge → RAG

- Documents get chunked + embedded into **Postgres + pgvector** (Neon) for real vector search backing `/ask` and `/solve`'s knowledge step.

### Import pipelines (future)

- Raw text import, transcript import, PDF import, manual note import, **bulk folder import** — each runs the same classification that `/add-knowledge` does in v1.

### Commands → endpoints → UI

Each command (§7) is a REST endpoint and a UI feature. Planned dashboards/pages:

- Problem history · Action tracker · Insights dashboard · Knowledge library · Repeated-pattern dashboard · Decision history · Reflection journal · Systems/routines page.
- Later: calendar / reminder / task integration.

### Migration = a parse script

Read each file's YAML → insert rows; `/export` already emits the same schema as JSON, so import is trivial.

---

## 12. How v1 is verified

- Author `CLAUDE.md`, `taxonomy.md`, `SCHEMA.md`, and the 11 command files.
- Seed 2–3 knowledge docs via `/add-knowledge` and run one real `/solve`.
- Confirm: files validate against `SCHEMA.md`; IDs and cross-links resolve; controlled tags are all in `taxonomy.md`; pattern-warning fires when a related past problem exists; `/analytics` correctly reads the structured fields; `/export` round-trips to JSON and back.

---

## 13. Open items for the implementation plan

- Exact `taxonomy.md` enumerations (full emotion list, life-area list) — drafted during implementation, reviewed before first use.
- Wording of the safety/escalation block in `CLAUDE.md`.
- Whether `analytics/` snapshots are saved every run or on request (default: on request).
