# Domain Packs

Domain packs are optional, repo-local bundles for specialized work habits. They
extend the harness with domain examples, routines, validation notes, and
templates without changing the core doctrine every operator must load.

Use a domain pack when a recurring kind of work needs vocabulary, evidence
expectations, or repeatable checks that are too specific for the core lab. Keep
the pack small enough for a fresh session to inspect quickly, and treat it as a
starter context bundle rather than an installed runtime extension.

## What Belongs In A Pack

A pack may include:

- A `pack.json` manifest with id, purpose, optional status, and referenced
  files.
- A short `README.md` explaining when to use the pack.
- Domain-specific roles, routines, templates, validation notes, and examples.
- Concrete stop conditions, evidence expectations, and review criteria.

Pack files should point to durable repo artifacts and should be readable as
plain markdown or JSON. They should not require hidden state, provider-specific
tools, or package installation.

## What Stays In Core

Core doctrine remains domain-agnostic. Keep these topics in core docs:

- Fresh-session execution, prompt boundaries, closeout, preflight, and bridge
  decisions.
- Human operator authority, permission posture, and commit hygiene.
- General role boundaries, contract shapes, validation gates, and metadata
  rules.
- Guardrails that apply to every prompt regardless of domain.

If a rule should apply to every user of the lab, it belongs in core doctrine or
runbooks, not in a domain pack.

## Optional Use

Domain packs are never required for core usage. An operator may ignore
`domain-packs/` entirely and still run prompts, audits, handoffs, and helper
checks. A prompt or task should name a pack explicitly before a fresh assistant
loads it.

Packs do not spawn agents, install plugins, add dependencies, or grant extra
authority. They are inspectable context bundles for specialized manual work.

## Validation

Run the lightweight manifest check before relying on a pack:

```sh
python3 scripts/ahl.py domain-pack check
```

The command parses each `pack.json`, checks required manifest fields, verifies
referenced files exist, and reports structured results. It does not validate
pack prose quality or decide whether a pack should be used.

Reviewers should also confirm that pack guidance is optional, scoped to the
domain, and does not contradict core guardrails.

## When Not To Create A Pack

Do not create a domain pack when:

- The guidance is useful to every prompt and belongs in core docs.
- The domain is a one-off task with no repeatable routine.
- The pack would mostly duplicate role packs, lane playbooks, or templates.
- The work needs dependency management, installation, marketplace metadata, or
  provider integrations.
- The domain guidance would force one workflow onto unrelated users.

Start with a short routine, example, or note first. Promote it into a pack only
after repeated work shows the specialized context is worth maintaining.

## Included Starters

- `_template/` - compact reusable skeleton for new domain packs.
- `software-docs/` - modest example pack for documentation-heavy software
  building work.
