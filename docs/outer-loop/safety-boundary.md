# Outer Loop Safety Boundary

The outer loop is allowed only as bounded automation around an already explicit
baseline workflow. Prompts 01 through 32 established prompt files, startup
rules, validation checks, completion audit, next-prompt readiness, bridge
handoff judgment, and commit hygiene. A runner can help only if it exposes its
decisions through files and structured output that the operator can inspect.

## Consent Model

- Dry-run first: planning, driver capability checks, payload previews, and
  validation-gate plans must work without invoking an assistant.
- Live assistant invocation requires explicit `--execute` style consent.
- Commit execution requires a separate explicit approval even when a live run
  was authorized.
- The MVP must not run prompts in parallel.
- The runner must stop when an approval boundary is reached.

## Provider And Credential Boundary

- No hidden provider abstraction is allowed in the MVP.
- No provider credentials, API keys, refresh tokens, browser cookies, or
  account secrets may be stored by AHL.
- Subscription CLIs may be used only when the operator has authenticated the
  tool outside AHL.
- API-backed drivers belong to an explicitly designed later phase with cost,
  credential, logging, and consent handling.

## Data Boundary

- Raw transcript storage is off by default.
- Durable records should be concise summaries, run ledger entries, validation
  evidence, completion audit notes, readiness notes, and commit plans.
- Temporary files must be named and located so `doctor` and data-hygiene
  guidance can inspect them.
- Secrets and sensitive transcripts must not be promoted into docs, memory, or
  run records.

## Git Boundary

- No destructive git operations.
- No staging, commits, pushes, tags, releases, or publishes unless explicitly
  requested.
- Dirty working trees must be inspected before each prompt.
- Unrelated changes must be preserved.
- Unexpected git state must stop the run instead of being normalized by the
  runner.

## Failure Handling

The runner must handle these cases cleanly by stopping and recording the reason:

- rate limits;
- context exhaustion;
- authentication failure;
- assistant CLI command failure;
- validation failure;
- completion audit failure;
- next-prompt readiness blocker;
- unsafe git state;
- unexpected generated files;
- missing required docs or prompts.

After unexpected state, the runner should not improvise a new scope, skip
validation, rewrite history, retry indefinitely, change providers, or continue
to later prompts. It should leave an inspectable failure record and wait for
operator direction.

