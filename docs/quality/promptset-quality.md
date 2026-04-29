# Promptset Quality

A prompt file is execution-ready when a fresh assistant session can run it
without relying on prior conversation.

## Criteria

- Clear scope: the prompt states the work type and boundary.
- Bounded deliverables: required paths and artifacts are named.
- Startup instructions: required first reads and state checks are listed.
- Constraints: prohibited work, dependency posture, and scope limits are
  explicit.
- Validation expectations: commands or manual checks are named.
- Endcap instructions: audit, preflight, bridge, reset, and commit posture are
  clear.
- Next-prompt readiness check: the immediate next prompt is inspected without
  implementing it.
- No hidden dependency on prior conversation: necessary context is in repo
  files or named docs.

## Common Readiness Problems

- Deliverables are described by theme but not by path.
- Validation says "test it" without naming likely commands or evidence.
- The prompt assumes unstated previous-session knowledge.
- Endcap instructions omit next-prompt readiness or handoff discipline.
- Constraints conflict with required deliverables.

Use `python3 scripts/ahl.py promptset` for filename numbering checks and
`python3 scripts/ahl.py validate` for structural readiness checks. Neither
command proves prompt prose quality by itself.
