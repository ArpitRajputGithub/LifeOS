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
