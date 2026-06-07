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
