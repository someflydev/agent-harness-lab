# Completion Audit

## Purpose

Determine whether the active prompt is done by comparing its requirements to
actual files, docs, scripts, templates, and validation evidence.

## When To Use It

Use before claiming a prompt-execution, repair, or bridge session is complete.
Use the template at `templates/reports/completion-audit.md` when a durable audit
record is needed.

## Required Context To Load

- Active prompt file.
- `git status --short`.
- Changed files and any new files.
- Prompt validation section.
- Relevant indexes such as `docs/README.md` and `runbooks/README.md`.
- Any contract, report, handoff, or run templates referenced by the prompt.

## Roles Involved

- Completion Auditor: performs the comparison and states the result.
- Orchestrator: decides whether to fix, bridge, or stop.
- Worker or Lead: supplies implementation evidence when needed.

## Step-By-Step Procedure

1. Extract the prompt's required deliverables, content requirements,
   constraints, validation steps, and endcap steps.
2. For each required path, confirm whether it exists.
3. For each required content item, inspect the relevant file and identify the
   concrete section that satisfies it.
4. Compare constraints against the diff. Check for prohibited scripts,
   generated prompts, heavy runtime concepts, or future-prompt work.
5. Check navigation. Confirm new durable docs are discoverable from the nearest
   index.
6. Review validation evidence. Note commands run, inventories checked, and
   checks that could not run.
7. Check whether durable context should be updated. Context updates are
   justified only when the prompt introduced or changed workflow,
   architecture, command, convention, or repo-navigation knowledge that future
   fresh sessions need. Do not edit context files merely because the prompt
   ran; record `no context update needed` as an audit conclusion when no
   candidate exists.
8. Assign completion confidence:
   - `high`: deliverables, constraints, and validation evidence align cleanly.
   - `medium`: deliverables exist, but there is a named residual risk or
     skipped check.
   - `low`: evidence is thin, indirect, or dependent on assumptions.
9. Run one lightweight adversarial pass: ask what could make the prompt look
   complete while still failing its intent. Record one concrete risk and its
   verdict impact, or state that none was found after checking requirements,
   diff, and validation evidence.
10. Classify the result:
   - `done`: every required deliverable exists, explicit content is present,
     constraints are honored, and validation evidence is sufficient for the
     prompt.
   - `incomplete`: required work is missing or evidence has not been gathered,
     but the remaining work is known and can continue in the same session.
   - `blocked`: completion depends on missing prerequisites, operator input, a
     failed check that cannot be fixed in scope, or a scope conflict.
11. Fix incomplete in-scope gaps before closeout.
12. If blocked, decide whether to create `tmp/HANDOFF.md` using
   `bridge-fix-session.md`.

## Expected Artifacts

- A pass, warning, incomplete, or blocked statement in closeout.
- A completion confidence label with one evidence sentence.
- A context-update conclusion, either `no context update needed` or a concise
  candidate report naming possible targets such as `AGENT.md`, `CLAUDE.md`,
  `.context/`, or `context/`.
- A short adversarial note covering one plausible soft failure or why no such
  risk was found.
- Optional `templates/reports/completion-audit.md` record when the operator or
  prompt asks for one.
- Fixes for any small in-scope gaps found during the audit.

## Validation Or Evidence

- File inventory proves required paths exist.
- Read-back of changed docs proves required sections are present.
- Validation commands or manual checks are named.
- Constraints are checked against the actual diff, not memory.

## Stop Conditions

- A required deliverable is absent.
- A prompt constraint has been violated.
- Evidence cannot be gathered without unavailable tools or operator approval.
- The remaining work belongs to a future prompt.

## Common Failure Modes

- Auditing only the list of changed files.
- Declaring done while skipping the prompt's explicit validation section.
- Treating next-prompt readiness as proof that the active prompt is complete.
- Ignoring docs claims that overstate current automation.
