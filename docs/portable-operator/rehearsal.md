# Portable Workflow Rehearsal

`portable rehearsal` is the deterministic end-to-end rehearsal for the
portable operator workflow. It composes the existing read-only portable helpers
against artificial fixture projects and an isolated temporary git repository.
It does not call assistant CLIs, require network access, use provider
credentials, edit `human-notes.md`, or commit to the AHL repository.

## Invocation

```sh
python3 scripts/ahl.py portable rehearsal
python3 scripts/ahl.py portable rehearsal --json
make portable-rehearsal
```

The JSON form is the machine-checkable surface. The Makefile target is a stable
human-readable wrapper.

## Coverage

The rehearsal exercises:

- AHL home and target project root discovery using the basic fixture;
- `project status` for the valid-sequential basic fixture;
- `project status` for the gapped fixture;
- `lifecycle snippets` for `PROMPT_01`;
- `lifecycle context-check` for `PROMPT_01`;
- `lifecycle run-range 1 2` against the basic fixture;
- `lifecycle run-range 1 3` against the gapped fixture, expecting a clear
  missing `PROMPT_02` stop;
- `commit check --last 2` against a temporary git repository with one
  prompt-prefixed commit and one deliberately unprefixed commit.

The temporary git repository is created under the system temporary directory
and cleaned up before the command returns. If git is unavailable, the
commit-check portion is skipped cleanly while the fixture rehearsal still runs.

## Report

The current static report is
`../../reports/portable-operator/rehearsal.md`. Regenerate live evidence with:

```sh
python3 scripts/ahl.py portable rehearsal --json
```

The report distinguishes implemented helper behavior from manual assistant
work. A passing rehearsal means the helper path is ready for capstone review,
not that any real target project prompt was implemented.
