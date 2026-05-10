# Assistant Usage Guides

These guides explain how to run `agent-harness-lab` with different coding
assistant tools while preserving the same operating model:

1. Start a fresh session.
2. Load only the required repo context.
3. Run one bounded prompt.
4. Validate the result.
5. Close with Execute -> Audit -> Preflight -> Bridge -> Reset.

The guides are intentionally tool-agnostic where product behavior varies. They
do not make any assistant mandatory, and they do not assume this repo currently
has provider orchestration, API-backed runners, cross-tool automation, network
requirements, secrets, paid APIs, or machine-readable subscription quotas.
AHL produces repo-backed instructions and helper output; the human operator or
chosen assistant CLI executes the prompt work.

## Guides

- `codex.md` - Codex-style coding assistant sessions.
- `claude-code.md` - Claude Code-style terminal assistant sessions.
- `gemini.md` - Gemini-style coding assistant sessions.
- `pi.md` - Pi-style assistant sessions that can use project prompts and
  skills as ordinary repo context.
- `generic-chat.md` - manual copy/paste use in a general chat assistant.
- `subscription-workflow.md` - subscription-friendly operating model, quota
  control, and workflow boundaries.
- `context-loading.md` - small matrix for what to load by session type.
- `../portable-operator/assistant-surfaces.md` - portable boundary across
  Codex, Claude Code, Gemini, generic chat, and manual surfaces.

## Common Operating Model

All assistant paths should use the same durable source of truth: checked-in
repo files, explicit prompt files, validation output, and git history. Assistant
chat history can help during a session, but it should not become durable memory
unless a prompt or review process promotes it into a repo artifact.

When a tool supports commands, skills, file search, or local shell execution,
use those capabilities to reduce manual copying. When it does not, paste the
same startup files and prompt text manually. The workflow remains the same.

Claude Code is treated as a manual or terminal assistant surface. AHL must not
assume that Claude subscription usage can be automated through external APIs,
browser sessions, cookies, or hidden provider integrations.

## Minimum Startup Context

For a normal prompt execution session, load:

- `AGENT.md`
- `README.md`
- `docs/guardrails.md`
- the active `.prompts/PROMPT_XX.txt`
- any docs explicitly named by that prompt

Do not preload broad directories, reference repos, or future prompts unless the
active prompt asks for them.
