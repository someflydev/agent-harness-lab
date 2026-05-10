# Scripts

`scripts/ahl.py` is a small Python 3 helper CLI for local
`agent-harness-lab` work. It checks repository foundations, inspects prompt
filenames, scaffolds run and handoff artifacts from templates, validates
deterministic dry-run scenario manifests, and reports a compact session context
briefing. It also scaffolds and checks reviewed memory promotion artifacts and
can run a dry-run-default sequential outer-loop plan through an explicitly
selected assistant driver. It can also create prompt-scoped commit plans,
inspect recent commit-message hygiene, and execute reviewed plans only when
the operator supplies an explicit approval flag.
The repo Makefile provides a small operator console for the most common
commands; this script remains the underlying command source.

It is intentionally dependency-free and uses only the Python standard library.
Future architecture docs may describe richer orchestration candidates, but
this script remains a small helper layer. The phase-two outer-loop baseline is
bounded local support, not a daemon or provider platform.

The portable-operator extension is documented in
`../docs/portable-operator/`. It adds an explicit distinction between AHL home
and a target project repo. `project locate`, `project status`, `lifecycle
snippets`, `lifecycle context-check`, `lifecycle run-range`, and `commit
check` are the read-only portable commands for that distinction; most older
commands still resolve paths from the current working directory and assume it
is the AHL repo.
Portable helpers produce snippets, prompt payloads, plans, reports, and
validation helpers; the operator or chosen assistant CLI executes prompt work.
They do not require provider credentials, network access, paid APIs, or
machine-readable subscription quota checks.
`portable rehearsal` composes those helpers against artificial fixtures and an
isolated temporary git repository to provide offline capstone evidence.

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
  capability probes without live model calls. The Pi record is an external
  harness candidate and is marked `manual-confirmation-required` for live use
  until the local command shape and output contract are verified.
- `project locate` reports AHL home and target project root discovery from the
  current directory or `--project` without editing files or invoking
  assistants.
- `project status` reports the target project's git state, `.prompts/`
  diagnostics, bootstrap/context file presence, recent prompt-prefixed
  commits, and likely next prompt inference without editing files or invoking
  assistants.
- `lifecycle snippets` prints reusable run, audit/next-readiness/context,
  commit-plan, make-commits, commit-check, and optional repair snippets for a
  single target-project prompt without editing files or invoking assistants.
- `lifecycle context-check` inspects target-project changed paths and suggests
  conservative context-update review questions without editing bootstrap,
  `.context/`, `context/`, or target-project files.
- `lifecycle run-range` dry-runs a prompt range in a target project, validates
  strict prompt files, and prints or explicitly writes a one-prompt-at-a-time
  phase plan without invoking assistants or editing target files.
- `portable rehearsal` runs the deterministic portable-operator fixture
  rehearsal, including project discovery, status, snippets, context-check,
  run-range, gapped diagnostics, and temporary git commit-check evidence.
- `outer plan` creates an inspectable sequential batch plan under
  `runs/outer-loop/` without invoking assistants, staging, or committing.
- `outer dry-run` validates a batch plan's prompt files, driver record,
  validation commands, AHL checks, and stop conditions without invoking
  assistants.
- `outer run` builds bounded prompt payloads from a plan, writes a run ledger,
  defaults to dry-run, and invokes supported assistant CLIs only when
  `--execute` is passed. The `manual` driver records the expected operator
  action without invoking a model.
- `outer status`, `outer resume`, and `outer recovery-handoff` read run
  ledgers, report completed, failed, skipped, and pending steps, plan dry-run
  resume points, refuse dirty or unsafe worktrees, and create recovery handoffs
  from a template when needed.
- `outer gate` collects post-prompt gate evidence from git status, prompt and
  next-prompt files, recorded validation commands, allowlisted AHL checks,
  completion-audit artifact presence, handoff state, and commit-plan policy.
  It records prompt validation commands in record-only mode rather than
  executing arbitrary shell.
- `commit plan` creates a plan-only artifact with prompt-prefixed subjects,
  explicit file lists, validation evidence when available, and unrelated
  working-tree changes separated.
- `commit check` inspects recent commits in a target project for prompt
  prefixes, Tim Pope-style subject/body shape, line wrapping, literal `\n`
  sequences, co-author trailers, generated boilerplate, and grouping evidence.
  It reports amend or interactive rebase guidance only when it finds a clear
  issue.
