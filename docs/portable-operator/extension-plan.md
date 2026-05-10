# Portable Operator Extension Plan

This plan inventories the existing AHL helper surface and defines the prompt
arc for making the one-prompt-at-a-time workflow usable from arbitrary project
repositories. It is a design map for later prompts, not an implementation of
portable CLI behavior.

## Current Inventory

### Existing CLI Commands

`scripts/ahl.py` currently treats `Path.cwd()` as `repo_root()`. That means
commands assume the current working directory is the AHL checkout unless a
later prompt changes the root model.

| Command | Current purpose | AHL-repo-specific today |
| --- | --- | --- |
| `help` | List common helper commands and Makefile targets. | Reads built-in command registry only. |
| `doctor` | Check AHL foundations, ignore rules, stale handoffs, transcript paths, and secret-looking names. | Requires AHL top-level dirs, docs dirs, `.prompts/`, and AHL ignore policy. |
| `promptset` / `promptset lint` | Inspect AHL `.prompts/` numbering and shallow prompt readiness. | Reads `.prompts/` under `repo_root()`, and lint checks AHL prompt registry alignment. |
| `validate` | Check AHL quality foundations and promptset numbering. | Requires AHL quality docs and repo layout. |
| `docs check` | Check local markdown links, docs index coverage, and registry paths. | Scans AHL doc roots and expects `docs/README.md` navigation rules. |
| `registry list` / `registry check` | Validate curated AHL registry JSON indexes. | Reads `registry/` and AHL schema/path expectations. |
| `driver list` / `driver check` / `driver probe` | Validate assistant driver records and help-only probes. | Driver registry and fixtures live in AHL home; probes may inspect local `PATH`. |
| `outer plan` | Create an inspectable prompt batch plan under `runs/outer-loop/`. | Resolves prompt range, driver registry, templates, and output paths under AHL root. |
| `outer dry-run` | Validate plan structure, prompts, driver records, checks, and stop conditions. | Expects AHL prompt paths and AHL checks. |
| `outer run` | Build prompt payloads and run ledgers; dry-run by default, `--execute` for supported local drivers. | Reads AHL prompts, startup docs, templates, and writes AHL run artifacts. |
| `outer gate` | Collect post-prompt status, validation command records, allowlisted AHL checks, audit artifact state, handoff state, and next-prompt readiness. | Checks AHL prompt files and AHL validation commands. |
| `outer status` / `outer resume` / `outer recovery-handoff` | Summarize ledgers, plan safe resumes, and create recovery handoffs. | Reads/writes AHL `runs/outer-loop/` artifacts and uses AHL git state. |
| `commit plan` / `commit execute` | Create prompt-scoped commit plans and execute reviewed commits with explicit approval. | Extracts expected files from AHL prompts and uses AHL working tree paths. |
| `fixtures check` | Validate expected fixture JSON structures. | AHL fixtures and schemas only. |
| `dry-run list` / `dry-run check` | Validate deterministic AHL dry-run scenarios and parity records. | AHL scenario manifests and backing files only. |
| `lane check` / `lane status` | Inspect manual lane simulation artifacts. | AHL simulation directories and templates. |
| `domain-pack check` | Validate optional AHL domain pack manifests. | AHL domain-pack layout. |
| `experiment new` / `experiment check` / `finding new` | Scaffold and check AHL lab evidence. | Writes and checks AHL experiment/finding directories. |
| `memory propose` / `memory check` / `memory decision` | Scaffold reviewed memory promotion artifacts. | AHL memory workspace and templates. |
| `resume` | Print a read-only Session Context Briefing. | Summarizes AHL git state and runtime files. |
| `trace` | Summarize prompt-related working tree changes. | Reads AHL prompt files and AHL git state. |
| `checkpoint`, `scaffold-run`, `new-handoff`, `metadata-example` | Scaffold local context, run manifests, handoffs, and metadata examples. | Uses AHL templates and output locations. |

### Existing Outer-Loop Helpers

The phase-two outer loop already supports local batch planning, plan dry-runs,
prompt payload generation, dry-run-default run ledgers, explicit one-step live
invocation for supported local driver contracts, post-prompt gates, status and
resume reports, recovery handoffs, commit plans, and approval-gated commit
execution. Portable work should extend those capabilities by adding a target
project root, not by renaming them under unrelated commands.

