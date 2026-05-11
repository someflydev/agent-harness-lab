# Commit Check

`commit check` is a read-only post-commit inspection helper for portable
one-prompt workflows. Use it after the operator has approved and created
commits, before deciding whether message cleanup is worth an amend or
interactive rebase.

## Invocation

```sh
python3 scripts/ahl.py commit check --project /path/to/project --prompt PROMPT_84 --json
python3 scripts/ahl.py commit check --project /path/to/project --prompt PROMPT_84 --range HEAD~10..HEAD --json
python3 scripts/ahl.py commit check --project /path/to/project --last 7 --json
```

Without `--project`, the command inspects the current working directory. If
`--prompt` is supplied without `--last` or `--range`, it searches the most
recent 10 commits for subjects prefixed with that prompt id and warns that the
search may be truncated. If that prompt-default search finds no matching
commit, the command fails instead of silently passing.

When `--prompt` is combined with an explicit `--last` or `--range`, the command
inspects the selected commits against the requested prompt prefix. Commits in
that explicit selection whose subjects do not start with the requested prompt
are reported with `missing_prompt_prefix`.

## Checks

The helper reports:

- missing subject prefixes such as `[PROMPT_84]`;
- Tim Pope-style subject, blank line, then body when a body exists;
- overlong subject guidance;
- unwrapped body or secondary lines;
- literal `\n` sequences;
- co-author trailers;
- generated assistant boilerplate;
- merge commits that need manual grouping review;
- commit count, prompt-prefix counts, changed-file count, and top-level
  changed directories;
- searched, matched, and unmatched commit counts in the selector summary.

When it finds a clear issue, it may print suggested `git commit --amend` or
`git rebase -i` commands as guidance. It does not run those commands.

## Boundaries

The command reads git history and changed-file lists only. It does not stage,
commit, amend, rebase, reset, push, tag, edit files, invoke assistants, or
require credentials.
