# Routines

Routines are reusable sequences of behavior that an operator or assistant can
run. They are practical operating building blocks. The runbooks in
`../../runbooks/` provide operator-facing procedures, while this directory keeps
the smaller reusable routine vocabulary.

Routines differ from skills. A skill is a capability, such as artifact
verification. A routine sequences skills into a repeatable activity, such as a
completion audit.

## Documents

- `catalog.md` - initial routine catalog with purpose, inputs, outputs, stop
  conditions, and automation potential.
- `micro-routine-library.md` - detailed reusable micro-routines for scope,
  assumptions, validation discovery, audit, readiness, handoff, promotion,
  closeout, and repair triage.
- `routine-record-format.md` - simple markdown record format for future
  runbooks and scripts.

## Use

Use this catalog when naming repeated session behaviors in prompts, operator
guidance, future runbooks, templates, and helper scripts. Do not treat a
routine as automated unless a later artifact provides the script, contract, and
validation path.