The current plan, dry-run, run, gate, resume, and commit helpers assume AHL
prompt files and AHL run artifacts. They also treat AHL validation checks as
the allowlisted checks in gate reports.

### Promptset And Registry Behavior

Promptset numbering is dependency-free and can already inspect any supplied
prompt directory internally, but the public command uses
`repo_root() / ".prompts"`. Promptset lint also checks prompt registry alignment in
`registry/prompts.json`, which is an AHL-home concern. Later portable commands
need to distinguish target project prompt parsing from AHL prompt registry
validation.

Registry checks are AHL-home checks. They should remain tied to AHL templates,
schemas, fixtures, docs, scripts, and driver records.

### Assistant Usage Surfaces

Documented assistant surfaces are Codex, Claude Code, Gemini, Pi, generic
chat, subscription-friendly workflows, and context-loading guidance. The common
model is fresh-session execution with `AGENT.md`, `README.md`,
`docs/guardrails.md`, the active prompt, prompt-named docs, local validation,
completion audit, next-prompt preflight, bridge only when useful, and reset.

These docs intentionally avoid provider lock-in. They allow local CLIs,
manual copy/paste, and project-context tools, but they do not claim API-backed
automation or universal assistant skill discovery.

### AHL Home Versus Target Project

Current `repo_root()` equals `Path.cwd()`. Portable behavior needs two roots:

- AHL home: the checkout containing `scripts/ahl.py`, AHL templates,
  registries, schemas, fixtures, docs, and tests.
- Target project root: the operator's current repo or explicitly selected
  project. It may contain `.prompts/`, `AGENT.md`, `CLAUDE.md`, `.context/`,
  `human-notes.md`, local validation commands, and project git history.

Commands that read AHL assets should resolve them from AHL home. Commands that
inspect, report on, or write run artifacts for the operator's project should
name the target project root explicitly in structured output and avoid writing
into AHL unless the artifact is AHL-owned.

### Safety Boundaries

The portable extension inherits the outer-loop safety boundary:

- Dry-run first for discovery, plans, payload previews, and validation gates.
- Live assistant invocation requires explicit execution consent.
- Commit execution requires a separate explicit operator approval.
- No provider credentials, API keys, cookies, or account secrets in AHL.
- Raw transcripts are off by default.
- Dirty worktrees and unexpected git state are reported instead of normalized.
- No destructive git operations, staging, commits, pushes, tags, releases, or
  publishes unless the operator explicitly authorizes them.
- Failures should stop with an inspectable record rather than retrying,
  switching providers, skipping validation, or continuing to later prompts.

## Prompt Arc

### Portable Invocation And Workspace Discovery

- Likely command shape: `project locate --json` and `project locate --project
  <path> --json`.
- Likely files to modify later: `scripts/ahl.py`, `tests/test_ahl.py`,
  `scripts/README.md`, `docs/portable-operator/invocation.md`,
  `docs/portable-operator/README.md`, `docs/README.md`.
- Safety boundary: read-only discovery; reject invalid `AHL_HOME`; do not
  create wrappers or mutate target projects.
- Validation approach: unit tests for AHL-home detection, invalid overrides,
  git-root discovery, non-git fallback, missing `.prompts/`, and JSON fields.
- Dependency posture: standard library only; optional `git` use must degrade
  cleanly when unavailable.

### Target Project Detection And Status Reporting

- Likely command shape: `project status --project <path> --json`.
- Likely files to modify later: `scripts/ahl.py`, `tests/test_ahl.py`,
  `scripts/README.md`, `docs/portable-operator/status.md`.
- Safety boundary: report target files and git state without editing them;
  treat missing `.prompts/` as status, not a crash.
- Validation approach: temporary project fixtures covering clean, dirty,
  missing promptset, and non-git cases.
- Dependency posture: no project dependency install or network call.

### Lifecycle Snippet Generation

- Likely command shape: `lifecycle snippets --project <path> --prompt
  PROMPT_XX --assistant codex|claude-code|gemini|generic --json`.
- Likely files to modify later: `scripts/ahl.py`, `tests/test_ahl.py`,
  `templates/portable-operator/`, `docs/portable-operator/lifecycle.md`.
- Safety boundary: generate copyable instructions only; do not invoke
  assistants or rewrite project prompts.
