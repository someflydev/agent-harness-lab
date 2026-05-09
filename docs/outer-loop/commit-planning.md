# Commit Planning

Commit planning turns prompt-scoped working-tree changes into reviewable commit
groups. It is plan-only by default and does not stage, commit, push, tag, or
amend history.

## Grouping Rules

- Default to one commit per prompt id.
- Group multiple prompt ids only when the changes are tightly related, easy to
  review together, and share the same validation result.
- Never group failed or blocked prompt work with passing prompt work.
- Never include unrelated pre-existing changes.
- Use prompt id prefixes such as `[PROMPT_38]` in every subject.
- Include validation evidence in commit bodies when it helps review.
- Record skipped or unavailable checks honestly.
- Prefer explicit file lists over broad staging.

## Good Grouping

- One prompt updates a doc, schema, fixture, and test for the same CLI feature:
  one `[PROMPT_38]` commit is reviewable.
- Two adjacent prompts only update the same wording in the same operator guide,
  both passed the same checks, and the operator wants a single editorial
  commit: grouping may be acceptable.

## Bad Grouping

- A passing docs prompt and a blocked script prompt in one commit.
- A prompt implementation plus unrelated local notes or run scratch files.
- A broad staging commit that depends on `git add .`.
- A commit body that cites checks that were skipped or unavailable.

## Planner Output

`python3 scripts/ahl.py commit plan PROMPT_38 --json` inspects
`git status --short --untracked-files=all`, reads prompt context when
available, separates modified, untracked, deleted, and staged files, and writes
a commit plan artifact. When a run ledger is supplied, the planner also records
ledger validation evidence and writes `commit-plan.json` beside the ledger.

The planner excludes likely unrelated changes when prompt deliverables list
specific repo paths. The result remains derived metadata: git status, prompt
files, validation output, and operator review remain authoritative.

After the operator makes commits, use the portable read-only check to inspect
message hygiene and grouping evidence:

```sh
python3 scripts/ahl.py commit check --project /path/to/project --prompt PROMPT_38 --json
```

The check may suggest amend or interactive rebase commands when it detects a
clear message issue, but it does not rewrite history.
