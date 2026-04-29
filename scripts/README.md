# Scripts

`scripts/ahl.py` is a small Python 3 helper CLI for local
`agent-harness-lab` work. It checks repository foundations, inspects prompt
filenames, scaffolds run and handoff artifacts from templates, and reports a
compact session context briefing.

It is intentionally dependency-free and uses only the Python standard library.
Future architecture docs may describe richer orchestration candidates, but
this script remains a small helper layer until repeated workflow evidence
justifies more.

## What It Does

- `doctor` checks expected repo foundations and ignore rules.
- `promptset` reports prompt filenames, numbers, duplicate numbers, gaps, and
  strict two-digit naming.
- `validate` checks expected quality foundations and promptset numbering in
  one lightweight gate.
- `resume` prints a read-only Session Context Briefing for visible repo state.
- `checkpoint` scaffolds local `context/*.md` files from examples or minimal
  built-ins.
- `scaffold-run` creates a timestamped run manifest from
  `templates/runs/run-manifest.md`.
- `new-handoff` creates `tmp/HANDOFF.md` from
  `templates/handoffs/handoff.md`.
- `metadata-example` prints a skeleton run record for metadata-aware closeout.

## What It Does Not Do

- It does not run prompts or call model providers.
- It does not inspect, ingest, or store raw assistant transcripts.
- It does not maintain a daemon or hidden runtime state.
- It does not replace human closeout, readiness, or promotion judgment.
- It does not provide graph, vector, provider, plugin, or server
  infrastructure.

## Examples

```sh
python3 scripts/ahl.py doctor
python3 scripts/ahl.py doctor --json
python3 scripts/ahl.py promptset
python3 scripts/ahl.py validate
python3 scripts/ahl.py resume --json
python3 scripts/ahl.py checkpoint
python3 scripts/ahl.py scaffold-run PROMPT_09 --assistant codex --permission-posture workspace-write
python3 scripts/ahl.py new-handoff
python3 scripts/ahl.py metadata-example PROMPT_13 --assistant codex --json
```

Generated files refuse to overwrite existing files unless the command exposes
and receives `--force`.

## JSON Stability

JSON output is meant for lightweight local checks. Stable top-level fields are:

- `doctor`: `ok`, `checks`, `problems`
- `promptset`: `ok`, `prompts`, `filenames`, `numbers`, `duplicates`, `gaps`,
  `strict_two_digit`, `malformed`
- `validate`: `ok`, `checks`, `problems`, `promptset`
- `resume`: `branch`, `head`, `clean`, `runtime_files`, `posture`,
  `recommendation`
- `checkpoint`: `ok`, `existing`, `scaffolded`, `stale`
- `scaffold-run`: `ok`, `created`, `run_id`, `prompt_id`
- `new-handoff`: `ok`, `created`
- `metadata-example`: `prompt_id`, `prompt_batch_id`, `run_id`,
  `assistant_tool`, `permission_posture`, `started_at`, `ended_at`,
  `changed_files`, `changed_directories`, `docs_changed`, `tests_changed`,
  `validation_commands`, `completion_audit_status`, `next_prompt_ready`,
  `readiness_blockers`, `handoff_created`, `follow_up_fix_required`,
  `reusable_pattern_observations`, `associated_commit_hashes`

Additional fields may be added when useful, but existing field meanings should
remain stable.

## Helper Tooling Boundary

This script supports the manual operator workflow described by the runbooks. It
surfaces repo state and creates inspectable markdown artifacts, but the human
operator still chooses the prompt, validates results, decides whether a handoff
is justified, and controls commits.
