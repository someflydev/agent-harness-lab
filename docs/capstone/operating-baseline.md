# Operating Baseline

This baseline defines the supported operating model after the initial
`agent-harness-lab` promptset. It is the baseline for Prompts 01 through 32.
Prompts 33 and later, if present, are optional phase-two work.

## Starting The Repo

An operator starts with:

1. Read `README.md` for project identity and current status.
2. Read `AGENT.md` before assigning a coding assistant session.
3. Choose exactly one `.prompts/PROMPT_XX.txt` file for a fresh session.
4. Have the assistant read `docs/guardrails.md`, the active prompt, and any
   docs explicitly named by the prompt.
5. Run `git status --short` before editing and preserve unrelated changes.
6. Execute the prompt, validate, audit deliverables, preflight the next prompt,
   and commit only when the operator chooses to do so.

## Expected Passing Commands

The baseline expects these local commands to pass in a normal clean setup:

```sh
make help
make doctor
make promptset
make lint-prompts
make check-docs
make test
make registry
make dry-run
make lane-check
make memory-check
make experiment-check
make domain-pack
python3 -m unittest tests/test_ahl.py
```

The `doctor` command is the current safety hygiene entry point. There is no
separate `safety` subcommand in `scripts/ahl.py`.

## Baseline-Supported Workflows

- Fresh-session execution of one bounded prompt at a time.
- Manual completion audit against the active prompt.
- Immediate next-prompt readiness preflight.
- Bridge handoff creation only when an unresolved blocker or warning would
  otherwise be lost.
- Operator-controlled commit packaging with prompt-id commit prefixes.
- Local structural validation for prompts, docs, registries, dry-runs, lane
  simulations, memory candidates, experiments, and domain packs.
- Manual role, lane, review, repair, promotion, and assistant-usage routines.
- Findings and experiment recording through templates and helper scaffolds.

## Manual Responsibilities

The operator remains responsible for:

- Selecting the next prompt.
- Deciding whether to grant permissions.
- Reviewing assistant changes and validation evidence.
- Deciding whether a temporary handoff is justified.
- Choosing commit boundaries and whether to commit at all.
- Resolving real-world ambiguity that structural checks cannot prove.
- Keeping product-specific assistant guidance current when tools change.

## Not Yet Implemented

The baseline does not implement:

- Provider or assistant invocation.
- A sequential runner for multiple prompts.
- Parallel prompt execution.
- A daemon, queue worker, TUI, MCP server, or REPL.
- Credential or secret management.
- Live multi-agent orchestration.
- Raw transcript storage as durable memory.
- Graph or vector retrieval.
- Semantic proof that a prompt was completed correctly.

## Recording Findings

Real usage findings should be recorded in `findings/` when they capture a
durable observation, risk, or improvement candidate. Experiments should be
planned and closed through `experiments/` when the work is a bounded trial.
Memory candidates should go through `memory/` and `docs/memory/` promotion
workflow rather than being copied from raw assistant chatter.

Use helper commands when they fit:

```sh
python3 scripts/ahl.py finding new <slug>
python3 scripts/ahl.py experiment start <slug>
python3 scripts/ahl.py memory propose <slug>
```