- `commit execute` stages only files listed in a commit plan and commits only
  when `--operator-approved` is supplied. It refuses unrelated staged files,
  missing listed files, and failed or blocked validation status unless
  `--allow-failed` is explicit.
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

Future portable commands should continue the documented namespace in
`../docs/portable-operator/extension-plan.md`. `lifecycle snippets` is
implemented as read-only copy/paste output, `lifecycle context-check` is
implemented as read-only advisory output, `lifecycle run-range` is implemented
as dry-run prompt-range planning, and `commit check` is implemented as
read-only post-commit inspection.

## What It Does Not Do

- It does not run prompts or call model providers unless `outer run --execute`
  is explicitly selected for a supported local driver.
- It does not commit by default; commit execution requires a reviewed plan and
  explicit `--operator-approved`.
- It does not inspect, ingest, or store raw assistant transcripts.
- It does not scan file contents for secrets or replace human review before
  committing.
- It does not approve memory promotions or make `memory/` a replacement for
  docs, findings, runbooks, templates, scripts, or tests.
- It does not maintain a daemon or hidden runtime state.
- It does not replace human closeout, readiness, or promotion judgment.
- It does not provide graph, vector, provider, plugin, or server
  infrastructure.
- `project locate` does not make older AHL-root commands operate on arbitrary
  target project repos.
- `project status` does not run prompts, execute validation commands, treat
  `human-notes.md` as machine authority, or make completion decisions.
- `lifecycle snippets` does not run or repair prompts, execute validation
  commands, edit `human-notes.md`, modify target-project context files, stage,
  commit, amend, rebase, or call providers.
- `lifecycle context-check` does not edit `AGENT.md`, `CLAUDE.md`,
  `.context/`, `context/`, `human-notes.md`, or any target-project file. It
  does not decide that context must be updated; it only suggests review
  questions from changed paths.
- `lifecycle run-range` does not run prompts, invoke assistant CLIs, execute
  validation commands, edit target-project files, edit `human-notes.md`,
  stage, commit, amend, rebase, push, tag, or continue automatically. It
  writes JSON only when `--artifact` is explicit.
- `portable rehearsal` does not run prompts, call assistant CLIs, edit
  `human-notes.md`, edit target-project fixtures, stage or commit in the AHL
  repository, fetch network resources, or require credentials. Its only
  commits are isolated temporary git fixture data for `commit check`.
- `commit check` does not stage, commit, amend, rebase, reset, push, tag, or
  edit target-project files. It reads git history and changed-file lists only.
- Driver probes do not authenticate, send prompts, create sessions, or prove
  quota. They inspect the registry, `PATH`, and optional help output only.