- Validation approach: golden-output style tests for snippet fields and
  assistant-neutral defaults.
- Dependency posture: template rendering with standard-library string handling.

### Context-Update Doctrine And Report Support

- Likely command shape: `lifecycle context-check --project <path> --json` and
  a report artifact under a project-local run directory.
- Likely files to modify later: `docs/portable-operator/context-updates.md`,
  `templates/portable-operator/context-report.md`, `scripts/ahl.py`,
  `tests/test_ahl.py`.
- Safety boundary: never auto-edit `human-notes.md`; report stale or missing
  context candidates for operator review.
- Validation approach: fixtures for `AGENT.md`, `CLAUDE.md`, `.context/`, and
  operator-owned notes.
- Dependency posture: file inspection only, no semantic index.

### Commit-Message Inspection After Commits

- Likely command shape: `commit check --project <path> --since <ref> --json`.
- Likely files to modify later: `scripts/ahl.py`, `tests/test_ahl.py`,
  `docs/portable-operator/commit-checks.md`, `scripts/README.md`.
- Safety boundary: inspect commit messages and prompt-id conventions only; no
  staging, committing, rebasing, amending, pushing, or history rewrite.
- Validation approach: temporary git repo tests with prompt-prefixed and
  missing-prefix commits.
- Dependency posture: local `git` when available; skip or degrade clearly
  when unavailable.

### One-Prompt Autopilot Runbooks

- Likely command shape: docs-first runbook plus optional
  `lifecycle snippets` support, not an autonomous daemon.
- Likely files to modify later: `runbooks/portable-one-prompt.md`,
  `docs/portable-operator/autopilot.md`, `docs/README.md`,
  `runbooks/README.md`.
- Safety boundary: "autopilot" means operator-guided one-prompt routine with
  explicit approval points, not unattended multi-prompt execution.
- Validation approach: docs check and promptset lint; no provider calls.
- Dependency posture: markdown and local helper commands only.

### Run-Range Dry-Run Orchestration

- Likely command shape: `lifecycle run-range --project <path> --from
  PROMPT_XX --count N --dry-run --json`.
- Likely files to modify later: `scripts/ahl.py`, `tests/test_ahl.py`,
  `schemas/portable-run-range.schema.json`, `templates/portable-operator/`,
  `docs/portable-operator/run-range.md`.
- Safety boundary: dry-run range planning only at first; no live assistant
  invocation, no parallelism, and no commits.
- Validation approach: external-project fixtures for prompt range selection,
  missing prompts, and output artifact paths.
- Dependency posture: reuse existing prompt range parsing where possible;
  standard library only.

### Assistant-Surface Boundaries

- Likely command shape: no provider-specific command family; assistant names
  may be options for snippet wording and driver records only.
- Likely files to modify later: `docs/assistants/README.md`,
  `docs/portable-operator/assistant-surfaces.md`,
  `docs/outer-loop/assistant-driver-boundary.md`.
- Safety boundary: no provider lock-in, no hidden APIs, no Claude subscription
  API automation assumptions, and no Pi-specific extension material.
- Validation approach: docs check plus review for overclaims.
- Dependency posture: documentation-only unless existing driver records are
  reused for local CLI probes.

### External-Project Fixtures And Smoke Rehearsal

- Likely command shape: `fixtures check` may gain portable fixture coverage,
  and smoke docs may describe manual rehearsal commands.
- Likely files to modify later: `fixtures/portable-projects/`,
  `tests/test_ahl.py`, `docs/portable-operator/smoke-rehearsal.md`.
- Safety boundary: fixtures must be artificial and local; smoke rehearsals
  should avoid network, credentials, and provider calls by default.
- Validation approach: unit tests and dry-run smoke commands against temporary
  projects.
- Dependency posture: standard library and local git only.

### Final Capstone And Docs Navigation

- Likely command shape: no new command required; capstone is an audit report.
- Likely files to modify later: `docs/portable-operator/capstone-audit.md`,
  `docs/portable-operator/operating-baseline.md`, `README.md`,
  `docs/README.md`, `scripts/README.md`.
- Safety boundary: state implemented capability honestly and separate future
  backlog from baseline behavior.
- Validation approach: `docs check`, `promptset lint`, `doctor`, unit tests,
  and review against portable non-goals.
- Dependency posture: no new runtime dependencies.
