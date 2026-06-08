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
| precedent | `PRE-YYYYMMDD-NN` | `PRE-20260608-01` |
| action (inline child) | `ACT-<problemID>-NN` | `ACT-PRB-20260607-01-01` |
| outcome (inline child) | `OUT-<problemID>-NN` | `OUT-PRB-20260607-01-01` |

`NN` = 2-digit daily sequence: list same-day files of that type and increment.

## problem  (type: problem)
**Required:** `id, type, title, created, updated, status, subjects, life_areas, problem_types, deeper_issue, ratings`
**Optional:** `emotions, people, tags, root_cause, related_problems, knowledge_refs, precedent_refs, systems, actions, outcomes, immediate_next_action`
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

## precedent  (type: precedent)
**Required:** `id, type, title, created, subjects, problem_types, source`
**Optional:** `life_areas, deeper_issue, tags`
- `subjects` ⊆ subjects. `problem_types` ⊆ problem_types. `life_areas` ⊆ life_areas. `deeper_issue` ∈ deeper_issue. `source` is an attribution string (book, person, framework, "Distilled from lived experience", or a contributor).
- **Body sections (in order):** Situation, Approaches Tried, What Worked, What Didn't, Lesson / Principle, Source & Attribution.
- **Public/shared:** precedents live in `precedents/` (tracked). Never include personal identifying details.
