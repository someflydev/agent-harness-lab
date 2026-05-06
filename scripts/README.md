# Scripts

`scripts/ahl.py` is a small Python 3 helper CLI for local
`agent-harness-lab` work. It checks repository foundations, inspects prompt
filenames, scaffolds run and handoff artifacts from templates, validates
deterministic dry-run scenario manifests, and reports a compact session context
briefing. It also scaffolds and checks reviewed memory promotion artifacts.
The repo Makefile provides a small operator console for the most common
commands; this script remains the underlying command source.

It is intentionally dependency-free and uses only the Python standard library.
Future architecture docs may describe richer orchestration candidates, but
this script remains a small helper layer until repeated workflow evidence
justifies more.

## What It Does

- `help` lists common operator console commands and supports `--json`.
- `doctor` checks expected repo foundations, ignore rules, and conservative
  safety hygiene signals such as stale handoffs, transcript dump paths, and
  secret-looking file names.
- `promptset` reports prompt filenames, numbers, duplicate numbers, gaps, and
  strict two-digit naming.
- `promptset lint` checks prompt structure readiness, immediate next-prompt
  references, and prompt registry alignment with transparent per-prompt scores.
- `validate` checks expected quality foundations and promptset numbering in
  one lightweight gate.
- `docs check` checks local markdown navigation, required index coverage, and
  registry path consistency without fetching external URLs.
- `registry list` and `registry check` list and validate curated registry JSON
  indexes.
- `driver list`, `driver check`, and `driver probe` list conservative
  assistant driver records, validate required driver fields, and run safe local
  capability probes without live model calls.
- `outer plan` creates an inspectable sequential batch plan under
  `runs/outer-loop/` without invoking assistants, staging, or committing.
- `outer dry-run` validates a batch plan's prompt files, driver record,
  validation commands, AHL checks, and stop conditions without invoking
  assistants.
- `dry-run list` and `dry-run check` list deterministic scenario manifests,
  validate their referenced artifacts, and check `dry-runs/PARITY.md` backing
  files.
- `experiment new`, `experiment check`, and `finding new` scaffold lightweight
  lab evidence artifacts and structurally check active experiment records.
- `memory propose`, `memory check`, and `memory decision` scaffold reviewed
  promotion candidates, validate queue structure, and create accepted or
  rejected decision records without promoting facts automatically.
- `resume` prints a read-only Session Context Briefing for visible repo state.
- `trace` summarizes prompt-related working tree changes and emits a run-record
  skeleton for closeout.
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
- It does not scan file contents for secrets or replace human review before
  committing.
- It does not approve memory promotions or make `memory/` a replacement for
  docs, findings, runbooks, templates, scripts, or tests.
- It does not maintain a daemon or hidden runtime state.
- It does not replace human closeout, readiness, or promotion judgment.
- It does not provide graph, vector, provider, plugin, or server
  infrastructure.
- Driver probes do not authenticate, send prompts, create sessions, or prove
  quota. They inspect the registry, `PATH`, and optional help output only.

## Examples

```sh
make help
make doctor
make test
python3 scripts/ahl.py help --json
python3 scripts/ahl.py doctor
python3 scripts/ahl.py doctor --json
python3 scripts/ahl.py promptset
python3 scripts/ahl.py promptset lint
python3 scripts/ahl.py promptset lint --json
python3 scripts/ahl.py validate
python3 scripts/ahl.py docs check
python3 scripts/ahl.py docs check --json
python3 scripts/ahl.py registry check
python3 scripts/ahl.py registry list --json
python3 scripts/ahl.py driver list
python3 scripts/ahl.py driver list --json
python3 scripts/ahl.py driver check
python3 scripts/ahl.py driver probe codex --help-only --json
python3 scripts/ahl.py outer plan --from PROMPT_33 --count 3 --driver codex --model gpt-5.5 --reasoning medium --json
python3 scripts/ahl.py outer plan --next 10 --driver codex --json
python3 scripts/ahl.py outer dry-run --plan runs/outer-loop/<plan-id>/plan.json --json
python3 scripts/ahl.py dry-run list
python3 scripts/ahl.py dry-run check sequential-prompt-run
python3 scripts/ahl.py dry-run check --all --json
python3 scripts/ahl.py experiment new closeout-check
python3 scripts/ahl.py experiment check --json
python3 scripts/ahl.py finding new repeated-closeout-gap
python3 scripts/ahl.py memory propose stable-cli-boundary
python3 scripts/ahl.py memory check --json
python3 scripts/ahl.py memory decision stable-cli-boundary --accepted
python3 scripts/ahl.py resume --json
python3 scripts/ahl.py trace PROMPT_20 --json
python3 scripts/ahl.py checkpoint
python3 scripts/ahl.py scaffold-run PROMPT_09 --assistant codex --permission-posture workspace-write
python3 scripts/ahl.py new-handoff
python3 scripts/ahl.py metadata-example PROMPT_13 --assistant codex --json
```

