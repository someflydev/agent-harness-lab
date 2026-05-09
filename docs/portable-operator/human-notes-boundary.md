# Human Notes Boundary

`human-notes.md` is operator-owned scratch and control-zone content in a target
project repo. It can help the operator remember intent, sequencing, or local
decisions, but it is not AHL machine state.

## Rules

- AHL must never automatically edit `human-notes.md`.
- AHL must never treat `human-notes.md` as authoritative machine state.
- AHL may mention whether `human-notes.md` is present in status output.
- AHL may read or discuss it only when the operator explicitly provides it or
  asks for help with its contents.
- Reusable snippets may be copied into the file by the operator, but AHL should
  generate snippets directly rather than rewriting notes.

## Appropriate Human Use

The operator may manually note intentions such as:

```text
told AHL to run prompts 18 through 27
```

That note is an operator reminder, not permission for AHL to run a range or to
infer completion. AHL should still rely on repo files, prompt files, validation
evidence, git history, and explicit operator instructions.

## Relationship To Portable Commands

`project status` may report `human-notes.md` as present or absent. It must not
parse the file, derive next-prompt state from it, or use it to override
promptset or git evidence.

`lifecycle snippets`, `lifecycle context-check`, and commit helpers must not
edit `human-notes.md`. They should emit reusable instruction text or
inspectable reports that the operator can copy manually if desired.
