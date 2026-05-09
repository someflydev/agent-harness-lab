# One-Prompt Autopilot

## Purpose

Describe the operator-governed loop for taking a new project from planning
assistant discussion through a committed promptset, one-prompt implementation
runs, post-commit inspection, and fresh-session reset.

In this runbook, "autopilot" means repeatable operator choreography. AHL helps
with prompts, snippets, checks, runbooks, and inspectable reports. It does not
schedule prompts by itself, call provider APIs, edit private planning blobs,
or decide that work is complete.

## When To Use It

Use this when the operator wants to apply AHL's one-prompt workflow to a new or
existing local project repo with its own `.prompts/` directory.

Do not use it to bypass prompt review, run multiple prompts in one assistant
session, or turn `human-notes.md` into machine state.

## Roles Involved

- Operator: owns project intent, private planning context, scheduling, review,
  commits, and fresh-session boundaries.
- Planning assistant: helps discuss the project and shape initial context, but
  does not become the durable source of truth.
- Prompt authoring session: turns approved intent into committed prompt files
  and baseline docs.
- Prompt execution assistant: runs exactly one prompt in a fresh session.
- Auditor or reviewer: compares delivered work to the prompt and validation
  evidence before commit decisions.

## Step-By-Step Procedure

1. Discuss the project in ChatGPT or another planning assistant.
   Keep this exploratory. Capture goals, constraints, stack choices, risks,
   non-goals, and likely prompt phases, but do not treat the chat transcript as
   project state.
2. Generate an initial context blob and promptset instructions.
   The blob can include private business goals, design notes, local machine
   details, or operator preferences that are useful for prompt generation.
3. Store private initial context outside the repo.
   Use a private gist, private notes app, encrypted document, or another
   operator-controlled store. Do not commit private blobs or provider
   transcripts merely so AHL can see them.
4. Create the local project repo.
   Initialize git, set the repo-local `user.name` and `user.email` when needed,
   add an appropriate ignore file, and create bootstrap files such as
   `AGENT.md` or `CLAUDE.md` only when they are useful for future sessions.
5. Generate initial `.prompts/PROMPT_XX.txt` files and baseline docs.
   Use the private planning blob as input to the prompt authoring session, then
   commit only the reviewed promptset and non-private baseline documentation.
6. Preflight the generated promptset before committing it.
   Check numbering, strict filenames, prompt scope, required validation,
   adjacent-prompt references, and whether prompt instructions can run in fresh
   sessions without hidden planning-chat context.
7. Commit the preflighted promptset.
   Use coherent commits with clear subjects. Keep generated prompt files,
   bootstrap docs, and baseline docs reviewable.
8. Run implementation one prompt at a time.
   Start each prompt in a fresh assistant session from repo files, not from an
   old chat transcript. The normal command to give a capable coding assistant
   is `Load AGENT.md, then run .prompts/PROMPT_XX.txt`.
9. Use lifecycle snippets for repeated instructions.
   Generate or copy snippets for `run`, `audit`, `commit-plan`,
   `make-commits`, and `commit-check` steps. From the AHL checkout, use:

   ```sh
   python3 scripts/ahl.py lifecycle snippets PROMPT_84 --project /path/to/project
   ```

10. Audit after each prompt.
    Compare deliverables, constraints, validation output, and changed files.
    Inspect only the immediate next prompt for readiness.
11. Run inline repair only while context is fresh and the issue is bounded.
    If the assistant can fix a small validation failure, missing link, or
    narrow audit gap without expanding scope, keep it in the same session.
    Larger repair belongs in a dedicated repair session.
12. Create a handoff only when it is materially useful.
    Use `tmp/HANDOFF.md` for real blockers or non-trivial warnings that a
    future fresh session needs and that are not already captured in durable
    docs, validation output, or the final closeout.
13. Check context update needs.
    At closeout, ask whether `AGENT.md`, `CLAUDE.md`, `.context/`, or
    `context/` needs a concise durable update. If no future fresh-session
    knowledge changed, record `no context update needed`.
14. Preserve the fresh-session reset boundary.
    After audit, optional repair, optional commit packaging, post-commit
    inspection, and context-update review, stop. Start the next prompt in a new
    assistant session.

## Lifecycle Snippet Uses

Use `lifecycle snippets` as copy/paste instruction text, not as an assistant
runner.

- `run`: starts one prompt from the selected bootstrap file.
- `audit_next_readiness_context_update`: asks for completion audit,
  next-prompt readiness, and context-update review.
- `commit_plan`: asks for grouped prompt-prefixed commit suggestions.
- `make_commits`: lets the assistant create commits only after operator
  approval.
- `commit_check`: inspects the resulting commits for prompt prefix, message
  format, grouping, literal `\n`, co-author trailers, and generated boilerplate.
- `repair`: optional bounded repair instructions when `--include-repair` is
  explicitly requested.

## Human Notes Boundary

`human-notes.md` may exist in a target project as operator-owned scratch space.
AHL may report that it exists, but it must not parse it as authoritative state
or edit it automatically. See
`docs/portable-operator/human-notes-boundary.md` for the durable boundary.

## Expected Artifacts

- Private planning blob stored outside the project repo.
- Local target project repo with reviewed `.prompts/PROMPT_XX.txt` files.
- Optional bootstrap or context files that contain only durable
  fresh-session-critical knowledge.
- Prompt-scoped implementation changes.
- Validation evidence in final closeout or repo artifacts.
- Prompt-prefixed commits when the operator chooses to commit.
- Optional `tmp/HANDOFF.md` only for justified blockers or warnings.

## Validation Or Evidence

- Prompt files are sequential, scoped, and preflighted before the initial
  promptset commit.
- Each prompt run has completion audit evidence and next-prompt readiness.
- Commit packaging is separated from implementation and post-commit inspection.
- Private planning context is not committed.
- `human-notes.md` remains operator-owned and untouched by AHL.

## Stop Conditions

- A prompt cannot run without missing private context that should have been
  converted into safe committed docs or prompt text.
- Validation exposes a material blocker that is not bounded repair.
- Commit creation has not been explicitly approved by the operator.
- The next action would run another prompt in the same assistant session.
