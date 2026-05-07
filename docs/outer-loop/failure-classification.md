# Failure Classification

Failure classes guide recovery. They do not authorize hidden retries or
automatic live assistant invocation.

| Class | Resume Safe | Repair Needed | Explaining Artifact | Runner Must Not Do Automatically |
| --- | --- | --- | --- | --- |
| Driver executable missing | No | Yes | run ledger and recovery handoff | Install tools or switch drivers |
| Driver auth failure | No | Yes | run ledger and operator note | Reauthenticate or retry credentials |
| Driver rate limit or quota exhaustion | Later, after review | Usually no code repair | run ledger and recovery handoff | Spin retries or bypass quota |
| Driver timeout | Sometimes | Review required | run ledger step record | Assume prompt completion |
| Prompt execution failed | No | Yes | step summary or recovery handoff | Mark prompt complete |
| Validation failed | No | Yes | gate report and run ledger | Continue to next prompt |
| Completion audit incomplete | No | Yes | completion audit or handoff | Claim semantic completion |
| Next-prompt readiness blocked | No | Yes | readiness/gate report | Start the next prompt |
| Unsafe git state | No | Yes | git status in gate or ledger | Stage, reset, stash, or discard files |
| Unexpected changed files | No | Yes | run ledger and commit plan | Treat unrelated changes as prompt output |
| Commit plan refused | No | Maybe | commit-plan output | Commit, stage, or amend history |
| User interruption | Usually | Review first | run ledger and recovery handoff | Continue without operator confirmation |
| Unknown failure | No | Yes | recovery handoff | Guess a resume point |

## General Rules

- Resume is safe only when completed steps are clearly recorded, the next
  prompt is known, and the worktree is clean.
- Repair is needed when a blocker changes repo state, validation confidence,
  prompt readiness, driver availability, or commit safety.
- The explaining artifact should be concise and durable: run ledger, gate
  report, step summary, commit plan, or recovery handoff.
- The runner must not rerun completed prompts, retry assistant CLIs, edit git
  state, or store raw transcripts without explicit operator action.
