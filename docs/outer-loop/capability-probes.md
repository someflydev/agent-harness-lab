# Capability Probes

Capability probes are safe local checks for assistant driver records. They help
the outer-loop runner decide whether a configured driver is locally plausible
before any live assistant call is allowed.

## What Probes Check

- The driver registry exists and has structurally valid records.
- A non-manual driver's expected executable is present on `PATH`.
- A help-only command can be run when the operator requests it with
  `--help-only`.
- Probe results can be emitted as stable JSON with `ok`, `drivers`, `checks`,
  and `problems`.

## What Probes Do Not Check

- They do not send prompts to a model.
- They do not create, resume, or name assistant sessions.
- They do not authenticate, refresh tokens, or inspect credential stores.
- They do not prove subscription status, quota, rate-limit headroom, or model
  availability.
- They do not write transcripts or provider output artifacts.

## Missing Executables

A missing executable means the local machine cannot currently satisfy that
driver's command contract from `PATH`. It is not a project failure by itself and
it does not mean the assistant product is unsupported globally. It means a later
batch plan should either choose another configured driver, ask the operator to
install or expose the CLI, or fall back to a manual flow.

## Records Versus Auth State

Driver records are repo-local descriptions. They are safe to commit because
they contain command names, capability notes, and unsupported operations rather
than secrets. Local authentication state belongs to the assistant tool and the
operator's machine, not to AHL.

## Deferred Live Calls

Live model calls are deferred because they may spend quota, change files, create
remote or local session state, and hit provider-specific approval boundaries.
The first driver layer therefore stops at contract validation and capability
inspection. Later prompts must add explicit `--execute` style consent before
any assistant invocation.
