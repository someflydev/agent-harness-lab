# Safety

Safety guidance in this repo keeps powerful assistant sessions bounded,
inspectable, and operator-controlled. It is practical operating guidance, not a
security product or automated policy runtime.

## Start Here

- `permission-postures.md` - read-only, workspace-write, and manual-required
  session labels.
- `destructive-actions.md` - what to check before deletion, cleanup, history
  rewrite, or external state changes.
- `data-hygiene.md` - treatment for `tmp/`, handoffs, reports, memory
  candidates, and transient runtime files.
- `secrets-and-transcripts.md` - why secrets and raw transcripts do not belong
  in repo memory.
- `reference-repo-boundaries.md` - why local reference repos are not
  implementation targets.
- `operator-approval.md` - when the assistant must stop for human approval.

## Local Checks

Run the conservative safety checks through the existing doctor command:

```sh
python3 scripts/ahl.py doctor
python3 scripts/ahl.py doctor --json
```

The check looks for obvious hygiene problems by path name and git status. It
does not inspect private file contents and is not a secret scanner.
