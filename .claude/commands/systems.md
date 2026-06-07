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
5. Validate: `python tools/validate.py <file>` (activate `.venv` first). Fix errors.
6. End with the first time I should run/apply this system.
