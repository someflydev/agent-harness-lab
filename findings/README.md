# Findings

Findings are reviewed lessons drawn from evidence. A finding is stronger than a
raw observation because it connects a recurring pattern, failure, workflow
improvement, or anti-pattern to traceable support and a bounded scope.

Findings are not automatic doctrine. They can inform prompt-authoring sessions,
routine changes, experiment design, or memory promotion, but each durable
change still needs review.

## Finding Vs. Observation

A raw observation says what happened in one run. A finding says what the lab
has learned from one or more observations and why that lesson may matter
beyond the original session.

Use a finding when:

- the same issue recurs across sessions or prompts
- an experiment closeout produced a useful lesson
- a report identifies a workflow improvement with evidence
- an anti-pattern is visible enough to warn future prompt authors
- a failure mode needs to feed a repair, runbook, or template change

Do not create a finding for speculation, unverified claims, raw transcripts, or
one-off notes that do not change future work.

## Evidence Required

A finding should include:

- source prompts, reports, experiment artifacts, files, commands, or commits
- the observed pattern or failure
- scope of applicability
- counter-evidence or limitations when known
- recommended next action
- promotion recommendation, if any

Evidence can be compact, but it must be traceable.

## Relationship To Memory Promotion

A finding may propose a memory or doctrine update, but it does not approve that
update by itself. Use `../docs/memory/promotion-model.md` and
`../templates/memory/promotion-record.md` when a lesson should become durable
memory.

If the lesson is useful only for one prompt or one experiment, keep it local.
If it affects prompt wording, use it as input to a future prompt-authoring
session. If it changes stable operating behavior, route it through promotion
review.

## Templates

- `templates/finding-record.md` - one reviewed lesson with evidence and
  disposition.
- `templates/pattern-observation.md` - compact record for recurring patterns,
  failures, workflow improvements, or anti-pattern sightings that may become a
  finding after review.

