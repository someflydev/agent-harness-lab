# Outer Loop Requirements

The outer loop should automate only the repeatable parts of the existing
human-assisted prompt workflow. It must keep prompt files, repo artifacts, git
history, validation evidence, and operator judgment as the durable source of
truth.

## Target Workflow

The target workflow is:

1. Choose the next prompt range, for example the next 10 prompts.
2. Create a batch plan that lists prompt ids, prompt files, expected startup
   context, validation gates, stop rules, and commit-planning policy.
3. Run prompts sequentially, never in parallel by default.
4. Start a fresh assistant CLI session for each prompt.
5. Pass the prompt file and bounded startup context.
6. Run prompt-required validations after each prompt.
7. Run AHL structural checks after each prompt.
8. Perform completion audit and next-prompt readiness check.
9. Stop on blocker, failed validation, driver failure, or unsafe git state.
10. Produce reviewable commit plans and perform explicit commits only when
    authorized.

Canonical operator example:

```text
Run the next 10 planned prompts in sequence, with a fresh Codex gpt-5.5
medium-reasoning session per prompt file, validating at the end of each run,
checking the next prompt for readiness, then creating appropriately grouped
reviewable commits with correct prompt-id prefixes.
```

This example is a target requirement, not implemented behavior.

## Required Inputs

- A clean enough working tree or an explicit operator-approved dirty-state
  policy.
- A prompt range that maps to existing `.prompts/PROMPT_XX.txt` files.
- Startup context rules derived from `AGENT.md`, `README.md`,
  `docs/guardrails.md`, the active prompt, and prompt-named docs.
- Assistant driver selection for a supported local tool.
- Validation gate selection, including prompt-required commands and AHL
  structural checks.
- Commit policy that defaults to planning only.

## Required Outputs

- A batch plan before execution.
- Per-prompt run ledger entries.
- Validation results after each prompt.
- Completion audit notes for each prompt.
- Immediate next-prompt readiness notes after each prompt.
- Failure records when the runner stops.
- Reviewable commit packages when requested.

## Stop Conditions

The runner must stop rather than continue when it observes:

- missing prompt files or missing required startup docs;
- unrelated dirty state that the operator has not approved for the batch;
- assistant driver launch failure or non-zero command failure;
- provider auth, rate-limit, or context-exhaustion failure;
- prompt-required validation failure;
- AHL structural check failure;
- completion audit failure or unresolved prompt blocker;
- next-prompt readiness blocker;
- unexpected files that imply secrets, raw transcripts, destructive changes, or
  external side effects;
- operator approval required for staging, committing, pushing, tagging,
  publishing, or destructive git operations.

## Commit Policy

The runner may propose commit packages with prompt-id prefixes and supporting
validation evidence. It must not stage, commit, push, tag, or publish unless
the operator explicitly authorizes that action for the current state.

