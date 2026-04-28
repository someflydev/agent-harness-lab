# Experiments

Experiments are bounded trials that test whether a prompt shape, routine,
role split, script, memory practice, or validation habit improves harness
execution quality. They answer a concrete workflow question and produce
evidence the operator can review.

## What Counts

An experiment has:

- a question or hypothesis
- a setup the operator can repeat or compare
- a prompt, routine, script, or practice under test
- controlled variables or known sources of variation
- observations and validation evidence
- a closeout decision

Normal prompt execution is not automatically an experiment. A prompt run
becomes experimental only when the session is intentionally testing a method,
recording useful evidence, and comparing the result against an expected
workflow outcome.

## When To Create One

Create an experiment when:

- a recurring workflow problem needs evidence before changing doctrine
- a new routine, role split, or template should be tested before broad use
- a script or check may reduce operator burden but has not earned automation
- a memory or promotion practice needs validation against fresh-session use
- two prompt shapes or closeout routines should be compared

Do not create an experiment for ordinary implementation work, one-off bug
fixes, raw transcript storage, or speculative notes that have no validation
plan.

## How To Run

1. Add a row to `catalog.md`.
2. Draft a plan from `templates/experiment-plan.md`.
3. Record evidence in `templates/experiment-log.md` or a similarly compact
   log.
4. Close the experiment with `templates/experiment-closeout.md`.
5. Decide whether the lesson stays local, becomes a finding, or is proposed
   for memory or doctrine promotion.

Keep artifacts small. Link to prompts, files, commands, reports, or commits
instead of copying raw session material.

## Closing Or Abandoning

Close an experiment when the question has enough evidence for a decision:
accepted, rejected, inconclusive, or superseded. Record the result, evidence,
follow-up decision, and any promotion recommendation.

Abandon an experiment when the question is no longer useful, the setup cannot
be reproduced, or the cost exceeds the value. Mark it abandoned in
`catalog.md`, explain why, and preserve only the facts that remain useful.

## Promotion Path

Experiment results do not become doctrine automatically. A recurring lesson
may become a finding in `../findings/` when evidence supports it. A finding may
then be proposed for durable memory or doctrine through the promotion model in
`../docs/memory/promotion-model.md`.

Promotion requires review, source evidence, scope, and an explicit target
artifact. The operator has final authority unless a later approved process says
otherwise.

## What Not To Store

Do not store:

- raw assistant transcripts by default
- secrets, credentials, or private operator data
- fake findings that look like real evidence
- broad metrics platforms or database exports
- provider-specific claims that were not part of the test
- session trivia that belongs in temporary notes or git history

