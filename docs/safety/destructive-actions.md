# Destructive Actions

Destructive actions remove, overwrite, rewrite, or externally publish state.
They require explicit operator approval unless the active prompt specifically
authorizes a narrow safe action.

## Before Running One

Check:

- `git status --short`
- whether the path is inside this repo
- whether the file is tracked, untracked, ignored, or user-created
- whether a smaller non-destructive edit solves the problem
- whether the prompt explicitly allows the action

Stop and ask when the command would delete files, rewrite history, clean ignored
artifacts, force overwrite generated files, push commits, deploy, or modify an
external system.

## Never Do Automatically

- `git reset --hard`
- `git checkout -- <path>` to discard user work
- broad cleanup commands over unknown directories
- forced overwrites of handoffs, memory candidates, reports, or run records
- deletion of local reference repos

When cleanup is appropriate, name the exact path, explain why it is safe, and
let the operator approve or perform it.
