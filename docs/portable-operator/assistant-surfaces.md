# Assistant Surfaces

Portable operator workflows can be used with several assistant surfaces without
making any one provider mandatory. AHL produces prompt payloads, lifecycle
snippets, range plans, status reports, commit-check guidance, and validation
helpers. The human operator or the chosen assistant CLI executes the actual
prompt work.

## Supported Surfaces

Codex can be used through local or manual subscription workflows when the
operator has that surface available. AHL may prepare prompt payloads and local
validation guidance, but the Codex tool and the operator's local permission
posture control the assistant session.

Claude Code can be used as a manual or terminal assistant surface. AHL does
not assume that Claude subscription usage can be automated through external
APIs, browser sessions, cookies, or hidden provider integrations. Any future
Claude API-backed runtime would need a separate reviewed design for cost,
credentials, logging, rate limits, and consent.

Gemini can be used manually or through local CLI behavior only where the
operator has verified that behavior on the machine running the workflow. AHL
does not infer authentication, quota, output capture, or stable headless
behavior from the existence of a Gemini-oriented guide.

Generic chat workflows rely on copy/paste and committed repo files. The
operator moves startup context, prompt text, patch output, and validation
evidence between the repo and the chat session.

Manual sessions are first-class. When no safe local CLI invocation exists, the
operator can still use generated snippets and prompt payloads as instructions
for a fresh assistant session.

## Local-First Boundary

AHL portable helpers do not require network access, secrets, browser cookies,
provider credentials, paid APIs, or machine-readable subscription quotas. They
should remain useful from a checkout with Python and git available.

Portable helpers do not query subscription usage limits programmatically. Rate
limits, context exhaustion, account status, and model availability remain
operator-observed facts unless a future prompt adds a reviewed provider-specific
integration.

`lifecycle snippets` and `lifecycle run-range` are planning and copy/paste
helpers. They do not invoke assistants, execute target-project validation
commands, edit target-project files, stage changes, commit, amend, rebase, push,
or continue automatically.

Outer-loop live invocation remains separate from the portable helper boundary.
When used, it is explicit, bounded by `outer run --execute`, and limited to
local driver contracts that have conservative registry records. Driver probes
may inspect `PATH` and help output only; they do not authenticate, send prompts,
consume model quota, or prove subscription status.

## Evidence And Closeout

The durable record should stay in repo artifacts and git history:

- prompt files and generated payloads;
- local validation output summarized in closeout notes;
- run ledgers or status reports when a helper creates them;
- commit plans and commit-check reports when packaging is in scope;
- handoffs only when a real blocker or non-trivial warning remains.

Raw assistant transcripts, account secrets, browser state, and provider logs
are not portable operator state by default.
