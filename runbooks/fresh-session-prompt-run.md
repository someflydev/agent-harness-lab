# Fresh-Session Prompt Run

## Purpose

Run exactly one active `.prompts/PROMPT_XX.txt` file from startup through
validated closeout in a fresh assistant session.

## When To Use It

Use this for normal prompt-execution work when the operator says to run a
specific prompt file.

Do not use it for prompt generation, broad promptset review, unbounded repair,
or commit packaging unless the active prompt explicitly asks for those actions.

## Required Context To Load

- `AGENT.md`
- `README.md`
- `docs/guardrails.md`
- The active prompt file named by the operator.
- Docs explicitly named by the active prompt.
- Existing hot-spot files before editing them.
- `git status --short` before editing and again near closeout.

Examples of what not to load by default:

- Every prompt in `.prompts/`.
- Local reference repos such as `agent-context-base`, `pi-mono`, or
  `claw-code`.
- Future-prompt docs except the immediate next prompt during preflight.
- Raw transcript from earlier sessions unless it was promoted into repo files
  or summarized in an active `tmp/HANDOFF.md`.

## Roles Involved

- Operator: starts the session, names the active prompt, and decides whether to
  commit.
- Orchestrator: keeps scope, closeout, bridge, and reset on track.
- Worker or Lead: implements bounded deliverables when the prompt requires
  execution work.
- Completion Auditor: checks actual output against prompt requirements.
- Next-Prompt Readiness Checker: inspects the immediate next prompt only.

## Step-By-Step Procedure

1. Start a fresh assistant session from the current repo state.
2. Run `git status --short` and note modified or untracked files.
3. Load `AGENT.md`, `README.md`, the active prompt, and narrow required docs.
4. Confirm the active prompt scope by naming required deliverables,
   constraints, and explicit non-goals.
5. Read existing files that will be edited, especially hot spots.
6. Implement only the active prompt. Leave future-prompt deliverables for their
   own sessions.
7. Validate with the prompt's required checks and any cheap relevant artifact
   checks.
8. Run the completion audit in `completion-audit.md`.
9. Inspect the immediate next prompt using `next-prompt-preflight.md`.
10. Apply a bridge fix only if it is cheap, directly tied to readiness, and not
    future-prompt implementation.
11. Create `tmp/HANDOFF.md` from `templates/handoffs/handoff.md` only if a real
    blocker or non-trivial warning would otherwise be lost.
12. Reset cleanly with `run-closeout.md`; do not commit unless the operator
    explicitly asks.

## Expected Artifacts

- Active prompt deliverables in their required paths.
- Validation evidence summarized in the final closeout.
- A readiness statement for the immediate next prompt.
- Optional `tmp/HANDOFF.md` only when justified.
- No new helper scripts unless the active prompt owns scripts.

## Validation Or Evidence

- Required paths exist.
- `docs/README.md` or other relevant indexes link to new durable docs.
- Claims in docs match current capabilities.
- Checks named by the prompt were run or clearly reported as not run.
- `git status --short` shows only expected task-related changes plus any
  preserved unrelated user changes.

## Stop Conditions

- All active prompt deliverables are complete and audited.
- A missing prerequisite blocks work.
- Validation fails for a task-relevant reason.
- The next step belongs to a future prompt or requires operator approval.
- Repair scope is no longer bounded.

## Common Failure Modes

- Loading too much future context and drifting into later prompts.
- Treating file creation as completion without checking content requirements.
- Creating `tmp/HANDOFF.md` for routine summary notes.
- Rewriting shared docs instead of updating them surgically.
- Committing without an explicit operator request.
