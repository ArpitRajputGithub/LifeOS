---
description: Solve a life problem with the full LifeOS process and save a tracked entry
---

Follow `CLAUDE.md` (the 13-step process, output format, safety rule, data rules) and `SCHEMA.md`.

My problem:

$ARGUMENTS

Steps:
1. If the problem hits a safety trigger (serious mental-health/medical/legal/financial risk or harm), give the safety guidance FIRST, then continue if appropriate.
2. Run steps 1–11 of the process and respond in the Default Output Format.
3. **Pattern-warning:** scan `problems/` for similar past problems (by subjects/problem_types/tags/people). If found, fill "Similar Past Problems" with the matched `id`(s), the repeating pattern, and what to do differently.
4. **Knowledge:** scan `knowledge/` for relevant docs; cite them by id+title in "Relevant Wisdom"; record their ids in `knowledge_refs`.
5. **Precedents (How Others Solved This):** match the problem against `precedents/` by subjects/problem_types/tags; summarize the most relevant in the "How Others Have Solved This" section, citing `PRE-id` + source; record matched ids in `precedent_refs`.
6. If `recurrence_likelihood >= 7`, suggest creating a preventive system via `/systems`.
7. Determine the next id (`problems/PRB-<today>-*.md`, increment NN) and save the full entry: frontmatter per SCHEMA + the body = the output format sections.
8. Validate: `python tools/validate.py <new file>` (activate `.venv` first). Fix errors before finishing.
9. End by telling me the saved id and the single Immediate Next Action.
