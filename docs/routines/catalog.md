# Routine Catalog

This catalog names early routines for prompt-bounded work. Each routine is
practical enough to run manually or in an assistant session, but none claims
runtime automation today.

## Prompt Execution

| Field | Value |
| --- | --- |
| Purpose | Run one active prompt from startup through validated closeout. |
| When to use it | At the start of a fresh prompt-execution session. |
| Primary role | Orchestrator, often enacted by the operator and one assistant session. |
| Required inputs | Operator request, `AGENT.md`, active prompt, required docs, `git status --short`. |
| Expected outputs | Prompt deliverables, validation evidence, completion audit, next-prompt readiness statement. |
| Stop conditions | Prompt complete and audited; operator decision required; scope belongs to a future prompt; validation blocker is material. |
| Future automation potential | Assistant routine now; later checklist and manifest support. |

## Completion Audit

| Field | Value |
| --- | --- |
| Purpose | Compare required deliverables against actual artifacts and evidence. |
| When to use it | Before claiming prompt completion or accepting a lane result. |
| Primary role | Completion Auditor under the Orchestrator. |
| Required inputs | Active prompt, changed files, deliverable list, validation notes. |
| Expected outputs | Pass, warning, or blocker statement with file-level evidence. |
| Stop conditions | Every deliverable checked; a missing artifact blocks completion; unchecked risk is explicitly reported. |
| Future automation potential | Strong candidate for checklist and helper-script support. |

## Next-Prompt Preflight

| Field | Value |
| --- | --- |
| Purpose | Check whether the next prompt can start cleanly after current changes. |
| When to use it | During prompt-execution closeout when the active prompt requires it. |
| Primary role | Orchestrator or Next-Prompt Readiness Checker. |
| Required inputs | Next prompt, current docs, navigation, known residual risks. |
| Expected outputs | Ready, risky, or blocked readiness report with concrete reasons. |
| Stop conditions | Obvious blockers are fixed or reported; no future-prompt implementation begins. |
| Future automation potential | Assistant routine now; later structured readiness report support. |

## Bridge Decision

| Field | Value |
| --- | --- |
| Purpose | Decide whether a temporary handoff is worth creating. |
| When to use it | At closeout when a blocker, warning, or context dependency remains. |
| Primary role | Orchestrator. |
| Required inputs | Completion audit, next-prompt preflight, residual issues, repo state. |
| Expected outputs | Decision to create no handoff or create a narrow bridge artifact. |
| Stop conditions | No material blocker remains; handoff would only duplicate final-answer notes. |
| Future automation potential | Human-operated judgment with possible checklist support. |

## Handoff Generation

| Field | Value |
| --- | --- |
| Purpose | Write temporary continuation context for the next fresh session. |
| When to use it | Only after the bridge decision says a handoff materially helps. |
| Primary role | Handoff Composer under the Orchestrator. |
| Required inputs | Blocker or warning, affected files, current status, next action. |
| Expected outputs | `tmp/HANDOFF.md` or equivalent temporary bridge with concise context. |
| Stop conditions | No real blocker remains; durable docs already contain the needed context. |
| Future automation potential | Template-supported later; not automated now. |

## Repair-Session Startup

| Field | Value |
| --- | --- |
| Purpose | Start a targeted session to fix blockers or small gaps from prior work. |
| When to use it | After a completion audit, review, or handoff identifies bounded repair scope. |
| Primary role | Recovery Planner or Orchestrator. |
| Required inputs | Defect or blocker description, affected files, expected fix, stop conditions. |
| Expected outputs | Narrow repair plan, focused changes, validation evidence. |
| Stop conditions | Repair exceeds bounded scope; operator or Orchestrator authority is needed. |
| Future automation potential | Assistant routine now; later startup template support. |

## Promotion Review

