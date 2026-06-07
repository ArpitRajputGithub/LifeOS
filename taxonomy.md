# Taxonomy — Controlled Vocabulary

This is the spine of analytics. Every controlled field in every entity must use a value from the lists below. The machine-readable source of truth is the `yaml` block at the bottom of this file (read by `tools/validate.py`). Extending a list is a deliberate edit to this file — never tag off-vocabulary silently.

## The 15 Subjects of Life
1. `self_and_inner_life`
2. `mind_and_psychology`
3. `body_and_health`
4. `relationships_and_people`
5. `career_and_work`
6. `money_and_resources`
7. `philosophy_and_wisdom`
8. `science_and_reality`
9. `society_and_civilization`
10. `practical_life_skills`
11. `creativity_and_expression`
12. `morality_ethics_and_character`
13. `life_stages_and_human_journey`
14. `problem_types`
15. `systems_and_thinking`

## Other controlled lists
- **life_areas** — practical areas of daily life.
- **problem_types** — the kind of problem.
- **deeper_issue** — the single dominant layer under the surface.
- **emotions** — controlled emotion words (so "fear" never fragments).
- **source_type** — where a knowledge document came from.
- **difficulty** — action difficulty.
- **status families** — problem / action / decision / system lifecycle states.
- **system kinds** — type of preventive system.
- **reflection periods** — cadence of a reflection.

`people` and free `tags` are NOT enumerated but ARE tracked for recurrence analytics.

```yaml
subjects:
  - self_and_inner_life
  - mind_and_psychology
  - body_and_health
  - relationships_and_people
  - career_and_work
  - money_and_resources
  - philosophy_and_wisdom
  - science_and_reality
  - society_and_civilization
  - practical_life_skills
  - creativity_and_expression
  - morality_ethics_and_character
  - life_stages_and_human_journey
  - problem_types
  - systems_and_thinking
life_areas:
  - self
  - health
  - relationships
  - family
  - friendships
  - career
  - money
  - education_learning
  - spirituality
  - home_environment
  - leisure_recreation
  - purpose_meaning
  - community_society
problem_types:
  - emotional
  - practical
  - decision
  - relationship
  - money
  - career
  - health
  - identity
  - discipline
  - moral
  - spiritual
  - crisis
  - repeated_pattern
deeper_issue:
  - emotional
  - practical
  - relational
  - financial
  - health
  - discipline
  - identity
  - spiritual
  - moral
  - decision
emotions:
  - anxiety
  - fear
  - anger
  - frustration
  - sadness
  - grief
  - guilt
  - shame
  - self_doubt
  - insecurity
  - loneliness
  - overwhelm
  - stress
  - restlessness
  - boredom
  - apathy
  - jealousy
  - resentment
  - hope
  - calm
  - confidence
  - gratitude
  - contentment
  - excitement
  - confusion
  - regret
  - disappointment
  - tiredness
source_type:
  - youtube_transcript
  - book
  - article
  - pdf
  - personal_note
  - reflection
difficulty:
  - easy
  - medium
  - hard
problem_status:
  - open
  - in_progress
  - resolved
  - abandoned
action_status:
  - not_started
  - in_progress
  - completed
  - failed
  - postponed
  - not_relevant
decision_status:
  - open
  - decided
  - reversed
system_status:
  - active
  - paused
  - retired
system_kind:
  - routine
  - rule
  - checklist
  - habit
  - boundary
reflection_period:
  - daily
  - weekly
```
