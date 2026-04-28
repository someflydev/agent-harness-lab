# Prompt Authoring Vs Execution

Prompt authoring, prompt execution, and repair sessions are different workflows.
Keeping them separate prevents hidden scope drift and makes the promptset
reviewable.

## Prompt-Authoring Sessions

A prompt-authoring session creates or refines prompt files, promptsets,
planning material, or sequencing guidance. It may inspect existing docs and
prior prompts, but it should not quietly execute implementation work unless the
operator asks.

Example: "Draft prompts 12 through 15 for reports and examples" belongs to a
prompt-authoring session.

`PLAN.md` does not generate `PROMPT_XX` files by itself. A plan can inform
prompt authoring, but prompt files are created through dedicated authoring work
with reviewable changes.

## Prompt-Execution Sessions

A prompt-execution session runs exactly one active `PROMPT_XX` file. It reads
bootstrap docs, executes that prompt's deliverables, validates the result,
preflights the immediate next prompt, and resets.

Example: "Run `.prompts/PROMPT_05.txt`" means implement Prompt 05 only. It does
not authorize generating `.prompts/PROMPT_06.txt` or doing Prompt 06's memory
deliverables.

A `PROMPT_XX` execution session does not generate `PROMPT_YY`. If the next
prompt is missing or flawed, report that as a readiness issue or handle it in a
separate prompt-authoring or repair session.

## Temporary Checklists And Handoffs

A prompt-execution session may create a temporary checklist or `tmp/HANDOFF.md`
only when the current scope cannot safely close without it. The handoff should
name the blocker, current status, affected files, validation evidence, and next
safe action.

Routine completion notes belong in the final answer, not in durable memory and
not in a handoff file.

## Repair Or Bridge Sessions

A repair session fixes a bounded blocker or small gap identified by review,
validation, or a prior handoff. It should start with the defect, affected
paths, expected outcome, and stop condition.

Example: "Fix the broken docs link left by Prompt 05" is repair work. "Create
the memory model that Prompt 06 owns" is prompt execution for Prompt 06, not a
repair to Prompt 05.
