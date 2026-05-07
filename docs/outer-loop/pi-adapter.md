# Pi Adapter

The Pi adapter is a bounded experiment for treating Pi as an external assistant
harness, not as code to copy into AHL. Local reference docs in `pi-mono`
describe Pi as a terminal coding harness with interactive, print, JSON, RPC,
and SDK modes. AHL only records a conservative contract around those modes and
keeps live use guarded until the operator verifies the local command behavior.

## Relevant Pi Modes

- Interactive mode is useful for manual operator-driven prompt execution. It
  exposes Pi's editor, commands, model selector, session tree, tools, skills,
  extensions, prompt templates, and package system.
- Print mode (`-p` / `--print`) is the likely first headless candidate because
  the Pi docs say it prints a response and exits, and can merge piped stdin into
  the initial prompt.
- JSON mode (`--mode json`) may support structured event capture, but AHL has
  not verified which event should be treated as the final assistant summary.
- RPC mode (`--mode rpc`) is for process integration over JSONL framing. It is
  more powerful than the current AHL helper needs and requires a separate
  protocol client before use.
- SDK mode is explicitly not used by this experiment. Using it would make AHL
  embed Pi rather than drive it as an external harness.

## Driver Differences

Codex and Gemini are subscription CLI drivers in AHL: the local runner maps a
bounded prompt payload to a small command and sends the payload on stdin when
`outer run --execute` is explicitly selected.

Pi is different because it is itself a harness with its own provider runtime,
tooling model, context loading, sessions, extensions, skills, packages,
settings, thinking controls, and output modes. AHL should not reinterpret those
surfaces. The Pi driver remains an `external-harness` record with
`manual-confirmation-required` live status until the exact local command and
output contract are verified.

## Provider And Model Selection

Pi owns provider, model, and thinking selection. Local Pi docs describe
subscription login, API-key providers, `/model`, `/settings`, `--provider`,
`--model`, `--models`, `--list-models`, and `--thinking`.

AHL may record desired model or reasoning values in a plan, but it should not
translate them into Pi command flags by default. That translation belongs to a
future verified Pi-specific contract because Pi's model names, provider
configuration, and thinking levels are Pi runtime concerns.

## Prompt Payload

AHL should pass the same bounded outer-loop payload used for other drivers:

- the active prompt id and prompt body;
- startup context named by the prompt;
- explicit constraints, validation commands, stop conditions, and closeout
  expectations;
- the driver id and recorded plan metadata;
- transcript and credential boundaries.

The payload should not include credentials, raw previous transcripts, or hidden
session state. For a verified print-mode command, stdin plus a concise argument
such as "run this AHL prompt payload" may be enough, but that is not yet
validated.

## Expected Result

AHL should expect only a process status and a short captured or operator-written
summary. It should not store raw Pi sessions by default. A verified integration
would need to identify whether print mode, JSON mode, or RPC returns a stable
final assistant message and how failures, aborts, tool calls, and rate limits
are represented.

## Safe Output Capture

Safe capture is limited to:

- executable path availability;
- help output previews from `pi --help`;
- dry-run plan metadata;
- process return code and a short failure reason if a future command is
  explicitly enabled;
- human-written summaries in run ledgers or step summaries.

AHL should not copy Pi session JSONL files, exported HTML, provider tokens,
package contents, or raw transcripts into durable artifacts unless a later
prompt creates an explicit reviewed policy.

## Required Probes

Before live use, AHL must be able to probe:

- `pi` executable availability on `PATH`;
- `pi --help` availability without sending a prompt;
- whether print mode can run non-interactively in the current project;
- whether `--no-session` prevents persistent session writes where needed;
- whether JSON mode has a stable final-message event;
- how Pi reports authentication, quota, permission, extension, package, and
  tool failures;
- whether the operator-selected Pi settings are safe for unattended execution.

Only the first two are implemented by the current AHL helper.

## Unknowns

The local docs justify a conservative registry record, but they do not prove
that this machine has Pi installed, authenticated, configured safely, or ready
for headless prompt execution. AHL also has not verified Pi final-message
capture, permission controls, session persistence, package side effects, or RPC
framing in an AHL runner.
