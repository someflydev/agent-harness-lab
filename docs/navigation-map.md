# Navigation Map

This map explains where humans and fresh assistant sessions should start, what
durable areas exist, and how the registry files relate to the source files.

## Starting Points

An operator starts with `README.md`, then uses `AGENT.md` and
`docs/operator-start.md` to decide which prompt or runbook to invoke. The
operator controls prompt selection, permissions, commits, and whether any
temporary handoff is justified.

A fresh assistant starts with `AGENT.md`, then `README.md`,
`docs/guardrails.md`, the active `.prompts/PROMPT_XX.txt`, and any docs the
prompt explicitly references. During prompt execution, the assistant should run
`git status --short` before editing and preserve unrelated work.

## Durable Areas

Routines live in `docs/routines/`, with operator-facing procedures in
`runbooks/`. The command-backed routine registry is summarized in
`docs/commands-and-routines.md`.

Templates live in `templates/`. Contract templates are under
`templates/contracts/`, handoff templates under `templates/handoffs/`, memory
templates under `templates/memory/`, report templates under
`templates/reports/`, and run manifests under `templates/runs/`.

Examples live in `examples/`. They show illustrative prompt runs, lane
delegation, memory promotion, and repair bridges. They are examples of shape,
not live operational state.

Reports and findings live in `reports/` and `findings/`. Bounded trial
material lives in `experiments/`. The lab method tying those areas together is
`docs/lab-method.md`.

Metadata guidance lives in `docs/metadata/`. Machine-checkable schemas live in
`schemas/`, including run record, readiness report, and promptset index
schemas.

Helper scripts live in `scripts/`, primarily `scripts/ahl.py`. Script usage is
documented in `scripts/README.md` and `docs/scripts.md`. Documentation link
checking is described in [navigation validation](navigation-validation.md).

## Registries

The `registry/` directory contains curated JSON navigation indexes:

- `registry/artifacts.json` maps top-level artifact families.
- `registry/prompts.json` lists every prompt file in prompt order.
- `registry/roles.json` maps durable role documents.
- `registry/routines.json` maps key routines and command-backed checks.
- `registry/templates.json` maps reusable template groups.
- `registry/examples.json` maps examples and evidence-oriented areas.
- `registry/scripts.json` maps helper scripts and commands.

Use `python3 scripts/ahl.py registry check` to validate JSON parsing, required
fields, referenced paths, and prompt registry ordering. Use
`python3 scripts/ahl.py registry list --json` when another local tool needs a
compact list of registry files.

Use `python3 scripts/ahl.py docs check` to catch missing local markdown link
targets, missing docs indexes, stale top-level navigation, and registry path
drift before closing a prompt that touches navigation surfaces.

## Source Of Truth

Checked-in repo files and git history are the source of truth. Registries are
derived navigation aids that point at those files. If a registry entry and a
source document disagree, inspect and update the source document first, then
refresh the registry entry only when it remains a useful curated index.

Do not treat `registry/` as an exhaustive mirror of the repo. Later prompts
should update registry files when explicitly required or when a new durable
artifact clearly belongs in an existing curated index.
