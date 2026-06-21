# Question Lifecycle

Questions move through states over time. A question is not static — it may be created, pursued, set aside, revived, or closed.

## States

### NEW

A question has just been created, often from a compression failure or an observation that does not fit the world model. Not yet under active pursuit.

### ACTIVE

The question is live and eligible for attention. It may compete with other questions for exploration resources.

### INVESTIGATING

The system is actively working on this question — gathering observations, testing hypotheses, or revising the world model.

### PARTIALLY_RESOLVED

Some aspects of the question are answered, but meaningful uncertainty remains. The question may split into child questions or continue as a narrower form.

### RESOLVED

The question is satisfactorily answered. It no longer generates curiosity debt from the same source, though related questions may persist.

### DORMANT

The question is set aside without being resolved or abandoned. It retains identity and may accumulate curiosity debt if related anomalies recur.

### ABANDONED

The question is closed without resolution — deemed unanswerable, irrelevant, or superseded by other questions.

## Transitions

Questions may transition between any of these states as understanding changes. Examples:

- NEW → ACTIVE → INVESTIGATING → RESOLVED
- INVESTIGATING → PARTIALLY_RESOLVED → INVESTIGATING
- ACTIVE → DORMANT → ACTIVE
- DORMANT → INVESTIGATING
- ACTIVE → ABANDONED

Dormant questions may become active again when related observations recur, curiosity debt rises, or the world model changes enough to reopen the problem.
