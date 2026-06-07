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
