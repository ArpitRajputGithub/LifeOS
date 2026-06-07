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
4. Validate: `python tools/validate.py <file>` (activate `.venv` first). Fix errors.
5. Tell me the recorded lesson and the pattern to remember next time.
