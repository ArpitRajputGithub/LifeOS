# LifeOS — Personal Problem-Solving AI Agent — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local-first, Markdown-based personal problem-solving agent that runs inside Claude Code via slash commands, with a strict data schema and controlled vocabulary so it can later port cleanly to a hosted web app.

**Architecture:** Each user action is a Claude Code slash command in `.claude/commands/`. A shared constitution (`CLAUDE.md`) holds persona, the problem-solving process, output format, and safety rules. Data lives as Markdown files with strict YAML frontmatter in per-entity folders. A controlled vocabulary (`taxonomy.md`) and a Python validator (`tools/validate.py`) enforce schema conformance from day one. A Python exporter (`tools/export.py`) emits a JSON bundle for data ownership and future DB migration.

**Tech Stack:** Markdown + YAML frontmatter (data), Claude Code slash commands (behavior), Python 3 + PyYAML + pytest (validation/export tooling), git (version history + frequent commits).

**Reference spec:** [2026-06-07-lifeos-problem-solver-design.md](../../../2026-06-07-lifeos-problem-solver-design.md)

**Spec refinement note:** The spec names the vocabulary file `taxonomy.md`. This plan keeps that filename but embeds the machine-readable enumerations inside a single fenced ```yaml block in that file, so both humans and `validate.py` read one source of truth.

---

## File Structure

**Foundation / data contract**
- `taxonomy.md` — controlled vocabulary, with a ```yaml block the validator parses
- `SCHEMA.md` — per-entity field contract + validation rules (human reference)
- `CLAUDE.md` — constitution: persona, tone, the 13-step process, output format, safety rule, ID + validation rules
- `README.md` — what this is + how to use it

**Behavior (slash commands)** — `.claude/commands/`
- `solve.md`, `add-knowledge.md`, `outcome.md`, `analytics.md`, `search.md`, `ask.md`, `actions.md`, `export.md` (must-have v1)
- `decide.md`, `reflect.md`, `systems.md` (included, lighter)

**Data stores** (one Markdown file per entity)
- `problems/`, `knowledge/`, `reflections/`, `decisions/`, `systems/` — each with a `README.md` describing its purpose
- `analytics/` — generated snapshots; `exports/` — generated JSON bundles

**Tooling** — `tools/`
- `validate.py` — validate entity files against schema + taxonomy
- `export.py` — emit a JSON bundle of all entities
- `requirements.txt` — `pyyaml`, `pytest`
- `tests/` — pytest tests + fixtures (`tests/fixtures/`)

---

## Phase 0 — Project foundation

### Task 1: Initialize repo structure

**Files:**
- Create: `.gitignore`
- Create: `problems/README.md`, `knowledge/README.md`, `reflections/README.md`, `decisions/README.md`, `systems/README.md`, `analytics/README.md`, `exports/README.md`

- [ ] **Step 1: Initialize git**

Run:
```bash
cd "/Users/0xdeadbeef/dev/Tools/AI Problem Solver"
git init
```
Expected: `Initialized empty Git repository...`

- [ ] **Step 2: Create `.gitignore`**

Create `.gitignore` with exactly:
```gitignore
# Python tooling
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/

# OS
.DS_Store
```
(Note: `exports/` is intentionally NOT ignored — it is your data and stays tracked.)

- [ ] **Step 3: Create data-folder READMEs**

Create each file below with the shown content.

`problems/README.md`:
```markdown
# problems/
One Markdown file per problem (`PRB-YYYYMMDD-NN-*.md`). Actions and outcomes live inline in each file as child entities. See `../SCHEMA.md`.
```

`knowledge/README.md`:
```markdown
# knowledge/
One Markdown file per knowledge document (`KND-YYYYMMDD-NN-*.md`). Classified into the 15 subjects of life. See `../SCHEMA.md`.
```

`reflections/README.md`:
```markdown
# reflections/
Daily/weekly reflection journal entries (`REF-YYYYMMDD-NN-*.md`). See `../SCHEMA.md`.
```

`decisions/README.md`:
```markdown
# decisions/
Decision-support entries (`DEC-YYYYMMDD-NN-*.md`). See `../SCHEMA.md`.
```

`systems/README.md`:
```markdown
# systems/
Preventive systems — routines, rules, checklists, habits, boundaries (`SYS-YYYYMMDD-NN-*.md`). See `../SCHEMA.md`.
```

`analytics/README.md`:
```markdown
# analytics/
Generated insight snapshots (`snapshot-YYYY-MM-DD.md`). Produced by `/analytics`. Derived data — safe to delete and regenerate.
```

`exports/README.md`:
```markdown
# exports/
Generated JSON bundles of all entities (`export-YYYY-MM-DD.json`). Produced by `/export` / `tools/export.py`. Your full, portable copy of the data.
```

- [ ] **Step 4: Commit**

```bash
git add .gitignore problems/ knowledge/ reflections/ decisions/ systems/ analytics/ exports/
git commit -m "chore: scaffold LifeOS directory structure"
```

---

### Task 2: Controlled vocabulary (`taxonomy.md`)

**Files:**
- Create: `taxonomy.md`

- [ ] **Step 1: Create `taxonomy.md`**

Create `taxonomy.md` with exactly this content:

````markdown
# Taxonomy — Controlled Vocabulary

This is the spine of analytics. Every controlled field in every entity must use a value from the lists below. The machine-readable source of truth is the `yaml` block at the bottom of this file (read by `tools/validate.py`). Extending a list is a deliberate edit to this file — never tag off-vocabulary silently.

## The 15 Subjects of Life
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

## Other controlled lists
- **life_areas** — practical areas of daily life.
- **problem_types** — the kind of problem.
- **deeper_issue** — the single dominant layer under the surface.
- **emotions** — controlled emotion words (so "fear" never fragments).
- **source_type** — where a knowledge document came from.
- **difficulty** — action difficulty.
- **status families** — problem / action / decision / system lifecycle states.
- **system kinds** — type of preventive system.
- **reflection periods** — cadence of a reflection.

`people` and free `tags` are NOT enumerated but ARE tracked for recurrence analytics.

