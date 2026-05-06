# Assistant Driver Boundary

Assistant drivers are narrow adapters for local assistant tools. They should
make provider-specific behavior explicit instead of hiding it behind a broad
runtime abstraction.

## Terms

- Assistant driver: a narrow local adapter that launches, monitors, and records
  the result of one supported assistant invocation.
- Subscription CLI: a local command-line assistant tool authenticated by the
  operator outside AHL, normally under that tool's subscription and permission
  settings.
- API provider runtime: code that calls a provider API directly and therefore
  needs explicit cost, credential, logging, and rate-limit handling.
- Headless invocation: a non-interactive or minimally interactive command mode
  that can accept a prompt payload and return a clear success or failure
  status.
- Prompt payload: the active prompt plus bounded startup context needed for one
  fresh assistant session.
- Run ledger entry: an inspectable record of one prompt attempt, including
  prompt id, driver, inputs, validation, audit, readiness, stop reason, and
  commit-plan references.
- Validation gate: a command or manual check required before a prompt is
  considered complete.
- Commit package: a reviewable group of changes with a proposed prompt-id
  commit prefix, summary, and validation evidence.

## Supported Direction

Codex and Gemini may be driven through their supported CLIs when the operator
has authenticated those tools outside AHL.

Pi may be adapted as an external harness if its local CLI mode can be driven
safely and inspected.

Claude subscription automation is not provided by AHL outside Claude Code. Any
external Claude automation belongs to an explicit API-backed driver in a later
phase if the operator asks for it.

## Boundary Rules

- Driver capability probes must be explicit per tool.
- Driver configuration must avoid secrets and machine-specific paths.
- The runner must surface the exact driver selected for each prompt.
- A driver failure must stop the batch.
- Driver output must be summarized in durable records without storing raw
  transcripts by default.
- AHL must not claim provider support that has not been implemented and
  validated in this repo.

