# Session Lifecycle

A prompt-bounded session is a visible operating loop, not a hidden autonomous
run. It starts from grounded repo state, loads only relevant context, executes
one bounded prompt, validates the result, checks the immediate next prompt, and
closes without leaving accidental state behind.

## 1. Session Context Briefing

| Field | Guidance |
| --- | --- |
| Purpose | Ground the session in visible repo state before loading more context. |
| Inputs | Operator request, current branch when available, `git status --short`, expected runtime files or docs, obvious repo complexity signals. |
| Expected actions | Identify modified or untracked files, note whether required runtime docs exist, observe whether the task appears documentation-only, code-heavy, or mixed. |
| Outputs | Brief working-state statement and any user-change cautions. |
| Stop conditions | Repo state is unclear, required files are missing, or unrelated changes would be at risk. |
| Common mistakes | Assuming a clean tree, skipping visible state, or treating ignored local reference repos as implementation sources. |

## 2. Boot And Context Selection

| Field | Guidance |
| --- | --- |
| Purpose | Load enough context to execute the active prompt without over-reading. |
| Inputs | `AGENT.md`, `README.md`, `docs/guardrails.md`, active prompt, and docs explicitly named by the prompt. |
| Expected actions | Read required bootstrap docs, inspect hot spots before editing, and avoid scanning local reference repos unless asked. |
| Outputs | A scoped understanding of the prompt, constraints, deliverables, and likely hot spots. |
| Stop conditions | Prompt prerequisites are absent or the active prompt conflicts with higher-level guardrails. |
| Common mistakes | Reading the whole repo before knowing the task, importing reference-project identity, or missing prompt-specific constraints. |

## 3. Scope Confirmation

| Field | Guidance |
| --- | --- |
| Purpose | Confirm what this session owns and what belongs elsewhere. |
| Inputs | Active prompt goal, required deliverables, constraints, current docs, operator request. |
| Expected actions | Distinguish prompt execution from prompt authoring, repair, future templates, scripts, and memory work. |
| Outputs | Working scope and out-of-scope boundaries. |
| Stop conditions | The requested work needs operator approval, conflicts with another active change, or would generate future prompts without authorization. |
| Common mistakes | Quietly expanding into the next prompt, producing templates before the template prompt, or turning a repair into a redesign. |

## 4. Implementation

| Field | Guidance |
| --- | --- |
| Purpose | Create or update the artifacts required by the active prompt. |
| Inputs | Deliverable list, existing hot-spot files, relevant doctrine, role, routine, and runtime docs. |
| Expected actions | Edit surgically, preserve useful structure, keep artifacts practical, and avoid unrelated refactors. |
| Outputs | Prompt deliverables in the repo with navigation updated where needed. |
| Stop conditions | Implementation exceeds the prompt, requires missing prerequisites, or needs manual approval. |
| Common mistakes | Rewriting shared docs wholesale, creating empty structure with no responsibility, or building automation before the workflow is stable. |

## 5. Validation

| Field | Guidance |
| --- | --- |
| Purpose | Check that the changed artifacts exist and make coherent claims. |
| Inputs | Changed files, prompt validation section, relevant checks, docs indexes, file inventories. |
| Expected actions | Confirm required paths, inspect content for overstated claims, and run cheap relevant checks when available. |
| Outputs | Validation evidence and any limits on what was checked. |
| Stop conditions | A required deliverable is missing, claims are unsupported, or a check fails for a task-relevant reason. |
| Common mistakes | Treating file creation as sufficient, skipping index links, or claiming automation exists when only doctrine exists. |

## 6. Completion Audit

| Field | Guidance |
| --- | --- |
| Purpose | Compare the active prompt's requirements against actual results. |
| Inputs | Active prompt, changed paths, validation evidence, constraints. |
| Expected actions | Verify each required deliverable, confirm explicit distinctions and warnings, and identify residual risks. |
| Outputs | Pass, warning, or blocker summary for the active prompt. |
| Stop conditions | Any required deliverable is absent or an explicit prompt requirement is unmet. |
| Common mistakes | Auditing only the diff, ignoring constraints, or blending active-prompt completion with next-prompt readiness. |

## 7. Next-Prompt Preflight

| Field | Guidance |
| --- | --- |
| Purpose | Check whether the immediate next prompt can start in a fresh session. |
| Inputs | Next prompt, current repo navigation, prerequisite docs, known residual risks. |
| Expected actions | Inspect only the next prompt, look for missing prerequisites or navigation, and avoid implementing its scope. |
| Outputs | Ready, risky, or blocked readiness statement with concrete reasons. |
| Stop conditions | The next prompt requires artifacts that are missing or current docs create misleading direction. |
| Common mistakes | Planning the whole future promptset, doing the next prompt early, or treating active-prompt completion as automatic readiness. |

## 8. Bridge Decision

| Field | Guidance |
| --- | --- |
| Purpose | Decide whether a cheap fix or temporary handoff is justified. |
| Inputs | Completion audit, next-prompt preflight, residual blockers, repo state. |
| Expected actions | Fix small navigation or terminology blockers when clearly in scope; otherwise record only material continuation context. |
| Outputs | No bridge needed, bridge fix applied, or temporary handoff needed. |
| Stop conditions | The proposed bridge would become a second implementation phase or duplicate the final answer. |
| Common mistakes | Creating handoffs by default, hiding future work in bridge fixes, or leaving obvious cheap blockers unfixed. |

## 9. Handoff Creation When Justified

| Field | Guidance |
| --- | --- |
| Purpose | Preserve only continuation context that materially helps the next fresh session. |
| Inputs | Real blocker or non-trivial warning, affected files, next safe step, validation status. |
| Expected actions | Create `tmp/HANDOFF.md` only when durable docs and the final answer are insufficient. |
| Outputs | Concise temporary handoff with current status, blocker, evidence, and next action. |
| Stop conditions | No real blocker remains or the handoff would become durable memory without review. |
| Common mistakes | Storing raw transcript, writing broad advice, or creating handoffs for routine completion notes. |

## 10. Reset And Closeout

| Field | Guidance |
| --- | --- |
| Purpose | Leave the repo understandable for review and safe for the next fresh session. |
| Inputs | Git status, changed files, validation results, readiness statement, handoff decision. |
| Expected actions | Summarize changes, checks, readiness, residual risks, and note that no commit was made unless requested. |
| Outputs | Clean closeout statement and a repo state that does not depend on hidden chat context. |
| Stop conditions | Task-relevant command sessions are still running, changed files are unexplained, or validation has not been reported. |
| Common mistakes | Ending before checks finish, omitting next-prompt readiness, or leaving unneeded temporary artifacts. |
