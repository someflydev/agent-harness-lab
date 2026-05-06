# Maintenance

This page describes routine maintenance for the lab's promptset, registries,
templates, skills, helper scripts, domain packs, and release-readiness checks.
Keep changes small, reviewable, and aligned with the human-assisted workflow.

## Update Prompt Files

Edit prompt files under `.prompts/` only when doing prompt-authoring or a
prompt explicitly requires it. Keep each prompt bounded for one fresh session,
name required deliverables, state validation, and identify the immediate next
prompt when relevant.

After changing prompts, run:

```sh
python3 scripts/ahl.py promptset
python3 scripts/ahl.py promptset lint
```

Update `registry/prompts.json` when prompt files are added, removed, renamed,
or materially reordered.

## Update Registries

Registries live under `registry/` and are curated navigation indexes. Update a
registry when a prompt explicitly names it or when a new durable artifact
clearly belongs in an existing index.

After changing registries, run:

```sh
python3 scripts/ahl.py registry check
python3 scripts/ahl.py docs check
```

## Add Templates And Skills

Add reusable markdown templates under `templates/` when a repeated artifact
shape has stabilized. Document the template in the nearest README and update
`registry/templates.json` when it becomes a curated template group.

Add project-level skills under `.agents/skills/<skill-name>/SKILL.md` when a
recurring routine needs loadable assistant instructions. Document the skill in
`.agents/skills/README.md` or `docs/project-skills.md` when it becomes part of
the expected operator surface.

## Add A Script Command And Test

Keep `scripts/ahl.py` dependency-free unless a later prompt explicitly changes
that boundary. For a new command:

- Add the CLI behavior in `scripts/ahl.py`.
- Add or update tests in `tests/test_ahl.py`.
- Document the command in `scripts/README.md` and `docs/scripts.md`.
- Add a Makefile target only if the command is a stable routine action.
- Update `registry/scripts.json` when the command belongs in the curated
  command index.

Run:

```sh
python3 -m unittest tests/test_ahl.py
python3 scripts/ahl.py validate
```

## Add A Domain Pack

Create a new directory under `domain-packs/` using
`domain-packs/_template/README.md` and `domain-packs/_template/pack.json` as
the local shape reference. Keep the pack modest and optional.

After adding or changing a pack, run:

```sh
python3 scripts/ahl.py domain-pack check
python3 scripts/ahl.py docs check
```

## Run Release-Readiness Checks

Use `docs/release-readiness.md` as the checklist. The core command set is:

```sh
python3 scripts/ahl.py promptset lint
python3 scripts/ahl.py docs check
python3 scripts/ahl.py registry check
python3 -m unittest tests/test_ahl.py
python3 scripts/ahl.py dry-run check --all
python3 scripts/ahl.py doctor
python3 scripts/ahl.py domain-pack check
```

Record failures as blockers or known limitations instead of implying support
for behavior that is not implemented.
