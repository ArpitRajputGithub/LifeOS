---
description: Look up how others have solved a similar problem from the precedents library
---

Follow `CLAUDE.md`.

Problem or query (or a problem id like `PRB-...`):

$ARGUMENTS

Steps:
1. Parse the input into controlled filters: `problem_types`, `subjects`, `tags`, and optionally `deeper_issue`. If given a `PRB-...` id, read that problem's frontmatter and use its fields.
2. Read `precedents/*.md`; rank by overlap of those controlled fields (most overlap first), breaking ties by body relevance.
3. For each top match, show: `id` + title, Approaches Tried, What Worked, What Didn't, the Lesson / Principle, and the `source`.
4. If nothing relevant matches, say so plainly and suggest `/add-precedent` to capture one.
5. End with the 1-2 most applicable precedents to act on now.
