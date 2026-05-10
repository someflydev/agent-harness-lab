# Helper Scripts

`scripts/ahl.py` provides the first lightweight helper layer for
`agent-harness-lab`. It is a local Python 3 CLI built on the standard library.
Its job is to make manual prompt execution easier to inspect. It defaults to
read-only checks, scaffolds, dry-runs, and review artifacts; the only live
assistant invocation path is explicit `outer run --execute` for supported local
driver contracts.

## Commands

```sh
python3 scripts/ahl.py doctor
python3 scripts/ahl.py promptset
python3 scripts/ahl.py validate
python3 scripts/ahl.py registry check
python3 scripts/ahl.py registry list --json
python3 scripts/ahl.py driver check
python3 scripts/ahl.py project status --project /path/to/project --json
python3 scripts/ahl.py lifecycle snippets PROMPT_84 --project /path/to/project --json
python3 scripts/ahl.py lifecycle context-check PROMPT_84 --project /path/to/project --json
python3 scripts/ahl.py lifecycle run-range 18 27 --project /path/to/project --dry-run --json
python3 scripts/ahl.py portable rehearsal --json
python3 scripts/ahl.py outer plan --from PROMPT_33 --count 3 --driver manual --json
python3 scripts/ahl.py outer dry-run --plan runs/outer-loop/<plan-id>/plan.json --json
python3 scripts/ahl.py outer run --plan runs/outer-loop/<plan-id>/plan.json --dry-run --json
python3 scripts/ahl.py outer gate PROMPT_36 --json
python3 scripts/ahl.py outer resume --run runs/outer-loop/<run-id>/run-ledger.json --dry-run --json
python3 scripts/ahl.py commit plan PROMPT_38 --json
python3 scripts/ahl.py commit check --project /path/to/project --last 10 --json
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
- `driver check` validates conservative assistant driver records. `driver
  probe --help-only` can inspect local executable availability without sending
  prompts.
- `project status` reports target-project git, promptset, bootstrap/context,
  recent prompt-prefixed commit, and likely-next-prompt state without editing
  files or invoking assistants.
- `lifecycle snippets` prints reusable one-prompt snippets for a target
  project without executing them.
- `lifecycle run-range` dry-runs a one-prompt-at-a-time range plan for a
  target project. It writes JSON only with explicit `--artifact`.
- `portable rehearsal` composes portable helpers against artificial fixtures
  and isolated temporary git data.
- `outer plan`, `outer dry-run`, `outer run`, `outer status`, `outer resume`,
  and `outer recovery-handoff` support bounded outer-loop planning, payloads,
  ledgers, dry-run execution, status, and recovery artifacts. `outer run`
  defaults to dry-run and needs `--execute` for live local assistant CLI use.
- `outer gate` collects post-prompt validation, audit, readiness, handoff, git,
  and commit-plan evidence without invoking assistants or executing arbitrary
  prompt validation commands.
- `lifecycle context-check` reads target-project git status and suggests
  conservative context-update review questions without editing bootstrap,
  `.context/`, `context/`, or target-project files.
- `commit plan` creates a plan-only artifact for prompt-scoped commit grouping.
- `commit check` inspects recent commits and reports prompt-prefix or message
  hygiene issues without rewriting history.
- `commit execute` commits only from a reviewed plan and only with explicit
  `--operator-approved`.
- `dry-run`, `lane`, `domain-pack`, `memory`, `experiment`, and `finding`
  subcommands validate or scaffold their named local artifact families.
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
- `driver check`: `ok`, `drivers`, `checks`, `problems`
- `project status`: `ok`, `ahl_home`, `project`, `warnings`, `problems`
- `lifecycle snippets`: `ok`, `ahl_home`, `project`, `prompt`,
  `configuration`, `snippets`, `warnings`, `problems`
- `outer gate`: `ok`, `status`, `prompt_id`, `changed_files`,
  `validation_commands`, `validation_outcomes`, `ahl_checks`,
  `completion_audit`, `next_prompt_readiness`, `handoff`, `commit_plan`,
  `decision`, `warnings`, `problems`
- `lifecycle context-check`: `ok`, `ahl_home`, `project`, `prompt`, `git`,
  `changed_paths`, `candidates`, `ignored_changes`, `questions`,
  `conclusion`, `read_only`, `warnings`, and `problems`
- `lifecycle run-range`: `ok`, `schema`, `plan_id`, `mode`, `dry_run`,
  `read_only`, `project`, `requested_range`, `steps`, `warnings`, `problems`
- `portable rehearsal`: `ok`, `schema`, `commands`, `summary`, `problems`
- `outer plan`: `ok`, `plan_id`, `requested_range`, `prompts`, `driver`,
  `required_ahl_checks`, `stop_conditions`, `commit_policy`, `artifact`,
  `problems`
- `outer run`: `ok`, `status`, `run_id`, `plan_id`, `mode`, `execute`,
  `dry_run`, `driver`, `steps`, `artifact`, `problems`
- `outer resume`: `ok`, `status`, `run_id`, `plan_id`, `dry_run`,
  `next_prompt`, `completed_prompts`, `pending_prompts`, `git`, `problems`
- `commit plan`: `ok`, `schema`, `plan_id`, `prompt_ids`, `git`, `groups`,
  `unrelated_changes`, `warnings`, `problems`
- `commit check`: `ok`, `read_only`, `project`, `selector`, `summary`,
  `commits`, `guidance`, `warnings`, `problems`
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

These fields are suitable for small local checks and smoke tests. See
`scripts/README.md` for the fuller JSON field inventory.

## Boundary

The helper CLI supports the human-assisted workflow described in the runbooks.
It does not choose prompts, call paid model APIs, store raw assistant
transcripts, create long-running processes, or decide when work is complete.
Live local assistant CLI invocation is opt-in through `outer run --execute` and
depends on local authentication outside AHL. The operator and active prompt
remain the source of scope and authority.