```yaml
subjects:
  - self_and_inner_life
  - mind_and_psychology
  - body_and_health
  - relationships_and_people
  - career_and_work
  - money_and_resources
  - philosophy_and_wisdom
  - science_and_reality
  - society_and_civilization
  - practical_life_skills
  - creativity_and_expression
  - morality_ethics_and_character
  - life_stages_and_human_journey
  - problem_types
  - systems_and_thinking
life_areas:
  - self
  - health
  - relationships
  - family
  - friendships
  - career
  - money
  - education_learning
  - spirituality
  - home_environment
  - leisure_recreation
  - purpose_meaning
  - community_society
problem_types:
  - emotional
  - practical
  - decision
  - relationship
  - money
  - career
  - health
  - identity
  - discipline
  - moral
  - spiritual
  - crisis
  - repeated_pattern
deeper_issue:
  - emotional
  - practical
  - relational
  - financial
  - health
  - discipline
  - identity
  - spiritual
  - moral
  - decision
emotions:
  - anxiety
  - fear
  - anger
  - frustration
  - sadness
  - grief
  - guilt
  - shame
  - self_doubt
  - insecurity
  - loneliness
  - overwhelm
  - stress
  - restlessness
  - boredom
  - apathy
  - jealousy
  - resentment
  - hope
  - calm
  - confidence
  - gratitude
  - contentment
  - excitement
  - confusion
  - regret
  - disappointment
  - tiredness
source_type:
  - youtube_transcript
  - book
  - article
  - pdf
  - personal_note
  - reflection
difficulty:
  - easy
  - medium
  - hard
problem_status:
  - open
  - in_progress
  - resolved
  - abandoned
action_status:
  - not_started
  - in_progress
  - completed
  - failed
  - postponed
  - not_relevant
decision_status:
  - open
  - decided
  - reversed
system_status:
  - active
  - paused
  - retired
system_kind:
  - routine
  - rule
  - checklist
  - habit
  - boundary
reflection_period:
  - daily
  - weekly
```
````

- [ ] **Step 2: Commit**

```bash
git add taxonomy.md
git commit -m "feat: add controlled vocabulary (taxonomy.md)"
```

---

### Task 3: Data contract (`SCHEMA.md`)

**Files:**
- Create: `SCHEMA.md`

- [ ] **Step 1: Create `SCHEMA.md`**

Create `SCHEMA.md` with exactly this content:

````markdown
# SCHEMA — The Data Contract

Every entity file is a Markdown file with YAML frontmatter (the structured "row") followed by a human-readable body. All controlled-field values must come from `taxonomy.md`. `tools/validate.py` enforces this.

## Shared rules
- `id` is permanent once assigned and matches its type's pattern.
- `created` / `updated` are `YYYY-MM-DD`.
- Controlled fields must use `taxonomy.md` values exactly.
- Cross-references (`related_problems`, `knowledge_refs`, `systems`, `source_problems`, `related_problems`, `detected_problems`) are lists of existing IDs.

## ID patterns
| Type | Pattern | Example |
|---|---|---|
| problem | `PRB-YYYYMMDD-NN` | `PRB-20260607-01` |
| knowledge | `KND-YYYYMMDD-NN` | `KND-20260607-01` |
| reflection | `REF-YYYYMMDD-NN` | `REF-20260607-01` |
| decision | `DEC-YYYYMMDD-NN` | `DEC-20260607-01` |
| system | `SYS-YYYYMMDD-NN` | `SYS-20260607-01` |
| action (inline child) | `ACT-<problemID>-NN` | `ACT-PRB-20260607-01-01` |
| outcome (inline child) | `OUT-<problemID>-NN` | `OUT-PRB-20260607-01-01` |

`NN` = 2-digit daily sequence: list same-day files of that type and increment.

## problem  (type: problem)
**Required:** `id, type, title, created, updated, status, subjects, life_areas, problem_types, deeper_issue, ratings`
**Optional:** `emotions, people, tags, root_cause, related_problems, knowledge_refs, systems, actions, outcomes, immediate_next_action`
- `status` ∈ problem_status. `subjects` ⊆ subjects. `life_areas` ⊆ life_areas. `problem_types` ⊆ problem_types. `deeper_issue` ∈ deeper_issue. `emotions` ⊆ emotions.
- `ratings` is a map with keys: `urgency, importance, emotional_intensity, controllability, long_term_impact, recurrence_likelihood, effort_required`, each integer 1–10.
- `actions[]` items: `id, what, why, when, difficulty (∈difficulty), expected_result, status (∈action_status), updated`.
- `outcomes[]` items: `id, date, what_happened, what_worked, what_failed, lesson, pattern_to_remember`.
- **Body sections (in order):** Problem Summary, Deeper Issue, Problem Ratings, Category and Tags, Similar Past Problems, Root Cause Analysis, Relevant Wisdom From My Knowledge Database, What Is In My Control, Possible Solutions, Recommended Action Plan, Immediate Next Action, Tracking Note.

## knowledge  (type: knowledge)
**Required:** `id, type, title, created, source_type, subjects`
**Optional:** `source, subtopics, life_areas, problem_types, related_subjects, tags`
- `source_type` ∈ source_type. `subjects` ⊆ subjects. `life_areas` ⊆ life_areas. `problem_types` ⊆ problem_types. `related_subjects` ⊆ subjects.
- **Body sections:** Key Ideas, Practical Lessons, Philosophical Lessons, Emotional Lessons, Possible Use Cases, Summary, Important Quotes or Concepts.

## reflection  (type: reflection)
**Required:** `id, type, created, period`
**Optional:** `mood, subjects, life_areas, detected_problems, patterns_detected, people`
- `period` ∈ reflection_period. `mood` ⊆ emotions. `subjects` ⊆ subjects. `life_areas` ⊆ life_areas.
- **Body:** the journal entry + what the agent noticed (hidden problems, emotional patterns, unresolved issues).

## decision  (type: decision)
**Required:** `id, type, title, created, status, options`
**Optional:** `chosen, related_problems, values_considered, subjects, life_areas, tags`
- `status` ∈ decision_status. `options` is a non-empty list. `subjects` ⊆ subjects. `life_areas` ⊆ life_areas.
- **Body:** comparison on pros/cons, risk, values, dharma/duty, long-term consequences, opportunity cost, emotional bias.

## system  (type: system)
**Required:** `id, type, title, created, status, kind`
**Optional:** `prevents_problem_types, addresses_patterns, source_problems, subjects, life_areas, tags`
- `status` ∈ system_status. `kind` ∈ system_kind. `prevents_problem_types` ⊆ problem_types. `subjects` ⊆ subjects.
- **Body:** the system — trigger, the rule/steps, how to follow it, how to review it.
````

- [ ] **Step 2: Commit**

```bash
git add SCHEMA.md
git commit -m "feat: add data contract (SCHEMA.md)"
```

---

### Task 4: Validator tooling (TDD)

