# Prompt Templates

Prompt templates are reusable starting prompts for recurring
`agent-harness-lab` routines. They live in `prompt-templates/` and are meant to
be copied into a fresh assistant session, filled with concrete placeholders, and
used manually by the operator.

## Templates Versus Implementation Prompts

`.prompts/PROMPT_XX.txt` files are the ordered implementation promptset. Each
one defines a specific project change to execute once in sequence.

`prompt-templates/*.md` files are reusable routine prompts. They do not define
new project phases, do not belong to promptset ordering, and should not be
treated as required implementation work. A template can help start a prompt
run, audit completion, preflight the next prompt, assign a Worker task, or
package a commit when the operator asks.

## Manual Use

1. Choose the template that matches the routine.
2. Replace placeholders such as `<PROMPT_ID>`, `<TARGET_SCOPE>`, or
   `<AFFECTED_PATHS>` with concrete values.
3. Load only the required context named by the filled template.
4. Run the routine until the expected output or stop condition is reached.
5. Preserve durable results in repo files, reports, commits, or final closeout
   notes as appropriate.

Templates assume no hidden chat history. If prior context matters, it must be
available from repo files, git history, an active `tmp/HANDOFF.md`, or explicit
operator notes.

## Future Tool Loading

A tool with Pi-style project prompt templates could later load these markdown
files directly as named prompts. The files intentionally avoid required
frontmatter, vendor-specific commands, and hidden runtime state so they remain
copyable in ordinary assistant sessions.

If a future tool adds metadata, the markdown body should remain the source that
an operator can read and paste. Tool indexes may point at the templates, but
they should not replace the repo files as the source of truth.

## Not A Second Promptset

The template library must not become another numbered promptset. Templates are
routine launchers and report shapes, not sequenced implementation tasks. Adding
more templates should improve repeated operator actions, not create a parallel
roadmap or bypass `.prompts/PROMPT_XX.txt`.

## Adding A Template

Add a template only when a recurring routine needs a reusable prompt shape that
is not already covered by a runbook or artifact template.

Use this process:

1. Check the relevant runbook, contract, report, or handoff template first.
2. Add one `prompt-templates/<TEMPLATE_NAME>.md` file with purpose, placeholders,
   required context, expected output, and stop conditions.
3. Link it from `prompt-templates/README.md`.
4. Update `registry/templates.json` so it is discoverable.
5. Avoid duplicating the runbook procedure; the prompt template should launch
   the routine, while the runbook remains the procedural source.
