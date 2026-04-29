# Software Docs Domain Pack

This optional pack is for documentation-heavy software-building work, such as
updating operator docs, template docs, API-facing explanations, or validation
notes around a code change.

Use it only when the active assignment benefits from a docs-focused lens. It
does not replace core prompt execution, role boundaries, or validation gates.

## Best Fit

- A prompt changes both code and docs and needs claims checked carefully.
- A docs page must explain an existing script, template, or workflow.
- A reviewer needs to compare user-facing claims with actual repo behavior.

## Avoid

- Pure code fixes with no durable documentation surface.
- Broad rewrites of core doctrine.
- Marketing copy, product positioning, or provider-specific integration docs.

## Files

- `pack.json` - pack manifest.
- `routines.md` - docs-focused routines.
- `validation.md` - evidence checks for documentation-heavy work.
