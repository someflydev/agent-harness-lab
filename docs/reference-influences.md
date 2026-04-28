# Reference Influences

Local copies of `agent-context-base`, `pi-mono`, and `claw-code` may be present
as reference material. They are influences, not parent projects to clone. This
repo should adapt compatible ideas while preserving its own human-assisted,
subscription-friendly operating model.

## agent-context-base

Compatible ideas:

- Deterministic startup boot sequence.
- A `work.py resume` style context briefing that reports branch, runtime file
  sizes, complexity posture, and a recommended next step.
- `checkpoint` drift detection to catch divergence before work proceeds.
- Concrete runtime files such as `context/TASK.md`, `context/SESSION.md`, and
  `context/MEMORY.md` that can give a fresh assistant grounded restart state
  without relying on hidden memory.
- Prompt discipline and explicit validation gates.
- Memory compaction versus promotion discipline.
- A two-layer model that separates operator sequencing from assistant
  execution.

These are context-discipline and workflow ideas. They should not be imported as
a full operating system for this repo.

## pi-mono

Compatible ideas:

- Minimal harness surface.
- Extensibility over framework gravity.
- Skills as directory packages, such as `dir/SKILL.md` with frontmatter, loaded
  on demand rather than at boot.
- Prompt templates as named workflow-specific starting points.
- Explicit context files instead of full-directory scans.
- "Adapt the tool to your workflow, not the other way around" as a design
  filter.

These ideas support a small, inspectable harness. They should not turn this repo
into a clone of `pi-mono` or require its exact packaging model.

## claw-code

Compatible ideas:

- Doctor or preflight as a first command with machine-readable structured
  output, not prose-only output.
- Stable field names such as `ok`, `checks`, and `problems` so downstream
  automation can key off results without prose parsing.
- `PARITY.md` as a canonical scenario-coverage tracker with per-lane status
  tables and evidence links.
- Permission posture as named, inspectable categories with explicit allowed and
  denied lists.
- Idempotent init with `created`, `updated`, and `skipped` reporting per
  artifact.
- Recoverable operating loops.

These ideas are useful where they preserve clarity, recovery, and auditability.
They should not pull this repo toward a heavy autonomous runtime.
