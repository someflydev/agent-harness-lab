---
name: trajectory-evaluator
description: Post-session audit skill. Run after any prompt Endcap to verify deliverables were completed, check whether the next prompt is READY/RISKY/BLOCKED, and suggest commit groupings. Use at closeout, not during implementation.
---

## When To Use

After completing a prompt session's implementation and running the standard
Endcap steps (audit, preflight, bridge decision, reset). Use this skill when
you want a structured read on whether the session was net-positive and whether
the next prompt is set up for success.

## Required Context

- The completed prompt file (`.prompts/PROMPT_XX.txt`)
- The next prompt file if it exists (`.prompts/PROMPT_YY.txt`)
- Current `git status --short` output
- Any validation output from this session
- Completion audit and next-prompt preflight notes from the Endcap

Do not load prior evaluation artifacts. Each evaluation is independent.

## Step-By-Step Behavior

### 1. Completion Audit

Compare the prompt's **Required Deliverables** list against what actually
exists in the repo right now. For each deliverable:

- DONE: file exists and contains the expected content
- PARTIAL: file exists but is missing required sections or is placeholder-only
- MISSING: file does not exist

Report the overall execution result:

- **PASS**: all deliverables done, validation passed
- **PARTIAL**: most deliverables done, minor gaps, no blockers
- **FAIL**: major deliverables missing or validation broken

### 2. Adjacency Check

Read the next prompt file. Ask:

- Does the repo state satisfy its Startup Instructions?
- Are any of its Required Deliverables blocked by missing foundations?
- Would a fresh session be able to run it cleanly today?

Report adjacency readiness:

- **READY**: next prompt can run cleanly from current repo state
- **RISKY**: next prompt may struggle; name the specific gap
- **BLOCKED**: next prompt cannot start without repair; name the blocker

This is the most important output. A PASS execution that leaves the next
prompt BLOCKED is a net-negative trajectory step.

### 3. Trajectory Rating

Rate the session across these dimensions:

| Dimension       | Options                                        |
|-----------------|------------------------------------------------|
| Execution       | PASS / PARTIAL / FAIL                          |
| Delta Quality   | +3 major / +2 clear / +1 minor / 0 / -1 / -2  |
| Adjacency Ready | READY / RISKY / BLOCKED                        |
| Drift           | NONE / MINOR / MAJOR                           |
| Handoff Usage   | NONE / JUSTIFIED / OVERUSED                    |
| Commit Quality  | STRONG / ACCEPTABLE / WEAK                     |

**Drift** means unintended regressions or scope creep relative to the prompt.
**Handoff Usage** rates whether `tmp/HANDOFF.md` was created appropriately.
**Commit Quality** rates how well the changes would group into a reviewable
commit if the operator asked now.

### 4. Commit Grouping Suggestion

If the operator is about to commit, suggest how to group the changes:

- Identify the natural logical groupings from `git status --short`
- Recommend one or more commit messages with `[PROMPT_XX]` prefixes
- Flag any changed files that look unrelated to this prompt's scope
- Do not stage or commit anything — suggestions only

### 5. Optional Evaluation Record

If the result contains a real signal worth preserving (PARTIAL or FAIL
execution, RISKY or BLOCKED adjacency, notable drift, or an insight about
the workflow), write a brief record to `tmp/SESSION_EVAL.md`:

```
# Session Eval — PROMPT_XX

Execution: PASS|PARTIAL|FAIL
Delta: +N
Adjacency: READY|RISKY|BLOCKED
Drift: NONE|MINOR|MAJOR
Handoff: NONE|JUSTIFIED|OVERUSED
Commits: STRONG|ACCEPTABLE|WEAK

Notes: <one or two sentences on what mattered>
```

Skip the file if the session was clean and unremarkable. Do not commit it.

## Expected Output

A brief structured report covering:

1. Completion audit summary (PASS / PARTIAL / FAIL with specifics)
2. Adjacency readiness verdict (READY / RISKY / BLOCKED with reason)
3. Trajectory rating table
4. Commit grouping suggestion (if changes exist)
5. Optional: `tmp/SESSION_EVAL.md` if there is a real signal

## Stop Conditions

- Do not perform bridge fixes or repairs as part of this skill. That is the
  Endcap's Bridge step.
- Do not create `tmp/HANDOFF.md` here. That belongs in the Endcap.
- Do not commit or stage files.
- Do not load prior evaluation records or attempt cumulative scoring.

## Safety Notes

- Evaluation artifacts in `tmp/` are transient. They are gitignored and must
  not be promoted to durable memory without review.
- This skill reads repo state but does not modify it.

## References

- `runbooks/completion-audit.md`
- `runbooks/next-prompt-preflight.md`
- `runbooks/commit-packaging.md`
- `docs/runtime/adjacent-prompt-readiness.md`
- `docs/runtime/execute-audit-preflight-bridge-reset.md`
- `prompt-templates/commit-package.md`
