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