**Files:**
- Create: `tools/requirements.txt`
- Create: `tools/validate.py`
- Test: `tools/tests/test_validate.py`
- Test fixtures: `tools/tests/fixtures/good_problem.md`, `tools/tests/fixtures/bad_problem.md`, `tools/tests/fixtures/good_knowledge.md`

- [ ] **Step 1: Create requirements + install**

Create `tools/requirements.txt`:
```
pyyaml
pytest
```

Run:
```bash
cd "/Users/0xdeadbeef/dev/Tools/AI Problem Solver"
python3 -m venv .venv && . .venv/bin/activate && pip install -r tools/requirements.txt
```
Expected: pyyaml and pytest install successfully.

- [ ] **Step 2: Create test fixtures**

`tools/tests/fixtures/good_problem.md`:
```markdown
---
id: PRB-20260607-01
type: problem
title: "Test problem"
created: 2026-06-07
updated: 2026-06-07
status: open
subjects: [mind_and_psychology, career_and_work]
life_areas: [career]
problem_types: [decision, emotional]
deeper_issue: emotional
emotions: [anxiety, self_doubt]
ratings: {urgency: 7, importance: 8, emotional_intensity: 6, controllability: 5, long_term_impact: 7, recurrence_likelihood: 6, effort_required: 5}
actions:
  - {id: ACT-PRB-20260607-01-01, what: "do x", why: "because", when: 2026-06-08, difficulty: easy, expected_result: "y", status: not_started, updated: 2026-06-07}
---
# Body
```

`tools/tests/fixtures/bad_problem.md` (missing `status`, off-vocab subject, bad id):
```markdown
---
id: PROBLEM-1
type: problem
title: "Bad problem"
created: 2026-06-07
updated: 2026-06-07
subjects: [not_a_real_subject]
life_areas: [career]
problem_types: [decision]
deeper_issue: emotional
ratings: {urgency: 7, importance: 8, emotional_intensity: 6, controllability: 5, long_term_impact: 7, recurrence_likelihood: 6, effort_required: 5}
---
# Body
```

`tools/tests/fixtures/good_knowledge.md`:
```markdown
---
id: KND-20260607-01
type: knowledge
title: "Seneca on anxiety"
created: 2026-06-07
source_type: book
subjects: [philosophy_and_wisdom]
subtopics: [stoicism]
problem_types: [emotional]
tags: [control]
---
# Key Ideas
```

- [ ] **Step 3: Write the failing test**

Create `tools/tests/test_validate.py`:
```python
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import validate  # noqa: E402

TAX = validate.load_taxonomy()
FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def errs(name):
    return validate.validate_file(os.path.join(FIX, name), TAX)


def test_good_problem_has_no_errors():
    assert errs("good_problem.md") == []


def test_good_knowledge_has_no_errors():
    assert errs("good_knowledge.md") == []


def test_bad_problem_flags_missing_status():
    assert any("missing required field 'status'" in e for e in errs("bad_problem.md"))


def test_bad_problem_flags_off_vocab_subject():
    assert any("not_a_real_subject" in e for e in errs("bad_problem.md"))


def test_bad_problem_flags_bad_id():
    assert any("does not match" in e for e in errs("bad_problem.md"))


def test_taxonomy_loads_15_subjects():
    assert len(TAX["subjects"]) == 15
```

- [ ] **Step 4: Run the test to verify it fails**

Run:
```bash
. .venv/bin/activate && python -m pytest tools/tests/test_validate.py -v
```
Expected: FAIL / ERROR — `validate` module or `load_taxonomy`/`validate_file` not defined.

- [ ] **Step 5: Implement `tools/validate.py`**

Create `tools/validate.py`:
```python
#!/usr/bin/env python3
"""Validate LifeOS entity files against SCHEMA.md and taxonomy.md."""
import glob
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ID_PATTERNS = {
    "problem": r"^PRB-\d{8}-\d{2}$",
    "knowledge": r"^KND-\d{8}-\d{2}$",
    "reflection": r"^REF-\d{8}-\d{2}$",
    "decision": r"^DEC-\d{8}-\d{2}$",
    "system": r"^SYS-\d{8}-\d{2}$",
}

REQUIRED = {
    "problem": ["id", "type", "title", "created", "updated", "status",
                "subjects", "life_areas", "problem_types", "deeper_issue", "ratings"],
    "knowledge": ["id", "type", "title", "created", "source_type", "subjects"],
    "reflection": ["id", "type", "created", "period"],
    "decision": ["id", "type", "title", "created", "status", "options"],
    "system": ["id", "type", "title", "created", "status", "kind"],
}

# entity field -> taxonomy list key
CONTROLLED = {
    "subjects": "subjects",
    "related_subjects": "subjects",
    "life_areas": "life_areas",
    "problem_types": "problem_types",
    "prevents_problem_types": "problem_types",
    "deeper_issue": "deeper_issue",
    "emotions": "emotions",
    "mood": "emotions",
    "source_type": "source_type",
    "period": "reflection_period",
    "kind": "system_kind",
}

STATUS_KEY = {
    "problem": "problem_status",
    "decision": "decision_status",
    "system": "system_status",
}

RATING_KEYS = ["urgency", "importance", "emotional_intensity", "controllability",
               "long_term_impact", "recurrence_likelihood", "effort_required"]


def load_taxonomy(path=None):
    path = path or os.path.join(ROOT, "taxonomy.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"```yaml\n(.*?)```", text, re.S)
    if not m:
        raise ValueError("No ```yaml block found in taxonomy.md")
    return yaml.safe_load(m.group(1))


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    return yaml.safe_load(m.group(1))


def _as_list(v):
    return v if isinstance(v, list) else [v]


def validate_file(path, tax):
    errors = []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm = parse_frontmatter(text)
    if fm is None:
        return [f"{path}: no YAML frontmatter"]
    t = fm.get("type")
    if t not in REQUIRED:
        return [f"{path}: unknown or missing type: {t!r}"]

    for field in REQUIRED[t]:
        if field not in fm or fm[field] in (None, "", []):
            errors.append(f"{path}: missing required field '{field}'")

    pat = ID_PATTERNS.get(t)
    if pat and not re.match(pat, str(fm.get("id", ""))):
        errors.append(f"{path}: id '{fm.get('id')}' does not match {pat}")

    for field, key in CONTROLLED.items():
        if field not in fm or fm[field] is None:
            continue
        allowed = set(tax.get(key, []))
        for v in _as_list(fm[field]):
            if v not in allowed:
                errors.append(f"{path}: '{field}' value '{v}' not in taxonomy[{key}]")

    skey = STATUS_KEY.get(t)
    if skey and "status" in fm and fm["status"] not in set(tax.get(skey, [])):
        errors.append(f"{path}: status '{fm['status']}' not in taxonomy[{skey}]")

    if t == "problem":
        ratings = fm.get("ratings") or {}
        for rk in RATING_KEYS:
            val = ratings.get(rk)
            if not isinstance(val, int) or not (1 <= val <= 10):
                errors.append(f"{path}: ratings.{rk} must be int 1-10, got {val!r}")
        for a in fm.get("actions") or []:
            if a.get("status") not in set(tax.get("action_status", [])):
                errors.append(f"{path}: action {a.get('id')} status '{a.get('status')}' invalid")
            if a.get("difficulty") not in set(tax.get("difficulty", [])):
                errors.append(f"{path}: action {a.get('id')} difficulty '{a.get('difficulty')}' invalid")

    return errors


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            yield from glob.glob(os.path.join(p, "**", "*.md"), recursive=True)
        elif p.endswith(".md"):
            yield p


