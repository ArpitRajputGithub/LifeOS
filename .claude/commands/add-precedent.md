---
description: Author a shareable precedent (how a problem was solved) into the public library
---

Follow `CLAUDE.md` and `SCHEMA.md`. The material (a book idea, a story, advice) is below (or ask me for it if empty):

$ARGUMENTS

Steps:
1. Determine the next id: list `precedents/PRE-<today>-*.md`, increment `NN` (today = current date `YYYYMMDD`).
2. Classify into the precedent schema: `subjects` (from the 15), `problem_types`, `life_areas`, `deeper_issue`, `tags`, and a `source` attribution. Use ONLY `taxonomy.md` values for controlled fields.
3. Write the body sections: Situation, Approaches Tried, What Worked, What Didn't, Lesson / Principle, Source & Attribution.
4. **Public folder:** `precedents/` is tracked/shared — do NOT include personal identifying details about real people. Generalize to the pattern.
5. Save as `precedents/PRE-<today>-NN-<kebab-title>.md`.
6. Validate: `python tools/validate.py <new file>` (activate `.venv` first). Fix any errors before finishing.
7. Confirm to me: the id, title, and how it was classified.
