---
name: promptset-inspector
description: Inspect prompt numbering, scope boundaries, registry alignment, and execution-order health without implementing prompt work.
---

## When To Use

Use for promptset health checks, prompt-order questions, or readiness reviews
that span more than the immediate next prompt. Do not use during normal
single-prompt execution unless the active prompt asks for promptset inspection.

## Required Context

- `.prompts/PROMPT_*.txt` inventory or the target prompt range
- `registry/prompts.json`
- `docs/quality/promptset-quality.md`
- `docs/runtime/prompt-authoring-vs-execution.md`
- Relevant output from `python3 scripts/ahl.py promptset`

## Step-By-Step Behavior

1. Identify the prompt range under review.
2. Check numbering, ordering, and registry alignment.
3. Inspect prompt scope for missing prerequisites, duplicate deliverables, or
   future-work leakage.
4. Distinguish structural issues from prose-quality risks.
5. Recommend prompt repairs only when they are concrete and bounded.
6. Do not implement the inspected prompts.

## Expected Output

- Promptset health summary
- Numbering and registry findings
- Scope or prerequisite warnings
- Suggested prompt repairs, if any

## Stop Conditions

- The inspection would turn into prompt implementation.
- Required prompt files are missing.
- Operator direction is needed to rewrite prompt intent.

## Safety Notes

- `scripts/ahl.py promptset` checks structure, not prompt quality.
- Do not treat registries as exhaustive mirrors.
- Keep findings tied to concrete prompt files.

## References

- `docs/quality/promptset-quality.md`
- `docs/runtime/prompt-authoring-vs-execution.md`
- `registry/prompts.json`
- `prompt-templates/prompt-authoring.md`
- `scripts/README.md`
