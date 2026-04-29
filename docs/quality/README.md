# Quality

Quality docs define the checks and discipline used before a prompt-execution
session claims completion. They are intentionally lightweight: compare the
active prompt to the repo, run available local checks, state evidence plainly,
and avoid inventing proof that was not gathered.

## Start Here

- `validation-gates.md` - expected checks and evidence by prompt type.
- `promptset-quality.md` - what makes a prompt file ready for fresh-session
  execution.
- `audit-protocol.md` - how to compare implementation against prompt text.
- `review-severity.md` - severity levels for review findings.
- `definition-of-done.md` - `done`, `incomplete`, and `blocked` meanings.
- `failure-classification.md` - common quality failures and dispositions.

## Local Checks

Use these checks when they are relevant to the active prompt:

```sh
python3 scripts/ahl.py promptset
python3 scripts/ahl.py doctor
python3 scripts/ahl.py validate
python3 -m unittest tests/test_ahl.py
```

`validate` checks expected quality foundations and prompt numbering. It is not
a substitute for reading the prompt or auditing deliverables.