def main(argv):
    tax = load_taxonomy()
    targets = argv[1:] or ["problems", "knowledge", "reflections", "decisions", "systems"]
    targets = [os.path.join(ROOT, t) if not os.path.isabs(t) else t for t in targets]
    all_errors = []
    for fpath in iter_files(targets):
        all_errors += validate_file(fpath, tax)
    for e in all_errors:
        print(e)
    if all_errors:
        print(f"\n{len(all_errors)} error(s)")
        return 1
    print("All files valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

- [ ] **Step 6: Run the test to verify it passes**

Run:
```bash
. .venv/bin/activate && python -m pytest tools/tests/test_validate.py -v
```
Expected: PASS (6 passed).

- [ ] **Step 7: Commit**

```bash
git add tools/
git commit -m "feat: add schema validator with tests (validate.py)"
```

---

## Phase 1 — Constitution + core flow

### Task 5: Constitution (`CLAUDE.md`)

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Create `CLAUDE.md`**

Create `CLAUDE.md` with exactly this content:

````markdown
# LifeOS — Constitution

You are my **Personal Life Problem-Solving AI Agent**. Your purpose: help me move from confusion to clarity, and from clarity to action, on the real problems in my life — using structured reasoning, my knowledge base (`knowledge/`), my past problem history (`problems/`), and wisdom across the subjects of life.

## Tone
Calm, honest, direct, practical, supportive. No vague motivation. No flattery. Do not only explain the problem — help me solve it.

## Use philosophy practically
- **Stoicism:** control, judgment, discipline, acceptance, virtue.
- **Indian philosophy:** dharma, karma, detachment, self-observation, clarity of duty.
- **Psychology:** emotions, triggers, beliefs, habits, avoidance, cognitive distortions.
- **Productivity:** systems, routines, prioritization, execution.

## Knowledge base rule
When the knowledge base contains something relevant, USE it and CITE the document (`id` + title). Do not give generic advice when my saved material applies.

## Pattern-warning (automatic)
Inside `/solve`, `/decide`, and `/reflect`: scan `problems/` for a similar past pattern. If found, warn me clearly: which past problem it resembles (by `id`), what pattern is repeating, the trigger, what I tried, what worked, what didn't, and what to do differently now.

## The problem-solving process (used by /solve)
1. Restate the problem clearly.
2. Identify the deeper issue (emotional / practical / relational / financial / health / discipline / identity / spiritual / moral / decision).
3. Rate 1–10: urgency, importance, emotional_intensity, controllability, long_term_impact, recurrence_likelihood, effort_required.
4. Classify: subjects, life_areas, problem_types (from `taxonomy.md`).
5. Compare with past problems (pattern-warning).
6. Use the knowledge base (cite sources).
7. Analyze the root cause (psychology + philosophy + systems thinking + practical reasoning).
8. Separate control from non-control (fully / partly / outside my control).
9. Possible solutions, ranked most-practical to least.
10. Ordered action plan — each action: what, why, when, difficulty, expected result.
11. One immediate next action, small enough to do today.
12. Save a structured entry (see Data rules).
13. Update analytics (the structured fields feed `/analytics`).

## Default output format (for /solve)
```
Problem Summary:
Deeper Issue:
Problem Ratings:
Category and Tags:
Similar Past Problems:
Root Cause Analysis:
Relevant Wisdom From My Knowledge Database:
What Is In My Control:
Possible Solutions:
Recommended Action Plan:
Immediate Next Action:
Tracking Note:
```

## Data rules (CRITICAL)
- Every entity is a Markdown file with YAML frontmatter conforming to `SCHEMA.md`, using only values from `taxonomy.md`.
- IDs are permanent and follow the patterns in `SCHEMA.md`. Compute `NN` by listing same-day files of that type and incrementing.
- **Before saving any file, validate it:** run `python tools/validate.py <path>` (activate `.venv` first). If it reports errors, fix them before finishing. If a needed tag is genuinely missing from `taxonomy.md`, propose adding it to `taxonomy.md` as an explicit edit — never write an off-vocabulary tag silently.
- Cross-link by ID: `related_problems`, `knowledge_refs`, `systems`, etc.

## Safety rule
You are not a substitute for a doctor, therapist, lawyer, or financial advisor. If a problem involves serious mental-health risk, medical danger, legal danger, financial danger, or harm to myself or others, clearly advise me to contact a qualified professional or a trusted person — first, before the rest of the analysis.
````

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "feat: add LifeOS constitution (CLAUDE.md)"
```

---

### Task 6: README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create `README.md`**

Create `README.md` with exactly this content:

````markdown
# LifeOS — Personal Problem-Solving AI Agent

A local-first, Markdown-based personal agent that helps me understand, organize, and solve life problems — built to later become a hosted LifeOS web app.

## Setup
```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r tools/requirements.txt
```

## How to use (inside Claude Code)
| Command | What it does |
|---|---|
| `/solve` | Describe a problem; runs the full process and saves an entry. |
| `/add-knowledge` | Add and classify a transcript / note / book / PDF text. |
| `/outcome` | Record how a past problem turned out. |
| `/analytics` | Insights across all problems; review open items. |
| `/search` | Search past problems by category, emotion, person, area, date, tag, outcome. |
| `/ask` | Ask the knowledge base a question (cited answers). |
| `/actions` | See open actions across all problems by status. |
| `/decide` | Decision support between options. |
| `/reflect` | Daily/weekly reflection check-in. |
| `/systems` | Build a preventive system for a recurring pattern. |
| `/export` | Export everything to a JSON bundle. |

## Data
- `problems/ knowledge/ reflections/ decisions/ systems/` — your data, as Markdown.
- `taxonomy.md` — controlled vocabulary. `SCHEMA.md` — the data contract.
- Validate any file: `python tools/validate.py <path>`.
- Export: `python tools/export.py`.

## Design
See [docs/superpowers/specs/2026-06-07-lifeos-problem-solver-design.md](docs/superpowers/specs/2026-06-07-lifeos-problem-solver-design.md).
````

Note: the spec file referenced was moved to the repo root during brainstorming; if it is not under `docs/superpowers/specs/`, update this link to `2026-06-07-lifeos-problem-solver-design.md`.

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README"
```

---

### Task 7: `/add-knowledge` command + seed + validate

**Files:**
- Create: `.claude/commands/add-knowledge.md`
- Create: `knowledge/KND-20260607-01-seneca-on-anxiety.md` (seed)
- Create: `knowledge/KND-20260607-02-deep-work-attention.md` (seed)

- [ ] **Step 1: Create the command**

Create `.claude/commands/add-knowledge.md`:
```markdown
---
description: Classify and file a knowledge document into the LifeOS knowledge base
---

Follow `CLAUDE.md` and `SCHEMA.md`. The material to add is below (or ask me for it if empty):

$ARGUMENTS

Steps:
1. Determine the next id: list `knowledge/KND-<today>-*.md`, increment `NN` (today = the current date, `YYYYMMDD`).
2. Read and classify the material into the knowledge schema: `subjects` (from the 15), `subtopics`, `life_areas`, `problem_types`, `related_subjects`, `tags`, `source_type`, `source`. Use ONLY `taxonomy.md` values for controlled fields.
3. Write the body sections: Key Ideas, Practical Lessons, Philosophical Lessons, Emotional Lessons, Possible Use Cases, Summary, Important Quotes or Concepts.
4. Save as `knowledge/KND-<today>-NN-<kebab-title>.md`.
5. Validate: `python tools/validate.py <new file>` (activate `.venv`). Fix any errors before finishing.
6. Confirm to me: the id, title, and how it was classified.
```

- [ ] **Step 2: Create seed knowledge docs**

`knowledge/KND-20260607-01-seneca-on-anxiety.md`:
```markdown
---
id: KND-20260607-01
type: knowledge
title: "Seneca — On groundless anxiety"
created: 2026-06-07
source_type: book
source: "Seneca, Letters from a Stoic, Letter XIII"
subjects: [philosophy_and_wisdom]
subtopics: [stoicism, acceptance]
life_areas: [self]
problem_types: [emotional, identity]
related_subjects: [mind_and_psychology]
tags: [control, fear, imagination]
---
# Key Ideas
We suffer more in imagination than in reality. Much fear is borrowed from a future that may never arrive.

# Practical Lessons
When anxious, ask: what is actually happening now versus what am I imagining? Separate the present fact from the projected fear.

# Philosophical Lessons
Stoicism: distinguish what is in our control (our judgments) from what is not (outcomes). Anxiety lives in the gap.

# Emotional Lessons
Naming a fear concretely shrinks it. Vague dread is larger than any specific, examined worry.

# Possible Use Cases
Overthinking decisions, fear of failure, catastrophizing, sleeplessness from worry.

# Summary
Most anxiety is anticipatory and exaggerated; return attention to the present and to what you control.

# Important Quotes or Concepts
"We suffer more often in imagination than in reality."
```

`knowledge/KND-20260607-02-deep-work-attention.md`:
```markdown
---
id: KND-20260607-02
type: knowledge
title: "Deep Work — attention as the lever"
created: 2026-06-07
source_type: book
source: "Cal Newport, Deep Work"
subjects: [career_and_work, systems_and_thinking]
subtopics: [focus, deep_work]
life_areas: [career]
problem_types: [discipline, practical]
related_subjects: [mind_and_psychology]
tags: [focus, attention, systems]
---
# Key Ideas
The ability to focus without distraction on a cognitively demanding task is rare, valuable, and trainable.

# Practical Lessons
Schedule deep-work blocks; remove distraction triggers; treat attention as a finite daily resource.

# Philosophical Lessons
Discipline is freedom: constraints on shallow inputs create room for meaningful output.

# Emotional Lessons
Constant context-switching breeds low-grade anxiety; single-tasking is calming.

# Possible Use Cases
Procrastination, scattered focus, low output, feeling busy but unproductive.

# Summary
Protect and train attention with systems; depth beats busyness.

# Important Quotes or Concepts
"Clarity about what matters provides clarity about what does not."
```

- [ ] **Step 3: Validate the seed docs**

Run:
```bash
. .venv/bin/activate && python tools/validate.py knowledge/
```
Expected: `All files valid.`

- [ ] **Step 4: Commit**

```bash
git add .claude/commands/add-knowledge.md knowledge/KND-20260607-01-seneca-on-anxiety.md knowledge/KND-20260607-02-deep-work-attention.md
git commit -m "feat: add /add-knowledge command and seed knowledge docs"
```

---

### Task 8: `/solve` command + sample problem + validate

**Files:**
- Create: `.claude/commands/solve.md`
- Create: `problems/PRB-20260607-01-overthinking-job-offer.md` (sample, demonstrates pattern-warning target + knowledge ref)

- [ ] **Step 1: Create the command**

Create `.claude/commands/solve.md`:
```markdown
---
description: Solve a life problem with the full LifeOS process and save a tracked entry
---

Follow `CLAUDE.md` (the 13-step process, output format, safety rule, data rules) and `SCHEMA.md`.

My problem:

$ARGUMENTS

Steps:
1. If the problem hits a safety trigger (serious mental-health/medical/legal/financial risk or harm), give the safety guidance FIRST, then continue if appropriate.
2. Run steps 1–11 of the process and respond in the Default Output Format.
3. **Pattern-warning:** scan `problems/` for similar past problems (by subjects/problem_types/tags/people). If found, fill "Similar Past Problems" with the matched `id`(s), the repeating pattern, and what to do differently.
4. **Knowledge:** scan `knowledge/` for relevant docs; cite them by id+title in "Relevant Wisdom"; record their ids in `knowledge_refs`.
5. If `recurrence_likelihood >= 7`, suggest creating a preventive system via `/systems`.
6. Determine the next id (`problems/PRB-<today>-*.md`, increment NN) and save the full entry: frontmatter per SCHEMA + the body = the output format sections.
7. Validate: `python tools/validate.py <new file>`. Fix errors before finishing.
8. End by telling me the saved id and the single Immediate Next Action.
```

- [ ] **Step 2: Create a sample problem**

`problems/PRB-20260607-01-overthinking-job-offer.md`:
```markdown
---
id: PRB-20260607-01
type: problem
title: "Paralyzed deciding on the new job offer"
created: 2026-06-07
updated: 2026-06-07
status: open
subjects: [mind_and_psychology, career_and_work]
life_areas: [career]
problem_types: [decision, emotional]
deeper_issue: emotional
emotions: [anxiety, self_doubt]
people: [manager]
tags: [overthinking, fear_of_failure]
ratings: {urgency: 7, importance: 8, emotional_intensity: 6, controllability: 5, long_term_impact: 7, recurrence_likelihood: 6, effort_required: 5}
root_cause: "Fear of an irreversible choice -> avoidance via over-analysis"
related_problems: []
knowledge_refs: [KND-20260607-01]
systems: []
actions:
  - {id: ACT-PRB-20260607-01-01, what: "List the 3 things I am actually afraid of", why: "Names the vague fear so it can be examined", when: 2026-06-08, difficulty: easy, expected_result: "Fear becomes concrete and smaller", status: not_started, updated: 2026-06-07}
outcomes: []
immediate_next_action: "Write the 3 fears, 10 minutes tonight"
---
# Problem Summary
I cannot decide whether to accept a new job offer and keep over-analyzing it.

# Deeper Issue
Emotional: fear of making an irreversible wrong choice, expressed as over-analysis.

# Problem Ratings
urgency 7, importance 8, emotional_intensity 6, controllability 5, long_term_impact 7, recurrence_likelihood 6, effort_required 5.

# Category and Tags
Subjects: mind_and_psychology, career_and_work. Life area: career. Type: decision, emotional.

# Similar Past Problems
None recorded yet.

# Root Cause Analysis
The decision feels final, so avoidance (more analysis) reduces short-term anxiety while delaying the choice.

# Relevant Wisdom From My Knowledge Database
KND-20260607-01 (Seneca — On groundless anxiety): "We suffer more often in imagination than in reality." Separate the present fact from projected fear.

# What Is In My Control
Fully: gathering specific facts, naming fears, setting a decision deadline. Partly: others' reactions. Outside: how the role actually unfolds.

# Possible Solutions
1. Set a 48-hour decision deadline with written criteria. 2. List concrete fears and test each. 3. Talk once with a trusted person, then decide.

# Recommended Action Plan
Tonight: write the 3 fears. Tomorrow: define decision criteria. Within 48h: decide.

# Immediate Next Action
Write the 3 fears, 10 minutes tonight.

# Tracking Note
Saved as PRB-20260607-01; decision/emotional; anxiety + self_doubt; root cause = fear of irreversibility.
```

- [ ] **Step 3: Validate problems + full repo**

Run:
```bash
. .venv/bin/activate && python tools/validate.py
```
Expected: `All files valid.`

- [ ] **Step 4: Commit**

```bash
git add .claude/commands/solve.md problems/PRB-20260607-01-overthinking-job-offer.md
git commit -m "feat: add /solve command and sample problem"
```

---

## Phase 2 — Tracking & retrieval

### Task 9: `/outcome` command

**Files:**
- Create: `.claude/commands/outcome.md`

- [ ] **Step 1: Create the command**

Create `.claude/commands/outcome.md`:
```markdown
---
description: Record the outcome of a past problem and update its status and lessons
---

Follow `CLAUDE.md` and `SCHEMA.md`.

Which problem + what happened:

$ARGUMENTS

Steps:
1. Identify the target problem file (by id, or search `problems/` by title/keywords; confirm with me if ambiguous).
2. Append an `outcomes[]` entry: `id` = `OUT-<problemID>-NN` (increment), `date` (today), `what_happened`, `what_worked`, `what_failed`, `lesson`, `pattern_to_remember`.
3. Update `status` (open/in_progress/resolved/abandoned), update affected `actions[].status`, set `updated` to today.
4. Validate: `python tools/validate.py <file>`. Fix errors.
5. Tell me the recorded lesson and the pattern to remember next time.
```

- [ ] **Step 2: Verify against the sample problem**

Manually confirm by adding a test outcome to `PRB-20260607-01` in a scratch copy is NOT required; instead validate the command's described mutation produces a schema-valid file by re-running:
```bash
. .venv/bin/activate && python tools/validate.py problems/
```
Expected: `All files valid.` (command file itself is not an entity; this confirms existing data still valid.)

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/outcome.md
git commit -m "feat: add /outcome command"
```

---

### Task 10: `/actions` command

**Files:**
- Create: `.claude/commands/actions.md`

- [ ] **Step 1: Create the command**

Create `.claude/commands/actions.md`:
```markdown
---
description: Show open actions across all problems, grouped by status; review stalled items
---

Follow `CLAUDE.md`.

Optional filter:

$ARGUMENTS

Steps:
1. Read all `problems/*.md`; collect every `actions[]` item with its parent problem id/title.
2. Group by `status` (not_started, in_progress, completed, failed, postponed, not_relevant). Apply any filter in $ARGUMENTS (by status, problem, difficulty, or `when` date).
3. Highlight **review** items: actions with `when` in the past that are still not_started/in_progress (overdue/stalled).
4. Present as a table: action id, parent problem, what, when, difficulty, status.
5. End with the top 3 actions worth doing next and why.
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/actions.md
git commit -m "feat: add /actions command"
```

---

### Task 11: `/search` command

**Files:**
- Create: `.claude/commands/search.md`

- [ ] **Step 1: Create the command**

Create `.claude/commands/search.md`:
```markdown
---
description: Search past problems by category, emotion, person, life area, date, tag, or outcome
---

Follow `CLAUDE.md`.

Query:

$ARGUMENTS

Steps:
1. Parse the query into structured filters: any of `subjects`, `problem_types`, `life_areas`, `emotions`, `people`, `tags`, `status`, date range (`created`), or outcome keywords.
2. Read `problems/*.md` frontmatter; match against the filters (AND semantics unless I say otherwise).
3. Return ranked matches: problem id, title, created, status, matched fields, and the one-line `root_cause`.
4. If a repeated pattern appears across matches (same problem_type/tags recurring), point it out.
5. Offer to open or `/outcome` any match.
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/search.md
git commit -m "feat: add /search command"
```

---

### Task 12: `/ask` command

**Files:**
- Create: `.claude/commands/ask.md`

- [ ] **Step 1: Create the command**

Create `.claude/commands/ask.md`:
```markdown
---
description: Ask the knowledge base a question; answer only from saved material, with citations
---

Follow `CLAUDE.md`.

Question:

$ARGUMENTS

Steps:
1. Identify relevant `knowledge/*.md` by `subjects`, `subtopics`, `problem_types`, `tags`, and body content.
2. Answer the question using those documents. Cite each source as `id` + title. Quote "Important Quotes or Concepts" where apt.
3. If the knowledge base has little or nothing relevant, say so plainly and clearly mark any general knowledge as NOT from my base — then suggest what to `/add-knowledge`.
4. End with the 2–3 most useful saved ideas on this topic.
```

- [ ] **Step 2: Verify retrieval target exists**

Run:
```bash
. .venv/bin/activate && python tools/validate.py knowledge/
```
Expected: `All files valid.` (confirms the citable corpus is schema-valid).

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/ask.md
git commit -m "feat: add /ask command"
```

---

## Phase 3 — Insights & data ownership

### Task 13: `/analytics` command

**Files:**
- Create: `.claude/commands/analytics.md`

- [ ] **Step 1: Create the command**

Create `.claude/commands/analytics.md`:
```markdown
---
description: Insights across all problems from structured fields; review open and unresolved items
---

Follow `CLAUDE.md`.

Optional scope (e.g. a date range):

$ARGUMENTS

Steps:
1. Read all `problems/*.md` (and `reflections/`, `decisions/`, `systems/` where useful). Use ONLY structured frontmatter fields for counts.
2. Report:
   - Most common `subjects`, `problem_types`, `life_areas`.
   - Recurring `emotions` and `people` (triggers; who/what keeps appearing).
   - Action `status` distribution (what I start vs finish).
   - **Avoided areas:** problems `abandoned` or with no `completed` actions.
   - **Improving areas:** `resolved` with positive outcomes.
   - **Needs better systems:** recurring `problem_types` with no `active` system.
   - Recurrence clusters via `related_problems`.
3. **Review:** list open problems, overdue/stalled actions, and old unresolved issues needing attention.
4. Offer to save a snapshot to `analytics/snapshot-<today>.md` (only if I say yes).
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/analytics.md
git commit -m "feat: add /analytics command"
```

---

### Task 14: `/export` command + exporter tool (TDD)

**Files:**
- Create: `tools/export.py`
- Test: `tools/tests/test_export.py`
- Create: `.claude/commands/export.md`

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_export.py`:
```python
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import export  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_build_bundle_groups_by_type():
    bundle = export.build_bundle(ROOT)
    assert "problems" in bundle and "knowledge" in bundle
    assert any(p["id"] == "PRB-20260607-01" for p in bundle["problems"])
    assert any(k["id"] == "KND-20260607-01" for k in bundle["knowledge"])


def test_bundle_is_json_serializable():
    bundle = export.build_bundle(ROOT)
    json.dumps(bundle, default=str)  # must not raise
```

- [ ] **Step 2: Run the test to verify it fails**

Run:
```bash
. .venv/bin/activate && python -m pytest tools/tests/test_export.py -v
```
Expected: FAIL/ERROR — `export` module not found.

- [ ] **Step 3: Implement `tools/export.py`**

Create `tools/export.py`:
```python
#!/usr/bin/env python3
"""Export all LifeOS entities to a single JSON bundle (data ownership / migration)."""
import glob
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDERS = {
    "problems": "problems",
    "knowledge": "knowledge",
    "reflections": "reflections",
    "decisions": "decisions",
    "systems": "systems",
}


def _frontmatter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return yaml.safe_load(text[4:end])


def build_bundle(root=ROOT):
    bundle = {}
    for key, folder in FOLDERS.items():
        items = []
        for path in sorted(glob.glob(os.path.join(root, folder, "*.md"))):
            fm = _frontmatter(path)
            if fm and fm.get("type"):
                items.append(fm)
        bundle[key] = items
    return bundle


def main(argv):
    root = ROOT
    bundle = build_bundle(root)
    out_dir = os.path.join(root, "exports")
    os.makedirs(out_dir, exist_ok=True)
    # Caller passes the date string to keep this deterministic/testable.
    date = argv[1] if len(argv) > 1 else "latest"
    out_path = os.path.join(out_dir, f"export-{date}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, default=str, ensure_ascii=False)
    counts = {k: len(v) for k, v in bundle.items()}
    print(f"Wrote {out_path}")
    print(f"Counts: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

- [ ] **Step 4: Run the test to verify it passes**

Run:
```bash
. .venv/bin/activate && python -m pytest tools/tests/test_export.py -v
```
Expected: PASS (2 passed).

- [ ] **Step 5: Create the `/export` command**

Create `.claude/commands/export.md`:
```markdown
---
description: Export all LifeOS data to a JSON bundle for ownership and future migration
---

Follow `CLAUDE.md`.

Steps:
1. Activate `.venv`, run: `python tools/export.py <today YYYY-MM-DD>`.
2. Report the output path and the per-type counts.
3. Remind me the data also remains as Markdown in `problems/ knowledge/ reflections/ decisions/ systems/` — I own it in both formats.
```

- [ ] **Step 6: Smoke-test the exporter**

Run:
```bash
. .venv/bin/activate && python tools/export.py 2026-06-07 && python -c "import json; b=json.load(open('exports/export-2026-06-07.json')); print(len(b['problems']), len(b['knowledge']))"
```
Expected: prints `1 2` (1 sample problem, 2 seed knowledge docs) and writes `exports/export-2026-06-07.json`.

- [ ] **Step 7: Commit**

```bash
git add tools/export.py tools/tests/test_export.py .claude/commands/export.md exports/export-2026-06-07.json
git commit -m "feat: add /export command and JSON exporter with tests"
```

---

## Phase 4 — Lighter commands (decide / reflect / systems)

### Task 15: `/decide` command

**Files:**
- Create: `.claude/commands/decide.md`

- [ ] **Step 1: Create the command**

Create `.claude/commands/decide.md`:
```markdown
---
description: Decision support — compare options on value, risk, duty, and bias; save a decision entry
---

Follow `CLAUDE.md` and `SCHEMA.md`.

The decision:

$ARGUMENTS

Steps:
1. List the options. For each, compare: pros/cons, risks, alignment with my values, dharma/duty, long-term consequences, opportunity cost, and where emotional bias is distorting the view.
2. **Pattern-warning:** scan `problems/` and `decisions/` for similar past decisions/patterns; note repeated mistakes.
3. Give a clear recommendation with the reasoning, and what would make me reverse it.
4. Determine the next id (`decisions/DEC-<today>-NN`), save a decision entry per SCHEMA (frontmatter + the comparison as the body). Link `related_problems` if relevant.
5. Validate: `python tools/validate.py <file>`. Fix errors.
6. End with one immediate next action.
```

- [ ] **Step 2: Verify with a sample decision**

Create a throwaway `decisions/DEC-20260607-01-sample.md` to confirm the schema, then validate:
```markdown
---
id: DEC-20260607-01
type: decision
title: "Sample: accept offer vs stay"
created: 2026-06-07
status: open
options: ["Accept offer", "Stay"]
related_problems: [PRB-20260607-01]
values_considered: [security, growth]
subjects: [career_and_work, philosophy_and_wisdom]
life_areas: [career]
tags: [opportunity_cost]
---
# Comparison
Pros/cons, risk, values, dharma, long-term consequences, opportunity cost, emotional bias.
```

Run:
```bash
. .venv/bin/activate && python tools/validate.py decisions/
```
Expected: `All files valid.`

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/decide.md decisions/DEC-20260607-01-sample.md
git commit -m "feat: add /decide command and sample decision"
```

---

### Task 16: `/reflect` command

**Files:**
- Create: `.claude/commands/reflect.md`

- [ ] **Step 1: Create the command**

Create `.claude/commands/reflect.md`:
```markdown
---
description: Daily/weekly reflection check-in; detect hidden problems and patterns; save an entry
---

Follow `CLAUDE.md` and `SCHEMA.md`.

My reflection / what's on my mind:

$ARGUMENTS

Steps:
1. Read what I wrote. Reflect it back briefly and honestly.
2. Detect hidden problems, emotional patterns, and unresolved issues. **Pattern-warning:** compare with `problems/` and past `reflections/`.
3. If a real problem surfaces, offer to run `/solve` on it (and record its id in `detected_problems` once created).
4. Determine the next id (`reflections/REF-<today>-NN`), set `period` (daily/weekly), `mood` (from emotions vocab), `patterns_detected`, `people`. Save the entry (frontmatter + the reflection + what you noticed as body).
5. Validate: `python tools/validate.py <file>`. Fix errors.
6. End with the single thing most worth my attention right now.
```

- [ ] **Step 2: Verify with a sample reflection**

Create `reflections/REF-20260607-01-sample.md`:
```markdown
---
id: REF-20260607-01
type: reflection
created: 2026-06-07
period: daily
mood: [restless, tiredness]
subjects: [self_and_inner_life]
life_areas: [career, self]
detected_problems: [PRB-20260607-01]
patterns_detected: [avoidance]
people: [manager]
---
# Reflection
Felt scattered today; kept circling the job decision without acting.

# What I noticed
Avoidance pattern: analysis substituting for action. Links to PRB-20260607-01.
```

Run:
```bash
. .venv/bin/activate && python tools/validate.py reflections/
```
Expected: `All files valid.`

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/reflect.md reflections/REF-20260607-01-sample.md
git commit -m "feat: add /reflect command and sample reflection"
```

---

### Task 17: `/systems` command

**Files:**
- Create: `.claude/commands/systems.md`

- [ ] **Step 1: Create the command**

Create `.claude/commands/systems.md`:
```markdown
---
description: Build a preventive system (routine/rule/checklist/habit/boundary) for a recurring pattern
---

Follow `CLAUDE.md` and `SCHEMA.md`.

The recurring problem/pattern:

$ARGUMENTS

Steps:
1. Identify the recurring pattern. Pull the related problems from `problems/` (by id or by matching problem_types/tags) into `source_problems`.
2. Design ONE preventive system: choose `kind` (routine/rule/checklist/habit/boundary). Define the trigger, the exact steps/rule, how to follow it, and how/when to review it.
3. Determine the next id (`systems/SYS-<today>-NN`). Save the entry (frontmatter: `prevents_problem_types`, `addresses_patterns`, `source_problems`, `subjects`, `life_areas`, `tags`; body = the system).
4. Optionally link the system id back into the relevant problems' `systems` field.
5. Validate: `python tools/validate.py <file>`. Fix errors.
6. End with the first time I should run/apply this system.
```

- [ ] **Step 2: Verify with a sample system**

Create `systems/SYS-20260607-01-48-hour-rule.md`:
```markdown
---
id: SYS-20260607-01
type: system
title: "48-hour rule for big decisions"
created: 2026-06-07
status: active
kind: rule
prevents_problem_types: [decision]
addresses_patterns: [overthinking]
source_problems: [PRB-20260607-01]
subjects: [systems_and_thinking, career_and_work]
life_areas: [career]
tags: [decision_making]
---
# System
Trigger: any decision I have circled for more than a day.
Rule: write criteria, set a 48-hour deadline, decide at the deadline.
Review: weekly, during /reflect.
```

Run:
```bash
. .venv/bin/activate && python tools/validate.py systems/
```
Expected: `All files valid.`

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/systems.md systems/SYS-20260607-01-48-hour-rule.md
git commit -m "feat: add /systems command and sample system"
```

---

## Phase 5 — Final verification

### Task 18: End-to-end verification

- [ ] **Step 1: Validate the entire dataset**

Run:
```bash
. .venv/bin/activate && python tools/validate.py
```
Expected: `All files valid.`

- [ ] **Step 2: Run the full test suite**

Run:
```bash
. .venv/bin/activate && python -m pytest tools/tests/ -v
```
Expected: all tests pass (validator + export).

- [ ] **Step 3: Confirm command inventory**

Run:
```bash
ls .claude/commands/ | sort
```
Expected exactly: `actions.md add-knowledge.md analytics.md ask.md decide.md export.md outcome.md reflect.md search.md solve.md systems.md` (11 commands).

- [ ] **Step 4: Round-trip export**

Run:
```bash
. .venv/bin/activate && python tools/export.py 2026-06-07
python -c "import json; b=json.load(open('exports/export-2026-06-07.json')); print({k: len(v) for k,v in b.items()})"
```
Expected: counts show `problems: 1, knowledge: 2, reflections: 1, decisions: 1, systems: 1`.

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "test: end-to-end verification of LifeOS v1"
```

---

## Manual acceptance (run inside Claude Code, not automated)

After the tasks above, confirm the live behavior:
1. `/add-knowledge` with a pasted transcript → produces a schema-valid `KND-*` file (validator passes).
2. `/solve` a new problem → produces the full output format, fires pattern-warning against `PRB-20260607-01` if related, cites a `KND-*` doc, saves a valid `PRB-*` file.
3. `/outcome` on that problem → appends an outcome, updates status.
4. `/actions`, `/search`, `/ask`, `/analytics` → return sensible results from the seeded data.
5. `/export` → writes a JSON bundle.
6. Safety: describe a risk-laden problem → the agent leads with professional-help guidance.
