# Portable One-Prompt Loop

The portable one-prompt loop applies AHL's file-backed prompt workflow to an
arbitrary target project repo. The operator remains the scheduler, reviewer,
validation authority, and commit authority.

## Operating Loop

1. Inspect the target project with `project status`.
2. Generate lifecycle snippets for the selected prompt.
3. Start a fresh assistant session and run exactly one prompt.
4. Audit the result against that prompt.
5. Inspect only the immediate next prompt for readiness.
6. Decide whether bounded repair is still in scope.
7. Decide whether bootstrap or context files need concise durable updates.
8. Plan commits only after implementation and validation are done.
9. Create commits only after explicit operator approval.
10. Run post-commit inspection.
11. Reset before the next prompt.

## Planning And Promptset Creation

A new project often starts in ChatGPT or another planning assistant. That
planning step may produce a private initial context blob and promptset
instructions, but the durable project state begins only when reviewed prompt
files and baseline docs are written into the target repo.

Store private context outside the repo, such as in a private gist or another
operator-controlled store. Convert only safe, durable, future-session knowledge
into committed prompt files, bootstrap docs, or baseline docs.

Before the first promptset commit, preflight:

- `.prompts/PROMPT_XX.txt` numbering and filename shape;
- prompt scope, constraints, and validation commands;
- adjacent-prompt references;
- whether a fresh assistant can run each prompt from repo files alone;
- whether private planning content has been excluded.

## Snippet Flow

Use lifecycle snippets to keep instruction text consistent across Codex,
Claude Code, Gemini, and generic chat surfaces:

```sh
python3 scripts/ahl.py lifecycle snippets PROMPT_84 --project /path/to/project
```

Use the generated `run` snippet for the active prompt. After implementation,
use the audit snippet to ask for deliverable audit, next-prompt readiness, and
context-update review. Use commit-plan and make-commits snippets only when the
operator is ready to package validated work. Use commit-check after commits
exist.

The snippets are copy/paste guidance. They do not run assistants, edit files,
stage changes, commit, or call providers.

For a reviewed range request such as "run prompts 18 through 27", use
`lifecycle run-range` to generate a dry-run phase plan first:

```sh
python3 scripts/ahl.py lifecycle run-range 18 27 --project /path/to/project --dry-run --json
```

The range plan preserves the same one-prompt loop. It creates per-prompt run,
audit, optional repair, commit-plan, explicit commit, commit-check, and
fresh-session boundaries, but it does not invoke assistants or continue
automatically.

## Repair And Handoff

Inline repair is appropriate when the issue is small, fresh, and clearly tied
to the active prompt, such as a failed docs link check or a narrow missing
deliverable. If the issue expands beyond the active prompt, stop and use a
dedicated repair session.

Create `tmp/HANDOFF.md` only when a real blocker or non-trivial warning would
otherwise be lost. Routine summaries belong in the final assistant closeout,
not in temporary memory.

## Context Update Review

At closeout, check whether durable context changed. Update `AGENT.md`,
`CLAUDE.md`, `.context/`, or `context/` only when future fresh sessions need
new workflow, architecture, command, convention, or repo-navigation knowledge.

When no update is justified, record `no context update needed`. Do not edit
context files just to prove the check happened.

## Boundaries

- No provider-specific automation, credentials, daemons, network calls, or
  hidden state.
- No automatic prompt scheduling or multi-prompt execution in one assistant
  session.
- No automatic editing of `human-notes.md`.
- No reliance on private planning blobs after prompt files and docs have been
  generated.
- No commits without explicit operator approval.

For the full operator procedure, see
`../../runbooks/one-prompt-autopilot.md`.