| Field | Value |
| --- | --- |
| Purpose | Decide whether transient knowledge should become accepted work memory. |
| When to use it | When session notes, findings, or repeated observations may deserve durable docs. |
| Primary role | Operator or Orchestrator, with Lead proposals. |
| Required inputs | Candidate fact, source evidence, target artifact boundary, reason for durability. |
| Expected outputs | Promote, defer, or reject decision with target path if promoted. |
| Stop conditions | Evidence is weak; target boundary is unclear; operator approval is required. |
| Future automation potential | Judgment-heavy; possible checklist support only. |

## Run Closeout

| Field | Value |
| --- | --- |
| Purpose | Leave the repo ready for review or the next fresh session. |
| When to use it | At the end of prompt execution, repair, or review sessions. |
| Primary role | Orchestrator. |
| Required inputs | Git status, changed files, validation results, residual risks. |
| Expected outputs | Final summary, checks run, blockers or readiness statement, no unnecessary temporary state. |
| Stop conditions | Required checks cannot run; repo state contains unexplained task-related changes. |
| Future automation potential | Assistant routine now; later manifest and checklist support. |

## Promptset Health Inspection

| Field | Value |
| --- | --- |
| Purpose | Review the prompt sequence for missing prerequisites, drift, and readiness hazards. |
| When to use it | Periodically or before running a later prompt that depends on prior artifacts. |
| Primary role | Promptset Quality Inspector. |
| Required inputs | Prompt files, docs indexes, completed artifacts, known blockers. |
| Expected outputs | Findings, warnings, and suggested prompt repairs. |
| Stop conditions | Inspection would start implementing future prompts instead of reporting health. |
| Future automation potential | Partial helper support for inventories; critique remains judgment-heavy. |

## Commit Packaging

| Field | Value |
| --- | --- |
| Purpose | Group completed changes into coherent commits when the operator asks. |
| When to use it | After validation and operator commit approval. |
| Primary role | Commit Packager under the Orchestrator. |
| Required inputs | Git status, diff, prompt id, validation evidence, unrelated-change notes. |
| Expected outputs | Reviewable commit grouping and commit message summary. |
| Stop conditions | Operator has not asked for a commit; unrelated changes cannot be separated safely. |
| Future automation potential | Assistant routine now; helper support for summaries later. |

## Assumption Diff

| Field | Value |
| --- | --- |
| Purpose | Compare session assumptions against durable repo facts. |
| When to use it | Before writing doctrine, resolving blockers, or promoting memory. |
| Primary role | Lead, Orchestrator, or Dependency or Assumption Tracker. |
| Required inputs | Assumption list, source docs, current repo state. |
| Expected outputs | Confirmed assumptions, conflicts, unknowns, and required follow-up. |
| Stop conditions | Evidence is unavailable; resolving the difference needs operator direction. |
| Future automation potential | Assistant routine now; future report format possible. |

## Scope Boundary Check

| Field | Value |
| --- | --- |
| Purpose | Prevent active work from drifting into future prompts or unrelated refactors. |
| When to use it | Before editing, during review, and when a tempting adjacent task appears. |
| Primary role | Orchestrator, Lead, or Worker depending on boundary level. |
| Required inputs | Active prompt, constraints, artifact boundaries, current task brief. |
| Expected outputs | In-scope, out-of-scope, and escalation notes. |
| Stop conditions | Decision belongs to a higher role or the operator. |
| Future automation potential | Checklist support likely; full automation unlikely. |

## Validation Path Discovery

| Field | Value |
| --- | --- |
| Purpose | Identify cheap and relevant checks for the active change. |
| When to use it | Before final validation or when a prompt requires checks. |
| Primary role | Validator, Lead, or Worker. |
| Required inputs | Changed files, README or Makefile guidance, scripts, package metadata. |
| Expected outputs | Recommended commands, rationale, and any validation limits. |
| Stop conditions | Commands require unavailable dependencies or would exceed the prompt scope. |
| Future automation potential | Good candidate for helper-script support after command conventions exist. |
