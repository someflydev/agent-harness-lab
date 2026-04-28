# Micro-Routine Library

Micro-routines are compact procedures that support runbooks, prompt execution,
repair, and closeout. They are manual or assistant-run steps today; helper
scripts belong to later prompts.

## Scope Boundary Check

Purpose: prevent active work from drifting into future prompts or unrelated
refactors.

1. Name the active prompt or operator request.
2. List required deliverables and explicit constraints.
3. Mark tempting adjacent tasks as `in scope`, `future prompt`, `repair`, or
   `operator decision`.
4. Before editing, confirm each intended file change maps to a required
   deliverable or cheap bridge fix.
5. Stop when the work would create scripts, prompts, templates, or runtime
   concepts owned by a later prompt.

Evidence: a short scope statement in the working notes or final closeout.

## Assumption Diff

Purpose: compare session assumptions with durable repo facts.

1. Write the assumption as a checkable sentence.
2. Identify the source that should confirm it, such as `README.md`, doctrine,
   runtime docs, or a prompt file.
3. Inspect the source and classify the assumption as `confirmed`, `conflict`,
   or `unknown`.
4. Resolve confirmed assumptions by using the source wording.
5. Escalate conflicts or unknowns when they affect deliverables.

Evidence: cited source files and any unresolved assumptions in closeout.

## Validation Path Discovery

Purpose: identify cheap, relevant checks for the current change.

1. Inspect the active prompt's validation section.
2. Check `README.md`, `Makefile`, scripts indexes, package metadata, or docs
   indexes for available checks.
3. Match checks to changed artifact types.
4. Prefer file inventories, link checks, and read-backs for docs-only changes.
5. Report unavailable or excessive checks instead of inventing runtime support.

Evidence: commands run, manual checks performed, and checks skipped with
reason.

## Prompt-Vs-Implementation Check

Purpose: verify the actual repo changes satisfy the active prompt.

1. Extract every required deliverable and content requirement from the prompt.
2. Map each item to a file path and section.
3. Confirm prohibited work is absent.
4. Confirm docs claims match current implementation level.
5. Classify missing items as incomplete or blocked.

Evidence: completion audit summary or `templates/reports/completion-audit.md`
when a record is needed.

## Next-Prompt Readiness Check

Purpose: inspect immediate next-prompt readiness without doing future work.

1. Read only the immediate next prompt.
2. List its startup docs, required deliverables, constraints, and endcap.
3. Check that prerequisite docs and templates exist and are linked where
   reasonable.
4. Label readiness as `ready`, `risky`, or `blocked`.
5. Apply only cheap navigation or terminology bridge fixes.

Evidence: readiness label and reasons in closeout or
`templates/reports/readiness-report.md`.

## Handoff Decision

Purpose: decide whether to create temporary continuation context.

1. Start from the completion audit and next-prompt preflight.
2. Ask whether a real blocker or non-trivial warning remains.
3. Ask whether the final answer is enough for the next session.
4. If not, write `tmp/HANDOFF.md` using `templates/handoffs/handoff.md`.
5. Keep the handoff concise and temporary.

Evidence: explicit `no handoff needed` statement or path to the created
handoff.

## Memory Promotion Review

Purpose: decide whether temporary knowledge should become durable memory.

1. State the candidate fact.
2. Name source evidence.
3. Choose a target artifact boundary or reject the candidate.
4. Decide `promote`, `defer`, or `reject`.
5. Use `templates/memory/promotion-record.md` when a record is needed.

Evidence: promotion decision, target path if promoted, and source evidence.

## Run Closeout

Purpose: leave the repo ready for review or the next fresh session.

1. Confirm required deliverables exist.
2. Confirm validation evidence is available.
3. Confirm navigation to new durable docs.
4. Check `git status --short`.
5. State changed files, checks, readiness, blockers, handoff decision, and
   commit status.

Evidence: final closeout message or `templates/session-closeout.md` when a
record is needed.

## Repair Triage

Purpose: decide whether a defect should be repaired now, handed off, or
escalated.

1. Name the defect and affected paths.
2. Identify the expected fixed state.
3. Decide whether the fix is bounded and within authority.
4. If bounded, use `runbooks/repair-session.md`.
5. If not bounded, create or update a handoff only when the next session needs
   material context.

Evidence: repair scope, stop condition, and validation check that will prove
the issue is fixed.