Generated files refuse to overwrite existing files unless the command exposes
and receives `--force`.

## Makefile Console

The stable Makefile targets are:

- `help`
- `doctor`
- `resume`
- `checkpoint`
- `promptset`
- `lint-prompts`
- `check-docs`
- `test`
- `domain-pack`
- `trace`
- `dry-run`
- `registry`
- `memory-check`
- `experiment-check`

Most targets are read-only wrappers around `scripts/ahl.py`. `checkpoint`
scaffolds missing `context/*.md` files and refuses to overwrite them through
the Makefile path. Use direct script commands for JSON output, non-default
arguments, `--force`, or scaffolds such as `scaffold-run`, `new-handoff`,
`memory propose`, `memory decision`, `experiment new`, and `finding new`.

## JSON Stability

JSON output is meant for lightweight local checks. Stable top-level fields are:

- `doctor`: `ok`, `checks`, `problems`
- `help`: `ok`, `commands`, `makefile_targets`
- `promptset`: `ok`, `prompts`, `filenames`, `numbers`, `duplicates`, `gaps`,
  `strict_two_digit`, `malformed`
- `promptset lint`: `ok`, `prompt_dir`, `summary`, `problems`, `numbering`,
  `registry`, `prompts`
- `validate`: `ok`, `checks`, `problems`, `promptset`
- `docs check`: `ok`, `scan_roots`, `anchors_validated`, `checks`,
  `problems`, `scanned_files`, `links`, `missing_links`, `navigation`,
  `registry`
- `registry list`: `ok`, `registries`
- `registry check`: `ok`, `checks`, `problems`, `registries`
- `driver list`: `ok`, `drivers`, `checks`, `problems`
- `driver check`: `ok`, `drivers`, `checks`, `problems`
- `driver probe`: `ok`, `drivers`, `checks`, `problems`, `probe`
- `outer plan`: `ok`, `plan_id`, `created_at`, `requested_range`, `prompts`,
  `driver`, `model`, `reasoning`, `permission_posture`,
  `required_ahl_checks`, `stop_conditions`, `commit_policy`,
  `transcript_capture_policy`, `run_artifact_dir`, `problems`, and `artifact`
  when creation succeeds
- `outer dry-run`: `ok`, `plan_id`, `steps`, `problems`; each step includes
  stable `prompt_id`, `path`, `status`, `validation_commands`, and `problems`
- `dry-run list`: `ok`, `scenario_count`, `scenarios`
- `dry-run check`: `ok`, `scenario_count`, `checked`, `results`, `parity`,
  `problems`; each result includes stable `id`, `status`, and `problems`
- `experiment new`: `ok`, `slug`, `directory`, `created`, `forced`,
  `catalog_updated`
- `experiment check`: `ok`, `directory`, `checks`, `problems`, `experiments`;
  each experiment includes stable `id`, `path`, `status`, and `problems`
- `finding new`: `ok`, `slug`, `directory`, `created`, `forced`
- `memory propose`: `ok`, `slug`, `created`, `forced`
- `memory check`: `ok`, `checks`, `problems`, `candidates`; each candidate
  includes stable `path`, `status`, and `problems`
- `memory decision`: `ok`, `candidate`, `decision`, `created`, `forced`
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

Additional fields may be added when useful, but existing field meanings should
remain stable.

## Helper Tooling Boundary

This script supports the manual operator workflow described by the runbooks. It
surfaces repo state and creates inspectable markdown artifacts, but the human
operator still chooses the prompt, validates results, decides whether a handoff
is justified, controls commits, and reviews any finding or promotion candidate.
