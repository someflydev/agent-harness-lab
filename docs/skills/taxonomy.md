# Skill Taxonomy

This taxonomy names recurring capabilities in `agent-harness-lab`. The current
support labels are conservative:

- `conceptual` - named and useful, but not yet procedural.
- `human-operated` - performed by the operator or reviewer with judgment.
- `assistant-executed` - suitable for a coding assistant session with clear
  inputs and stop conditions.
- `template-supported` - expected to use a reusable markdown shape later.
- `script-supported` - expected to have a helper script later.
- `future-runtime-supported` - possible future automation after evidence shows
  the workflow is stable.

## Prompt Interpretation Skills

| Skill | For | Typical Role Users | Inputs | Outputs | Failure Signals | Current Support |
| --- | --- | --- | --- | --- | --- | --- |
| Requirement extraction | Turn the active prompt into concrete obligations. | Orchestrator, Lead, Prompt Runner, Completion Auditor. | Operator request, active prompt, required docs. | Required deliverables, constraints, validation needs. | Missed files, vague obligations, untracked constraints. | Assistant-executed. |
| Scope boundary detection | Identify what belongs to the active prompt and what belongs later. | Orchestrator, Lead, Worker, Workflow Critic. | Active prompt, guardrails, artifact boundaries, repo state. | In-scope list, out-of-scope list, escalation points. | Future-prompt work starts early, unrelated refactors, hidden assumptions. | Human-operated and assistant-executed. |
| Deliverable enumeration | Build a checkable list of files, docs, commands, and closeout duties. | Orchestrator, Lead, Worker, Completion Auditor. | Prompt deliverables, repo navigation, current file tree. | Checklist of expected artifacts and evidence. | Completion claims without file-level evidence. | Assistant-executed. |

## Repo Analysis Skills

| Skill | For | Typical Role Users | Inputs | Outputs | Failure Signals | Current Support |
| --- | --- | --- | --- | --- | --- | --- |
| Structural mapping | Understand where artifacts live and how docs connect. | Orchestrator, Lead, Repo Cartographer. | File tree, docs indexes, artifact boundaries. | Navigation map and likely hot spots. | Duplicate homes for the same concept, broken navigation. | Assistant-executed. |
| Convention detection | Preserve existing style, vocabulary, and document shape. | Lead, Worker, Convention Keeper, Reviewer. | Neighboring docs, README files, guardrails. | Local style notes and editing constraints. | Abrupt tone shifts, inconsistent headings, overbuilt structure. | Assistant-executed. |
| Assumption diffing | Compare current assumptions against durable repo facts. | Orchestrator, Lead, Dependency or Assumption Tracker. | Prompt claims, repo docs, git status, prior accepted artifacts. | Assumption list with confirmations, gaps, and conflicts. | Unverified claims becoming durable docs. | Human-operated and assistant-executed. |

## Execution Skills

| Skill | For | Typical Role Users | Inputs | Outputs | Failure Signals | Current Support |
| --- | --- | --- | --- | --- | --- | --- |
| Focused file editing | Make narrow edits inside an assigned artifact boundary. | Worker, Lead, Implementer. | Task brief, target files, style conventions. | Edited files and concise change notes. | Broad rewrites, unrelated cleanup, missing validation. | Assistant-executed. |
| Multi-file consistency editing | Keep linked docs aligned across indexes and cross-references. | Lead, Worker, Convention Keeper. | Related docs, navigation files, glossary terms. | Consistent terminology and links across files. | One file says a concept exists while indexes omit it. | Assistant-executed. |
| Scaffold generation | Create initial directory and file shapes for later content. | Worker, Lead, Implementer. | Artifact boundary, required paths, naming conventions. | Minimal files with clear purpose and placeholders only when useful. | Empty shells that imply maturity, directories with no navigation. | Assistant-executed. |
| Patch repair | Fix a bounded defect, omission, or mismatch after review. | Worker, Refiner or Repair Agent. | Review finding, affected files, expected outcome. | Small corrective patch and evidence. | Fix expands scope or hides the original issue. | Assistant-executed. |

