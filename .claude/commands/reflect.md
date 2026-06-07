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
5. Validate: `python tools/validate.py <file>` (activate `.venv` first). Fix errors.
6. End with the single thing most worth my attention right now.
