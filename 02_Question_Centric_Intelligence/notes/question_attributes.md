# Question Attributes

Each question is a structured entity, not a plain string. These attributes support tracking, prioritization, and lifecycle management.

## id

Unique identifier for the question. Stable across state changes and references from other questions or observations.

## text

Human-readable statement of what is unknown or unresolved. May be refined as the question evolves.

## created_at

Timestamp when the question was first registered, typically following a compression failure or explicit uncertainty.

## state

Current lifecycle state. One of: NEW, ACTIVE, INVESTIGATING, PARTIALLY_RESOLVED, RESOLVED, DORMANT, ABANDONED.

## curiosity_debt

Accumulated pressure to resolve this question. Increases when related anomalies are encountered and decreases as understanding improves.

## importance

Relative priority among questions. Influences which questions receive attention when resources are limited.

## confidence

Estimated degree to which the question has been answered. Low confidence may keep a partially resolved question active.

## parent_questions

Questions from which this question was derived — through splitting, refinement, or specialization.

## child_questions

Questions spawned from this one — narrower sub-questions or branches created during investigation.

## related_observations

Observations linked to this question, especially those that triggered or sustained it.

## times_encountered

Count of how often related anomalies or observations have resurfaced this question.

## last_revisited

Timestamp of the most recent time the system directed attention to this question.