- AHL does not automate Claude subscription usage through external APIs,
  browser sessions, cookies, or hidden provider integrations; Claude Code and
  generic chat remain manual or terminal assistant surfaces.

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
python3 scripts/ahl.py driver probe pi --help-only --json
python3 scripts/ahl.py project locate --json
python3 /path/to/agent-harness-lab/scripts/ahl.py project locate --project /path/to/project --json
python3 scripts/ahl.py project status --json
python3 /path/to/agent-harness-lab/scripts/ahl.py project status --project /path/to/project --json
python3 scripts/ahl.py lifecycle snippets 45
python3 /path/to/agent-harness-lab/scripts/ahl.py lifecycle snippets PROMPT_84 --project /path/to/project --json
python3 scripts/ahl.py lifecycle snippets PROMPT_84.txt --bootstrap CLAUDE.md --context
python3 scripts/ahl.py lifecycle context-check PROMPT_84 --project /path/to/project --json
python3 /path/to/agent-harness-lab/scripts/ahl.py lifecycle run-range 18 27 --project /path/to/project --dry-run --json
python3 scripts/ahl.py lifecycle run-range 18 27 --project /path/to/project --artifact runs/portable-operator/run-range.json --json
python3 scripts/ahl.py project status --project fixtures/portable-operator/projects/basic --json
python3 scripts/ahl.py lifecycle snippets PROMPT_01 --project fixtures/portable-operator/projects/basic --json
python3 scripts/ahl.py lifecycle context-check PROMPT_01 --project fixtures/portable-operator/projects/basic --json
python3 scripts/ahl.py lifecycle run-range 1 2 --project fixtures/portable-operator/projects/basic --dry-run --json
python3 scripts/ahl.py lifecycle snippets PROMPT_01 --project fixtures/portable-operator/projects/claude-bootstrap --bootstrap CLAUDE.md --json
python3 scripts/ahl.py portable rehearsal --json
python3 scripts/ahl.py outer plan --from PROMPT_33 --count 3 --driver codex --model gpt-5.5 --reasoning medium --json
python3 scripts/ahl.py outer plan --from PROMPT_40 --count 1 --driver pi --json
python3 scripts/ahl.py outer plan --next 10 --driver codex --json
python3 scripts/ahl.py outer dry-run --plan runs/outer-loop/<plan-id>/plan.json --json
python3 scripts/ahl.py outer run --plan runs/outer-loop/<plan-id>/plan.json --dry-run --json
python3 scripts/ahl.py outer run --plan runs/outer-loop/<plan-id>/plan.json --execute --max-prompts 1 --json
python3 scripts/ahl.py outer gate PROMPT_36 --json
python3 scripts/ahl.py outer gate PROMPT_36 --plan runs/outer-loop/<plan-id>/plan.json --json
python3 scripts/ahl.py outer status --run <run-id> --json
python3 scripts/ahl.py outer resume --run <run-id> --dry-run --json
python3 scripts/ahl.py outer recovery-handoff --run <run-id>
python3 scripts/ahl.py outer plan --from PROMPT_41 --count 1 --driver manual --json
python3 scripts/ahl.py outer dry-run --plan runs/outer-loop/<plan-id>/plan.json --json
python3 scripts/ahl.py outer run --plan runs/outer-loop/<plan-id>/plan.json --execute --max-prompts 1 --json
python3 scripts/ahl.py commit plan PROMPT_38 --json
python3 scripts/ahl.py commit plan --run runs/outer-loop/<run-id>/run-ledger.json --json
python3 scripts/ahl.py commit check --project /path/to/project --prompt PROMPT_84 --json
python3 scripts/ahl.py commit check --project /path/to/project --prompt PROMPT_84 --range HEAD~10..HEAD --json
python3 scripts/ahl.py commit check --project /path/to/project --last 7 --json
python3 scripts/ahl.py commit execute --plan runs/outer-loop/<run-id>/commit-plan.json --operator-approved
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
- `portable-rehearsal`
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
- `project locate`: `ok`, `ahl_home`, `project`, `warnings`, `problems`;
  `ahl_home` includes `path`, `source`, `valid`, and `problems`; `project`
  includes `requested`, `requested_exists`, `requested_is_dir`, `root`,
  `source`, `git`, `prompt_dir`, `prompt_dir_exists`, `prompt_count`, and
  `prompt_files`
- `project status`: `ok`, `ahl_home`, `project`, `warnings`, `problems`;
  `ahl_home` has the same stable fields as `project locate`; `project`
  includes `requested`, `requested_exists`, `requested_is_dir`, `root`,
  `source`, `git`, `promptset`, `next_prompt`, and `files`; `git` includes
  `available`, `inside_work_tree`, `found`, `dot_git_exists`, `root`,
  `branch`, `dirty_count`, `untracked_count`, `status_lines`, and `problems`;
  `promptset` includes
  `prompt_dir`, `prompt_dir_exists`, `prompt_count`, `state`,
  `lowest_prompt_number`, `highest_prompt_number`, `gaps`, `duplicates`,
  `malformed`, `strict_two_digit`, `filenames`, and `numbers`; `next_prompt`
  includes `next_after_highest_prompt_file`,
  `prompt_prefixed_commit_summary`, `likely_next_prompt`, `confidence`, and
  `reason`; `files` includes `AGENT.md`, `CLAUDE.md`, `.context`, and
  `human-notes.md`
- `lifecycle snippets`: `ok`, `ahl_home`, `project`, `prompt`,
  `configuration`, `snippets`, `warnings`, and `problems`; `project` includes
  `requested`, `root`, `source`, `prompt_dir`, and `prompt_dir_exists`;
  `prompt` includes `input`, `id`, `number`, `path`, and `exists`;
  `configuration` includes `bootstrap`, `bootstrap_doc`, `context`,
  `context_detected`, `context_mentioned`, and `repair_included`; `snippets`
  includes `run`, `audit_next_readiness_context_update`, `commit_plan`,
  `make_commits`, and `commit_check`, plus `repair` only when
  `--include-repair` is used
