# Skill Maturity Model

Skill maturity describes how reliable and operationalized a capability is. It
does not describe role authority, and it does not imply automation by name
alone.

## Ladder

| Level | Meaning | Evidence Needed |
| --- | --- | --- |
| Named concept | The skill has a stable name and purpose. | Glossary, taxonomy, or doctrine reference. |
| Human-operated checklist | A human can run the skill by following explicit checks. | Checklist or closeout questions with examples. |
| Prompt template | A reusable prompt shape can invoke the skill consistently. | Template with inputs, outputs, and stop conditions. |
| Assistant routine | A coding assistant can perform the skill in a bounded session. | Routine record, required inputs, expected outputs, and validation evidence. |
| Helper-script supported | A small local script supports repeatable parts of the skill. | Script, docs, examples, and failure behavior. |
| Runtime-automated | A runtime can trigger or complete the skill with durable evidence. | Contracts, manifests, tests, operator override path, and audit trail. |

## Early Project Posture

Most early skills should remain at one of these levels:

- named concept
- human-operated checklist
- prompt template
- assistant routine

Helper scripts should appear only when the manual routine is repeated enough to
justify automation. Runtime automation should come later, after the repo has
clear contracts, validation evidence, and operator override paths.

## Advancement Rules

A skill can advance only when the lower level is already understandable. For
example, a helper script should not exist before the repo knows what inputs it
expects, what outputs it should produce, and what failure signals matter.

Advancement should preserve traceability. A more mature skill should still
connect back to the prompt, artifact, command, or review evidence that supports
its result.

## Anti-Claims

Avoid these claims until evidence exists:

- A checklist is not automation.
- A prompt template is not a guarantee of correct execution.
- An assistant-executed routine is not a persistent runtime capability.
- A helper script is not the source of truth; durable repo artifacts remain the
  source of truth.
- Runtime automation is not acceptable without review, stop conditions, and
  audit evidence.
