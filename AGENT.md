# AGENT.md

This file is the first-read bootstrap for coding assistants working in
`agent-harness-lab`.

## First Read Order

1. `AGENT.md`
2. `README.md`
3. `docs/guardrails.md`
4. The single `.prompts/PROMPT_XX.txt` the operator asked you to run
5. Any docs that prompt explicitly references

Do not scan local reference repos by default. Inspect them only when the active
prompt asks for reference influence or when a narrow comparison is needed.

## Before Acting

- Run `git status --short` and identify untracked or modified files before
  editing.
- Read existing hot-spot files before changing them.
- Treat user changes as intentional. Do not revert unrelated work.
- Modify files inside this repo only. Do not edit local clones of
  `agent-context-base`, `pi-mono`, or `claw-code`. Future architecture notes
  are guidance only; do not treat them as implemented runtime capabilities.

## Session Types

- Prompt-authoring sessions create or refine prompts, promptsets, or planning
  material. They should not quietly execute implementation work unless asked.
- Prompt-execution sessions run exactly one prompt in a fresh assistant session.
- Repair or bridge sessions fix blockers, fill small gaps, or prepare a clean
  handoff when a previous execution could not finish cleanly.

When running the promptset, execute one prompt per fresh session unless the
operator explicitly says otherwise.

## Runtime Guidance

Session lifecycle, endcap, bridge, reset, adjacent-prompt readiness, and
permission posture guidance lives in `docs/runtime/`. Use those docs when a
prompt asks for runtime/session behavior or closeout decisions.

Assistant-specific usage guidance lives in `docs/assistants/`. Use those docs
when a prompt or operator asks how to run this repo with Codex, Claude Code,
Gemini, Pi, generic chat, or subscription-friendly workflows. Keep that
guidance tool-agnostic unless the current environment proves a capability.

## Project Skills

Optional project-level skills live in `.agents/skills/`. They are on-demand
instruction packages for recurring harness routines, not mandatory startup
context and not hidden automation. Load one only when it matches the active
task, either through a tool command such as `/skill:trajectory-evaluator` or by
reading the relevant `.agents/skills/<name>/SKILL.md` file directly.

The closeout-focused `trajectory-evaluator` skill is available at
`.agents/skills/trajectory-evaluator/SKILL.md` for post-Endcap evaluation. Use
it when a prompt or operator asks for trajectory evaluation; otherwise the
standard Endcap routine below is enough.

## Helper Scripts

`scripts/ahl.py` is available for lightweight local checks and scaffolding:
`doctor`, `promptset`, `resume`, `checkpoint`, `scaffold-run`, and
`new-handoff`. Treat it as helper tooling for the human-assisted workflow, not
as an autonomous runner or provider integration.

The `doctor` command includes conservative safety hygiene checks for stale
handoffs, missing ignore rules, transcript dump paths, and secret-looking file
names. It does not scan file contents and is not a security scanner.

The repo also has a small Makefile console for common helper actions. Use
`make help` for the stable target list, and use direct `python3 scripts/ahl.py`
calls when you need JSON output, extra arguments, or scaffold commands outside
the Makefile surface.

## Endcap Routine

Use this closeout loop for prompt-execution sessions:

1. Execute the requested prompt.
2. Audit every required deliverable against the prompt.
3. Preflight the next prompt for obvious readiness issues.
4. Bridge only if there is a real blocker or non-trivial warning.
5. Reset by leaving the repo ready for the next fresh session.

Create `tmp/HANDOFF.md` only when it materially helps the next session. Do not
create or update it for routine completion notes that fit in the final answer.

## Validation

Before claiming completion:

- Verify required files and paths exist.
- Review changed docs for claims that overstate implemented features.
- Run available checks when the prompt requires them or when they are cheap and
  relevant.
- State any checks you could not run.

Use `docs/quality/` for validation gates, promptset quality, audit protocol,
severity, completion states, and failure classification. Cheap local checks
include:

```sh
python3 scripts/ahl.py promptset
python3 scripts/ahl.py doctor
python3 scripts/ahl.py validate
python3 -m unittest tests/test_ahl.py
```

## Commit Hygiene

Do not commit unless the operator asks. When commits are requested, prefer
small reviewable commits grouped by coherent change, not one large catch-all
commit. Prefix every commit subject with the active prompt id, for example
`[PROMPT_01] Bootstrap foundation docs`.

Use multi-line commit messages in Tim Pope style: a short imperative subject,
a blank line, then wrapped explanatory body lines when useful. Create those
messages with a heredoc so body lines are real newlines and no raw `\n`
characters appear in the commit message, for example:

```sh
git commit -F - <<'EOF'
[PROMPT_01] Bootstrap foundation docs

Explain why this change belongs together and call out any meaningful
validation or follow-up context.
EOF
```

## Hot-Spot Files

Treat shared files as integration targets. Read them first, preserve useful
existing structure, and update them surgically instead of rewriting them just to
fit a new outline.

Current and expected hot spots include:

- `README.md`
- `AGENT.md`
- `docs/README.md`
- `docs/operator-console.md`
- `scripts/README.md`
- `scripts/ahl.py`
- `tests/test_ahl.py`
- `Makefile`
- `CHANGELOG.md`
- `docs/release-readiness.md`
- `docs/known-limitations.md`
- `docs/maintenance.md`
- `docs/contributing.md`

## Core Guardrails

Follow `docs/guardrails.md`. In short: keep this repo distinct from the
reference projects, favor inspectable artifacts before automation, preserve the
human-assisted subscription-friendly workflow, and treat repo files plus git
history as the durable source of truth.
