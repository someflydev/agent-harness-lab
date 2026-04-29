# Run Record

A run record captures compact facts about one prompt-bounded execution session.
It may live as a JSON artifact, a manifest section, or a final-answer checklist,
but the field names below should remain stable when structured.

## Fields

| Field | Type | Why it pays rent |
| --- | --- | --- |
| `prompt_id` | string | Connects the run to one prompt, such as `PROMPT_13`. |
| `prompt_batch_id` | string | Groups related promptset runs when the operator uses batches. |
| `run_id` | string | Provides a unique handle for manifests, reports, or examples. |
| `assistant_tool` | string | Records which assistant or local tool performed the work. |
| `permission_posture` | enum | Captures whether work was `read-only`, `workspace-write`, or `manual-required`. |
| `started_at` | timestamp | Supports ordering and elapsed-time review. |
| `ended_at` | timestamp or null | Marks whether the run closed cleanly. |
| `changed_files` | string array | Gives reviewers a direct artifact list. |
| `changed_directories` | string array | Helps summarize blast radius without reading every path. |
| `docs_changed` | boolean | Flags documentation-only or documentation-including work. |
| `tests_changed` | boolean | Shows whether test artifacts moved with code or script changes. |
| `validation_commands` | object array | Records commands run, exit status, and compact evidence. |
| `completion_audit_status` | enum | States whether required deliverables passed, warned, failed, or were skipped. |
| `next_prompt_ready` | boolean or null | Records immediate next-prompt readiness when checked. |
| `readiness_blockers` | string array | Names blockers or warnings that affect the next session. |
| `handoff_created` | boolean | Shows whether `tmp/HANDOFF.md` or equivalent was needed. |
| `follow_up_fix_required` | boolean | Separates done work from known repair needs. |
| `reusable_pattern_observations` | string array | Captures reviewed pattern candidates without promoting them automatically. |
| `associated_commit_hashes` | string array | Links the run to later commits when available. |

## Validation Command Shape

Each `validation_commands` entry should use:

- `command`: command text.
- `status`: `passed`, `failed`, or `skipped`.
- `exit_code`: integer or null.
- `summary`: short evidence statement.

## Boundaries

The run record is not a transcript and should not duplicate long command
output. It should point reviewers to repo files, git commits, reports, or
handoffs when more detail is needed.

## Fixtures And Lightweight Checks

Artificial examples live in `../../fixtures/`. They provide compact successful
and blocked run records, readiness reports, a promptset index, a lane record,
and a prompt-to-commit traceability record for local schema coverage.

Use:

```sh
python3 scripts/ahl.py fixtures check
```

This command performs structural fixture checks with the Python standard
library only. It confirms that JSON parses, expected top-level fields exist,
fixtures map to the expected schema files, and prompt id references look like
`PROMPT_19`. It is not a full JSON Schema validator.
