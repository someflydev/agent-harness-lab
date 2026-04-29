# Audit Protocol

Use this protocol before claiming a prompt is complete.

## Procedure

1. Extract required deliverables, content requirements, constraints,
   validation steps, and endcap steps from the active prompt.
2. Check every required path exists.
3. Read changed hot-spot files and new durable docs.
4. Match each content requirement to a concrete file section.
5. Compare constraints against the actual diff.
6. Run the prompt's validation commands when available.
7. Run cheap adjacent checks when they directly support the prompt.
8. Inspect the immediate next prompt for readiness.
9. Classify the result as `done`, `incomplete`, or `blocked`.

## Evidence Rules

- Prefer command output, file paths, and section names over memory.
- State skipped checks and why they were skipped.
- Do not use next-prompt readiness as proof of active-prompt completion.
- Fix small in-scope gaps before closeout.
- Create `tmp/HANDOFF.md` only when a real blocker or non-trivial warning
  remains.
