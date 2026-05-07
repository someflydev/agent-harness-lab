# Pi Vs AHL

Pi and AHL solve adjacent but different problems.

Pi is an interactive and programmatic coding-agent harness. It owns the terminal
experience, providers, model selection, session storage, context files, tools,
skills, extensions, prompt templates, packages, thinking settings, and
programmatic integration modes.

AHL is a promptset, validation, traceability, and orchestration lab. It owns the
bounded prompt workflow around assistants: prompt files, startup context,
guardrails, dry-run plans, gate reports, ledgers, commit plans, readiness
checks, and human closeout.

## Why AHL Should Not Reimplement Pi

Rebuilding Pi's TUI, provider runtime, extension system, session tree, model
registry, package loading, or OAuth flows would move AHL away from its role as a
small inspectable harness lab. AHL should keep those concerns external and use
Pi only through a narrow, verified command boundary when that boundary is
actually useful.

## When Pi Is Sensible

Using Pi as the external driver is sensible when the operator already works in
Pi, needs Pi's provider/model coverage, wants Pi's skills or extensions, or
needs a Pi-managed session/tool environment while still using AHL for prompt
selection, validation, and run records.

## When Direct Drivers Are Simpler

Direct Codex or Gemini CLI drivers are simpler when the operator wants a narrow
subscription CLI run with a prompt payload, explicit `outer run --execute`
consent, and minimal command mapping. They avoid adding Pi's harness layer when
Pi-specific provider routing, extensions, sessions, or output modes are not
needed.
