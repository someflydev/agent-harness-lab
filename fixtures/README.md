# Fixtures

This directory contains compact, artificial JSON examples for metadata shapes
used by `agent-harness-lab`. They are meant to exercise schemas and lightweight
local checks without claiming that any listed run, commit, or readiness result
actually happened.

## Contents

- `run-records/success.json` - successful prompt-bounded run record.
- `run-records/blocked.json` - blocked run record with skipped validation.
- `readiness-reports/ready.json` - ready next-prompt report.
- `readiness-reports/blocked.json` - blocked next-prompt report.
- `promptset-index/valid.json` - representative `ahl.py promptset --json`
  output.
- `lane-records/single-lane.json` - one artificial lane assignment and result.
- `traceability/prompt-to-commit.json` - artificial prompt-to-commit links.
- `traceability/working-tree-summary.json` - artificial
  `scripts/ahl.py trace --json` style working tree summary.
- `outer-loop/gates/pass.json` and `outer-loop/gates/blocked.json` -
  artificial post-prompt gate reports for continuation and stop cases.
- `portable-operator/` - artificial external target projects for portable
  status, lifecycle snippet, context-check, bootstrap-selection, and range
  dry-run tests.
- `assistant-drivers/codex.json`, `assistant-drivers/gemini.json`, and
  `assistant-drivers/pi.json` - compact examples for conservative driver
  contract records.
- `docs-links/valid/README.md` - markdown link fixture with resolvable local
  and ignored external links.
- `docs-links/broken/README.md` - markdown link fixture with an intentionally
  missing local target for docs-check tests.

## Validation Limits

Use:

```sh
python3 scripts/ahl.py fixtures check
```

The fixture check is intentionally lightweight and standard-library only. It
confirms that JSON parses, expected top-level fields exist, schema-backed
fixtures are paired with the expected schema file name, and referenced prompt
ids look like `PROMPT_01`. The working-tree trace summary fixture is checked
structurally because it documents helper output rather than a durable schema.
This is not a full JSON Schema validator and does not enforce every rule in
`schemas/*.schema.json`.

The docs-link fixtures are intentionally outside the repo-wide docs scan roots
so the broken case can remain checked in without causing normal navigation
validation to fail.
