# Subscription Workflow

`agent-harness-lab` is designed for subscription-level coding assistants and
manual assistant sessions because the core workflow is prompt-bounded,
file-based, and operator-directed. A session does not need a provider API,
daemon, queue, or autonomous runner to be useful.
AHL produces snippets, prompt payloads, plans, reports, and validation helpers;
the human operator or selected assistant CLI executes the actual prompt work.

## Why Subscription-Level Tools Fit

Subscription tools are practical for this repo when the operator keeps work
small and inspectable:

- prompts are numbered and bounded;
- startup context is explicit;
- validation commands are local;
- closeout evidence is written in final notes or repo artifacts;
- git history remains the durable review surface.

This keeps the harness usable in Codex, Claude Code, Gemini, Pi, and generic
chat sessions without making any one tool mandatory.

Codex, Claude Code, Gemini, and generic chat surfaces should all use the same
file-backed loop: repo files and prompt files define the work, local
validation proves it, git history records reviewed commits, and the operator
controls scheduling and commit approval.

## Manual Prompt Copying

When the assistant cannot read files directly:

1. Paste `AGENT.md`.
2. Paste the relevant parts of `README.md` and `docs/guardrails.md`.
3. Paste the active `.prompts/PROMPT_XX.txt`.
4. Paste only docs and source files named by that prompt.
5. Ask for patch-style output or focused replacement sections.

Avoid pasting broad directories, transcripts, reference repos, or future
prompts. If the assistant needs more context, add the smallest file or excerpt
that resolves the question.

## Keep Sessions Bounded

Run one prompt per fresh session. If the prompt exposes a small readiness issue
that blocks the current work, fix it only when it is within the prompt's
bridge or endcap scope. Otherwise leave a concise handoff and stop.

Bounded sessions reduce hidden state, conserve context, and make review easier.

## Avoid Wasting Quota

Use the context-loading matrix in `context-loading.md` before pasting or
loading files. Prefer:

- startup docs before broad search;
- prompt-named docs before entire doc trees;
- focused file excerpts before whole unrelated files;
- local validation output before long assistant speculation.

Do not spend quota asking an assistant to rediscover repo navigation that is
already in `docs/README.md`, `runbooks/`, or `prompt-templates/`.

## Rate Limits And Context Exhaustion

If a subscription session hits rate limits or context exhaustion:

1. Stop expanding scope.
2. Save durable work in repo files if edits are complete.
3. Run available local checks.
4. Create `tmp/HANDOFF.md` only if the next session needs blocker context that
   is not already captured elsewhere.
5. Resume in a fresh session by loading `AGENT.md`, the active prompt, the
   current git status, and the handoff if one exists.

Do not rely on the exhausted chat transcript as the only memory.

## Workflow Modes

Subscription-CLI usage means a local assistant tool operates inside the working
tree under the operator's subscription and permission settings.

API-backed provider runtimes would call provider APIs from repo-owned or
operator-owned automation. This repo does not currently implement that runtime.
Claude subscription automation is not available through AHL external APIs; use
Claude Code or manual copy/paste workflows unless a future prompt adds a
separate reviewed API-backed design.

Manual copy/paste workflows use a general chat assistant with the operator
moving text, patches, and validation output between the repo and chat.

All three modes should preserve the same core loop: Execute -> Audit ->
Preflight -> Bridge -> Reset.

For portable target projects, `lifecycle snippets` can produce the reusable
run, audit, commit-plan, make-commits, and commit-check text for any of these
surfaces. The snippets are instructions for the operator to paste or hand to a
session; they are not provider automation.

AHL portable helpers do not require network access, secrets, paid APIs, or
provider credentials, and they do not query subscription usage limits
programmatically.

## Future Wrappers

A future outer wrapper may drive supported subscription CLIs one prompt at a
time, collect validation evidence, and help reset sessions. That would be an
automation layer around the existing operating model, not a replacement for
prompt files, repo artifacts, validation checks, or operator approval.
