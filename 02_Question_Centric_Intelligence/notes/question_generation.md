# Question Generation

## Question Birth

A question is born when a compression failure cannot be immediately resolved. The birth event records how and why the question entered the system.

## Birth Attributes

### birth_event

The event that created the question — typically a compression failure, though questions may also be born from splitting, merging, or deliberate formulation.

### triggering_observations

The observations that caused the compression failure and led to this question.

### initial_curiosity_debt

The curiosity pressure assigned at birth. Higher when the anomaly is surprising or conflicts strongly with the world model.

### confidence

Initial estimate of how well the world model explains the triggering observations. Low confidence at birth is common when compression has failed.

### novelty_score

A measure of the significance of the anomaly. How unexpected or disruptive the observation is relative to the current world model. Higher novelty suggests a more important question.

## Curiosity Debt Over Time

Repeated anomalies increase curiosity debt. When the same or related observations recur without resolution, pressure to investigate grows. A question that keeps resurfacing demands more attention than one that appeared once and faded.
