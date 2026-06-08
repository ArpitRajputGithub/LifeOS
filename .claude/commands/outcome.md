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
5. **Offer to distill a precedent (privacy bridge):** ask me "Distill a shareable, de-identified precedent from this?" Only if I say yes:
   - Create `precedents/PRE-<today>-NN-<kebab-title>.md` per `SCHEMA.md`, generalized to the *pattern* — strip names, employer, exact dates/places, and any unique identifier; `source: "Distilled from lived experience."`
   - Show me the draft before saving (it goes to a public folder), then validate it.
   - Optionally record the new `PRE-...` id in the problem's `precedent_refs`.
6. Tell me the recorded lesson and the pattern to remember next time.
