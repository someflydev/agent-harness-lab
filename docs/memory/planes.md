# Memory Planes

Memory planes keep short-lived working context separate from durable shared
truth. A fact should live in the narrowest plane that supports the work.

## Ephemeral Run Memory

| Field | Guidance |
| --- | --- |
| Purpose | Holds immediate working notes while one assistant executes one prompt. |
| Expected lifespan | Minutes to the end of the active session. |
| Owner or reviewer | Current assistant; operator may inspect if needed. |
| Examples | Current command output, temporary checklist, local reasoning, unresolved question being investigated. |
| Repo location | Usually not persisted. If scaffolding is needed, use ignored `context/TASK.md`. |
| Must not store | Durable claims, raw transcript archives, unrelated notes, future prompt plans. |
| Promotion path | Summarize only verified facts into a run record, handoff, or durable doc when the prompt requires it. |

## Transient Bridge Or Handoff Memory

| Field | Guidance |
| --- | --- |
| Purpose | Carries material continuation context when a fresh session would otherwise lose a blocker or warning. |
| Expected lifespan | Until the repair or next session consumes it. |
| Owner or reviewer | Orchestrator creates it; next session or operator reviews and deletes or supersedes it. |
| Examples | `tmp/HANDOFF.md` with active prompt, blocker, affected files, validation already performed, next safe action. |
| Repo location | `tmp/HANDOFF.md` or another ignored file under `tmp/`. |
| Must not store | Doctrine, broad advice, raw transcripts, routine completion summaries, unreviewed durable memory. |
| Promotion path | If a handoff reveals a stable project rule, propose promotion through the promotion model; do not copy the handoff wholesale. |

## Accepted Work Memory

| Field | Guidance |
| --- | --- |
| Purpose | Records completed prompt outputs that are visible, reviewable, and accepted as part of the repo. |
| Expected lifespan | Durable until changed by later reviewed work. |
| Owner or reviewer | Operator accepts; Orchestrator audits prompt completion. |
| Examples | Prompt-required docs, templates, runbooks, examples, reports, and tests committed to the repo. |
| Repo location | The required artifact paths for the prompt, such as `docs/`, `templates/`, `examples/`, or scripts. |
| Must not store | Session chatter, local scratch files, unverifiable claims, implementation notes unrelated to the artifact. |
| Promotion path | Can feed project, doctrine, decision, or promoted knowledge memory when reviewed and summarized. |

## Project Memory

| Field | Guidance |
| --- | --- |
| Purpose | Captures stable, repo-local facts needed by future sessions. |
| Expected lifespan | Durable, but pruned when stale or superseded. |
| Owner or reviewer | Operator or explicit approved process; Orchestrator may propose. |
| Examples | Stable validation commands, repo layout facts, recurring guardrails, known pitfalls. |
| Repo location | Reviewed docs such as `README.md`, `AGENT.md`, `docs/`, and committed `context/MEMORY.example.md` scaffolds. |
| Must not store | Temporary task notes, one-run command output, personal preferences without project relevance. |
| Promotion path | Proposed by a session, reviewed against evidence, then added to the narrow durable artifact. |

## Doctrine Memory

| Field | Guidance |
| --- | --- |
| Purpose | States durable operating principles, vocabulary, and boundaries. |
| Expected lifespan | Long-lived; changes should be deliberate. |
| Owner or reviewer | Operator has final authority; Orchestrator may recommend. |
| Examples | Guardrails, principles, glossary terms, anti-patterns, artifact boundaries. |
| Repo location | `docs/doctrine/`, `docs/guardrails.md`, and closely related indexes. |
| Must not store | Step-by-step routine detail, one-off decisions, implementation logs, tool transcripts. |
| Promotion path | Requires clear evidence that a repeated rule or principle belongs in doctrine rather than a runbook or local memory. |

## Decision Memory

| Field | Guidance |
| --- | --- |
| Purpose | Preserves important choices, rejected alternatives, and acceptance rationale. |
| Expected lifespan | Durable while the decision remains relevant. |
| Owner or reviewer | Operator accepts; Orchestrator records or routes. |
| Examples | Choosing markdown-first artifacts over automation, rejecting vector indexes as a current requirement. |
| Repo location | Decision records when introduced, doctrine notes, reports, or prompt-required docs. |
| Must not store | Every minor edit choice, unsupported opinions, raw debate. |
| Promotion path | A candidate decision needs context, alternatives, evidence, and an accepted outcome. |

## Role-Specific Local Memory

| Field | Guidance |
| --- | --- |
| Purpose | Keeps role-local working context for an assigned lane without turning it into project truth. |
| Expected lifespan | The role assignment or lane session. |
| Owner or reviewer | The role owner; Lead or Orchestrator reviews outputs. |
| Examples | Lead lane notes, Worker task status, local validation findings before synthesis. |
| Repo location | Usually local or ignored runtime state; committed only as prompt-required reports or templates. |
| Must not store | Cross-project doctrine, broad scope changes, unreviewed promotion decisions. |
| Promotion path | Role owner flags candidates; Lead or Orchestrator reviews; operator or approved process accepts. |

## Promoted Validated Knowledge

| Field | Guidance |
| --- | --- |
| Purpose | Holds facts that moved from temporary observation into durable memory after review. |
| Expected lifespan | Durable until contradicted, stale, or replaced. |
| Owner or reviewer | Operator or explicit approved process accepts; assigned role records. |
| Examples | A verified command, a repeated failure mode, a stable file ownership rule. |
| Repo location | The most specific durable artifact: docs, runbooks, templates, reports, or future memory records. |
| Must not store | Facts without sources, speculative conclusions, metadata retained only because it exists. |
| Promotion path | Candidate, evidence, review, acceptance, targeted update, validation, pruning of superseded text. |

## Archival Findings And Experiment Memory

| Field | Guidance |
| --- | --- |
| Purpose | Preserves bounded findings from experiments, audits, or reports without turning every detail into doctrine. |
| Expected lifespan | Durable while useful for comparison or evidence; periodically pruned or summarized. |
| Owner or reviewer | Report author proposes; Orchestrator or operator reviews relevance. |
| Examples | Experiment summaries, validation reports, compatibility findings, rejected prototype notes. |
| Repo location | Future `reports/`, `findings/`, or prompt-required docs when introduced. |
| Must not store | Full raw logs by default, unrelated exploratory output, claims unsupported by the reported evidence. |
| Promotion path | Stable lessons can be proposed for project, doctrine, decision, or promoted knowledge memory. |
