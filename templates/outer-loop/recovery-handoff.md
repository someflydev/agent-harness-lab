# Outer Loop Recovery Handoff

- Run id: {{RUN_ID}}
- Plan id: {{PLAN_ID}}
- Status: {{STATUS}}
- Stop reason: {{STOP_REASON}}
- Next prompt: {{NEXT_PROMPT}}

## Recovery Recommendation

{{RECOVERY_RECOMMENDATION}}

## Operator Checks

- Confirm the worktree is clean before resuming.
- Review the run ledger and step summaries.
- Repair any blocked validation, gate, auth, quota, or driver condition first.
- Do not rerun completed prompt steps unless the operator explicitly chooses `--rerun`.

## Resume Command

```sh
python3 scripts/ahl.py outer resume --run {{RUN_ID}} --dry-run
```