## Validation Skills

| Skill | For | Typical Role Users | Inputs | Outputs | Failure Signals | Current Support |
| --- | --- | --- | --- | --- | --- | --- |
| Test command discovery | Find cheap, relevant validation commands without inventing new tooling. | Lead, Worker, Validator. | README files, Makefile, scripts directory, package metadata. | Candidate commands and rationale. | Running expensive or irrelevant checks, missing obvious checks. | Assistant-executed. |
| Smoke-test judgment | Decide when a light check is enough for the change risk. | Orchestrator, Lead, Validator. | Change scope, affected files, available commands. | Validation choice with limits. | Overclaiming confidence from weak evidence. | Human-operated and assistant-executed. |
| Artifact verification | Confirm required files exist and links or references are present. | Worker, Completion Auditor, Validator. | Deliverable checklist, file tree, docs index. | Existence and navigation evidence. | Missing files, stale links, untracked required artifacts. | Assistant-executed. |
| Prompt-vs-implementation cross-checking | Compare the prompt's requirements against actual repo changes. | Orchestrator, Completion Auditor, Reviewer. | Active prompt, changed files, validation notes. | Completion audit with gaps and warnings. | Completion before checking every deliverable. | Human-operated and assistant-executed. |

## Transition Skills

| Skill | For | Typical Role Users | Inputs | Outputs | Failure Signals | Current Support |
| --- | --- | --- | --- | --- | --- | --- |
| End-of-session audit | Verify deliverables, validation, and residual risks before closeout. | Orchestrator, Completion Auditor. | Active prompt, git status, changed files, checks. | Closeout audit and final readiness statement. | Final answer omits gaps or unchecked requirements. | Human-operated and assistant-executed. |
| Next-prompt preflight | Inspect the next prompt for obvious blockers caused by current work. | Orchestrator, Next-Prompt Readiness Checker. | Next prompt, current docs, navigation. | Ready, risky, or blocked statement with evidence. | Next prompt cannot find expected terms or files. | Assistant-executed. |
| Handoff writing | Create a temporary bridge only when the next session needs it. | Orchestrator, Handoff Composer, Lead. | Blocker, warning, changed state, next action. | Short handoff with context, risks, and continuation steps. | Routine completion notes turned into unnecessary state. | Template-supported future; human-operated now. |
| Commit summarization | Group changed files into coherent reviewable commit intent. | Orchestrator, Commit Packager, Lead. | Git status, changed files, validation evidence. | Commit grouping and summary text when operator asks. | One catch-all summary hides unrelated changes. | Human-operated and assistant-executed. |

## Process Intelligence Skills

| Skill | For | Typical Role Users | Inputs | Outputs | Failure Signals | Current Support |
| --- | --- | --- | --- | --- | --- | --- |
| Prompt quality critique | Identify ambiguity, missing prerequisites, and scope hazards in prompts. | Orchestrator, Promptset Quality Inspector, Workflow Critic. | Prompt text, prior docs, expected artifacts. | Findings and suggested prompt repairs. | Repeated session confusion from the same prompt shape. | Human-operated. |
| Session waste detection | Notice work that consumes context or time without improving deliverables. | Orchestrator, Session Economics Monitor. | Session plan, active edits, validation path. | Stop, narrow, or reset recommendation. | Long exploration without artifact movement. | Conceptual and human-operated. |
| Recovery planning | Define how to resume after blockers or partial execution. | Orchestrator, Recovery Planner, Lead. | Blocker, current repo state, incomplete deliverables. | Repair-session scope and stop conditions. | Restarting from scratch without preserving evidence. | Human-operated and assistant-executed. |
| Rate-limit-aware chunking | Break work into bounded fresh-session slices when tool or provider limits matter. | Operator, Orchestrator, Lead, Session Economics Monitor. | Promptset, expected cost, context size, known limits. | Smaller prompt slices or lane boundaries. | A session attempts too much and loses auditability. | Conceptual and human-operated. |
