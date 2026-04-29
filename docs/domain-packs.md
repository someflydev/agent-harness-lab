# Domain Packs

Domain packs are optional context bundles for specialized domains. They let the
lab carry examples, routines, validation notes, and template guidance for a
recurring domain without making that domain part of core doctrine.

The top-level pack index lives at `../domain-packs/README.md`. Each pack should
have a `pack.json` manifest and enough markdown for a fresh session to inspect
the domain guidance quickly.

## Use Pattern

1. Run the normal prompt startup from `AGENT.md`.
2. Load a domain pack only when the operator or active prompt names it.
3. Treat pack guidance as optional context, subordinate to core guardrails and
   prompt-specific instructions.
4. Run `python3 scripts/ahl.py domain-pack check` after adding or changing pack
   manifests.

## Current Packs

- `_template` - reusable starter structure.
- `software-docs` - modest example for documentation-heavy software work.

## Boundaries

Domain packs do not install packages, act as plugins, provide a marketplace,
or change the required core workflow. If guidance applies to all harness work,
place it in doctrine, runbooks, templates, or role docs instead.
