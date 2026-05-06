# Assistant Driver Contracts

Assistant driver contracts describe local commands that a later outer-loop
runner may inspect before attempting one prompt-bounded assistant session. They
are not provider SDKs and they are not live-run authorization.

## Boundary

A driver contract describes a command: the expected executable, conservative
invocation shape, prompt input method, output expectations, session behavior,
and known unsupported operations.

A capability probe checks local availability: whether the configured executable
is present on `PATH` and, when explicitly requested, whether a help command can
run without sending a prompt.

A live run may spend quota, create or resume an assistant session, modify files,
or hit authentication and rate-limit boundaries. Live runs are deferred to later
prompts and must require explicit execution consent.

## Driver Record

Driver records live in `registry/assistant-drivers.json`. Each record includes
the normal registry fields plus driver-specific fields:

- `id`: stable driver id, such as `codex`.
- `display_name`: human-readable name shown in plans and logs.
- `driver_kind`: one of `subscription-cli`, `api-cli`,
  `external-harness`, or `manual`.
- `executable_name`: command expected on `PATH`, or `null` for manual drivers.
- `supported_invocation_modes`: conservative modes the contract can describe,
  such as `interactive`, `headless`, `print`, or `manual`.
- `prompt_input_methods`: one or more of `argument`, `stdin`, `prompt_file`,
  `tool_specific_option`, or `manual`.
- `structured_output_support`: whether the tool is known to emit stable machine
  output and what evidence supports that claim.
- `final_message_capture_support`: whether a final assistant message can be
  captured without storing a raw transcript.
- `sandbox_approval_controls`: documented permission, sandbox, or approval
  controls if known.
- `model_selection_support`: documented model selection surface if known.
- `reasoning_selection_support`: documented reasoning or thinking selection
  surface if known.
- `fresh_session_behavior`: how a new prompt-bounded session is expected to be
  started.
- `resume_behavior`: whether previous sessions can be resumed and what remains
  unverified.
- `capability_probe`: safe probe details, limited to executable lookup and
  optional help output.
- `known_limitations`: explicit gaps or unverified assumptions.
- `unsupported_operations`: actions AHL must not infer from the contract.

## Initial Drivers

The initial registry contains conservative records for Codex, Gemini, Pi, and
manual execution.

Codex and Gemini are represented as subscription CLI candidates. Their records
describe local command expectations and mark live behavior as requiring local
verification.

Pi is represented as an external harness candidate because the local reference
README describes interactive, print or JSON, RPC, and SDK modes. AHL records
that context without copying Pi internals or editing `pi-mono`.

The manual driver records copy/paste or human-operated sessions. It has no
executable and no local authentication probe.

Claude subscription automation is deliberately absent as an external driver.
Future Claude work should be represented only as a manual/Claude-Code-local
path or as an explicitly designed API-backed driver with cost, credential, and
consent handling.

## Contract Limits

Driver contracts do not prove that the operator is authenticated, that quota is
available, that a model can edit files, or that a tool's help text guarantees
headless execution. They are inspectable starting points for dry-run planning,
not authorization to call a model.
