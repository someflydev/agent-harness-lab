# Context Update Policy

Portable prompt closeout includes a context-update check so future fresh
sessions can start with the right durable project knowledge. The check is
review-only: it asks whether context files should change, but it does not
require or automate edits.

## Update Threshold

Update `AGENT.md`, `CLAUDE.md`, `.context/`, or `context/` only when a prompt
introduces or changes durable workflow, architecture, command, convention, or
repo-navigation knowledge that future fresh sessions need before doing useful
work.

Do not update context files merely because a prompt ran. Avoid noisy context
churn, duplicated closeout notes, and temporary task details. Keep context
concise, evidence-backed, and useful to a future assistant that starts without
the prior conversation.

Prefer checked-in docs, runbooks, templates, or script help for broad guidance.
Use context files for bootstrap-critical project facts, current-session state,
or local working memory according to the target project's conventions.

## Audit Outcomes

When no durable context changed, record `no context update needed` as an audit
conclusion. Do not create a file edit just to record that nothing changed.

When there may be a context update, produce a candidate report before editing.
The report should name changed paths, likely durable knowledge, affected
context targets, uncertainty, and the recommended reviewer action.

## Target Files

`AGENT.md` and `CLAUDE.md` are bootstrap files. Keep edits short and limited to
startup-critical rules or navigation.

`.context/` and `context/` may be absent in arbitrary projects. Do not require
either directory to exist. If present, treat them as project-local context
surfaces and follow local ownership rules.

`human-notes.md` is operator-owned and informational only. Assistants may read
it when asked or when lifecycle docs say it is relevant, but should not treat
it as machine authority and should not edit it.

## Helper Support

`python3 scripts/ahl.py lifecycle context-check PROMPT_84 --project <path>
--json` is a read-only helper. It inspects target-project git status and
suggests conservative context-update questions for docs, command-surface,
workflow, template, bootstrap, prompt, and context-file changes.

The helper does not edit `AGENT.md`, `CLAUDE.md`, `.context/`, `context/`, or
any target-project file. Its output is advisory and intentionally uncertain;
human or assistant review decides whether a concise context edit is justified.