- `lifecycle context-check`: `ok`, `ahl_home`, `project`, `prompt`, `git`,
  `changed_paths`, `candidates`, `ignored_changes`, `questions`,
  `conclusion`, `read_only`, `warnings`, and `problems`; `project` includes
  `requested`, `root`, `source`, `prompt_dir`, and `prompt_dir_exists`;
  `prompt` includes `input`, `id`, `number`, `path`, and `exists`; `git` has
  the same stable fields as `project status`; each candidate includes `path`,
  `kind`, `confidence`, `reason`, and `questions`
- `lifecycle run-range`: `ok`, `schema`, `plan_id`, `created_at`, `mode`,
  `dry_run`, `read_only`, `project`, `configuration`, `requested_range`,
  `prompt_ids`, `missing_prompt_ids`, `malformed_prompt_filenames`, `steps`,
  `planned_artifact`, `next_prompt`, `stop_reason`, `restart_state`,
  `safety_notes`, `warnings`, and `problems`; each step includes `prompt_id`,
  `number`, `path`, `exists`, `sequence_index`, `phase_order`, `phases`,
  `validation_commands`, `fresh_session_boundary`, and `next_prompt`;
  `artifact` is present only when an explicit artifact write succeeds
- `portable rehearsal`: `ok`, `schema`, `generated_at`, `mode`, `read_only`,
  `assistant_invocation`, `ahl_home`, `fixture_projects`, `commands`,
  `summary`, `known_limitations`, `residual_manual_steps`, `capstone_ready`,
  and `problems`; each command record includes `label`, `command`, `status`,
  `ok`, and `details`
- `outer plan`: `ok`, `plan_id`, `created_at`, `requested_range`, `prompts`,
  `driver`, `model`, `reasoning`, `permission_posture`,
  `required_ahl_checks`, `stop_conditions`, `commit_policy`,
  `transcript_capture_policy`, `run_artifact_dir`, `problems`, and `artifact`
  when creation succeeds
- `outer dry-run`: `ok`, `plan_id`, `steps`, `problems`; each step includes
  stable `prompt_id`, `path`, `status`, `validation_commands`, and `problems`
- `outer gate`: `ok`, `status`, `prompt_id`, `changed_files`,
  `validation_commands`, `validation_outcomes`, `ahl_checks`,
  `completion_audit`, `next_prompt_readiness`, `handoff`, `commit_plan`,
  `decision`, `warnings`, and `problems`
- `outer run`: `ok`, `status`, `run_id`, `plan_id`, `mode`, `execute`,
  `dry_run`, `driver`, `steps`, `problems`, and `artifact` when a ledger is
  written; each step includes stable `prompt_id`, `status`,
  `payload_artifact`, `driver`, and `gate`
- `outer status`: `ok`, `status`, `run_id`, `plan_id`, `artifact`, `steps`,
  `next_prompt`, `resume_safe`, `stop_reason`, `recovery_recommendation`, and
  `problems`
- `outer resume`: `ok`, `status`, `run_id`, `plan_id`, `dry_run`, `execute`,
  `rerun`, `next_prompt`, `completed_prompts`, `skipped_prompts`,
  `failed_prompts`, `pending_prompts`, `git`, `problems`, and `notes`
- `outer recovery-handoff`: `ok`, `created`, `artifact`, `run_id`, and
  `problems`
- `commit plan`: `ok`, `schema`, `plan_id`, `created_at`, `mode`, `source`,
  `prompt_ids`, `prompt_context`, `grouping_policy`, `git`, `groups`,
  `unrelated_changes`, `warnings`, `problems`, and `artifact`
- `commit check`: `ok`, `read_only`, `project`, `selector`, `summary`,
  `commits`, `guidance`, `warnings`, and `problems`; `selector` includes
  `mode`, `description`, `prompt`, `searched_commit_count`,
  `matched_commit_count`, and `truncated`; each commit includes `hash`,
  `short_hash`, `subject`, `parents`, `changed_files`, and `issues`
- `commit execute`: `ok`, `status`, `plan`, `dry_run`, `commits`, and
  `problems`
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
