# Helper Scripts

`scripts/ahl.py` provides the first lightweight helper layer for
`agent-harness-lab`. It is a local Python 3 CLI built on the standard library.
Its job is to make manual prompt execution easier to inspect, not to automate
agent work.

## Commands

```sh
python3 scripts/ahl.py doctor
python3 scripts/ahl.py promptset
python3 scripts/ahl.py validate
python3 scripts/ahl.py registry check
python3 scripts/ahl.py registry list --json
python3 scripts/ahl.py resume
python3 scripts/ahl.py trace PROMPT_20 --json
python3 scripts/ahl.py checkpoint
python3 scripts/ahl.py scaffold-run PROMPT_09
python3 scripts/ahl.py new-handoff
python3 scripts/ahl.py metadata-example PROMPT_13
```

Each command supports `--json` where machine-readable output is practical.

## Behavior

- `doctor` checks expected foundations such as `README.md`, `AGENT.md`,
  `.prompts/`, `docs/`, `runbooks/`, `templates/`, and relevant `.gitignore`
  entries. It also performs conservative safety hygiene checks for stale
  handoffs, transcript dump paths, and secret-looking file names.
- `promptset` reports prompt filenames and numbering health without parsing
  prompt prose.
- `validate` combines prompt numbering with expected quality foundations,
  including docs, runbooks, templates, helper scripts, and helper tests.
- `registry check` validates curated registry JSON parsing, required fields,
  referenced paths, and prompt registry ordering.
- `registry list` reports registry files and item counts.
- `resume` prints a read-only Session Context Briefing from git state,
  runtime-note files, and local `tmp/*.md` counts.
- `trace` summarizes prompt-related working tree changes, git branch and HEAD
  when available, docs/tests/templates flags, handoff presence, and a
  run-record skeleton for closeout.
- `checkpoint` reports and scaffolds local `context/TASK.md`,
  `context/SESSION.md`, and `context/MEMORY.md`.
- `scaffold-run` creates a timestamped run manifest from the run template.
- `new-handoff` creates `tmp/HANDOFF.md` from the handoff template.
- `metadata-example` prints a skeleton run record using the fields documented
  in `metadata/run-record.md`.

Generated artifacts refuse to overwrite existing files unless the command has
an explicit `--force` flag and it is supplied.

## JSON Output

The JSON shapes are intentionally compact. Stable top-level fields include:

- `doctor`: `ok`, `checks`, `problems`
- `promptset`: `ok`, `prompts`, `filenames`, `numbers`, `duplicates`, `gaps`,
  `strict_two_digit`, `malformed`
- `validate`: `ok`, `checks`, `problems`, `promptset`
- `registry check`: `ok`, `checks`, `problems`, `registries`
- `registry list`: `ok`, `registries`
- `resume`: `branch`, `head`, `clean`, `runtime_files`, `posture`,
  `recommendation`
- `trace`: `prompt_id`, `prompt_file`, `prompt_file_exists`, `branch`, `head`,
  `git`, `changed_files`, `changed_paths`, `changed_directories`,
  `docs_changed`, `tests_changed`, `templates_changed`, `handoff_exists`,
  `suggested_run_record_missing_fields`, `run_record_skeleton`
- `checkpoint`: `ok`, `existing`, `scaffolded`, `stale`
- `scaffold-run`: `ok`, `created`, `run_id`, `prompt_id`
- `new-handoff`: `ok`, `created`
- `metadata-example`: `prompt_id`, `prompt_batch_id`, `run_id`,
  `assistant_tool`, `permission_posture`, `started_at`, `ended_at`,
  `changed_files`, `changed_directories`, `docs_changed`, `tests_changed`,
  `validation_commands`, `completion_audit_status`, `next_prompt_ready`,
  `readiness_blockers`, `handoff_created`, `follow_up_fix_required`,
  `reusable_pattern_observations`, `associated_commit_hashes`

These fields are suitable for small local checks and smoke tests. The script is
not a provider integration surface.

## Boundary

The helper CLI supports the human-assisted workflow described in the runbooks.
It does not choose prompts, run assistants, call paid model APIs, store raw
assistant transcripts, create long-running processes, or decide when work is
complete. The operator and active prompt remain the source of scope and
authority.
