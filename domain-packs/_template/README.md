# Domain Pack Template

Use this template as the smallest useful starting point for a new optional
domain pack. Copy the directory, rename the pack id, and keep only guidance
that is specific to the domain.

## Files

- `pack.json` - manifest checked by `scripts/ahl.py domain-pack check`.
- `roles.md` - domain-specific role emphasis, if any.
- `routines.md` - repeatable work routines.
- `templates.md` - links or sketches for reusable domain artifacts.
- `validation.md` - domain evidence and review expectations.
- `examples/README.md` - small examples or pointers to example artifacts.

## Boundaries

Keep the pack optional. Do not move core prompt execution, closeout, validation
gate, or permission rules into this directory. If a rule applies to every
domain, update core docs instead.
