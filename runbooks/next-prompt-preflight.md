# Next-Prompt Preflight

## Purpose

Check whether the immediate next prompt can start cleanly in a fresh session
after the current work.

## When To Use It

Use during closeout when the active prompt or `AGENT.md` asks for adjacent
prompt readiness. Use `templates/reports/readiness-report.md` when a durable
readiness report is needed.

## Required Context To Load

- Immediate next prompt only, such as `.prompts/PROMPT_09.txt`.
- Current docs and indexes that the next prompt names.
- `git status --short`.
- Current completion audit results.
- Any unresolved blocker or warning from validation.

## Roles Involved

- Next-Prompt Readiness Checker: inspects adjacent readiness.
- Orchestrator: decides whether to bridge, report risk, or stop.
- Operator: decides whether to start the next fresh session.

## Step-By-Step Procedure

1. Open only the immediate next prompt.
2. Read its startup instructions, required deliverables, constraints,
   validation, and endcap.
3. List the prerequisite docs, templates, directories, or terms it expects.
4. Check whether those prerequisites exist and are discoverable.
5. Check for obvious conflicts between current repo state and next-prompt
   instructions.
6. Confirm the current session has not already implemented next-prompt
   deliverables.
7. Run one lightweight adversarial pass: ask what would make the next prompt
   fail despite startup files existing. Record one concrete risk and its
   verdict impact, or state that none was found after checking startup
   instructions, deliverables, constraints, and validation.
8. Assign one readiness label:
   - `ready`: no obvious blocker or material warning.
   - `risky`: the next session can start, but a concrete warning should be
     carried in closeout.
   - `blocked`: a required prerequisite is missing or the next prompt cannot
     safely proceed.
9. Include one evidence sentence for `ready`, explaining why a fresh session
   can start cleanly.
10. If a blocker is a cheap navigation or terminology issue caused or revealed
   by the current session, apply a bridge fix.
11. If a blocker remains and the next session needs context beyond the final
   answer, create `tmp/HANDOFF.md` from `templates/handoffs/handoff.md`.

## Expected Artifacts

- A readiness label and concrete reasons in the final closeout.
- A short adversarial note covering one plausible soft failure or why no such
  risk was found.
- Optional readiness report from `templates/reports/readiness-report.md`.
- Optional bridge fix limited to navigation, terminology, or references.

## Validation Or Evidence

- The next prompt file was read.
- Named prerequisites were checked against repo paths.
- Any readiness warning cites the missing or risky artifact.
- No future-prompt implementation was performed during preflight.

## Stop Conditions

- The inspection would require reading beyond the immediate next prompt.
- The fix would implement next-prompt deliverables.
- Readiness depends on operator sequencing or a missing prompt file.

## Common Failure Modes

- Turning preflight into future planning.
- Fixing a next-prompt deliverable under the label of bridge work.
- Calling the next prompt blocked without checking whether a cheap index link
  solves the issue.
- Omitting concrete evidence for a `risky` or `blocked` label.
