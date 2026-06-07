---
description: Ask the knowledge base a question; answer only from saved material, with citations
---

Follow `CLAUDE.md`.

Question:

$ARGUMENTS

Steps:
1. Identify relevant `knowledge/*.md` by `subjects`, `subtopics`, `problem_types`, `tags`, and body content.
2. Answer the question using those documents. Cite each source as `id` + title. Quote "Important Quotes or Concepts" where apt.
3. If the knowledge base has little or nothing relevant, say so plainly and clearly mark any general knowledge as NOT from my base — then suggest what to `/add-knowledge`.
4. End with the 2–3 most useful saved ideas on this topic.
