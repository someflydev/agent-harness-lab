# Organization Model

`agent-harness-lab` uses an Orchestrator -> Leads -> Workers model for
prompt-bounded assistant work. The model is designed for human-assisted
orchestration, not autonomous management software. A single operator can enact
the hierarchy by starting separate assistant sessions with different role
prompts and context bundles.

## Why Hierarchy Matters

Hierarchy matters because agent work fails differently from ordinary human
coordination. Assistants can absorb too much context, drift from the active
prompt, overfit to transient conversation, or make broad changes while trying
to be helpful. Role hierarchy narrows authority before work begins.

The hierarchy gives each layer a different job:

- The Orchestrator protects intent, scope, sequencing, and cross-lane
  coherence.
- Leads protect lane scope, task decomposition, Worker review, and lane-local
  memory.
- Workers protect bounded execution and structured reporting.

This separation controls cost, context bloat, and failure blast radius. A
Worker that receives only a narrow task can fail locally without corrupting the
whole prompt-bounded work unit. A Lead can replace or repair that slice without
forcing the Orchestrator to re-plan every lane.

## Context Narrows Downward

Context should become smaller and more concrete as it moves down the hierarchy.
The Orchestrator may inspect the broad prompt, repo doctrine, prior accepted
work memory, and next-prompt readiness concerns. A Lead receives only the lane
charter, relevant boundaries, and enough surrounding context to coordinate the
lane. A Worker receives a bounded task, relevant files, explicit stop
conditions, and the expected output shape.

Downward context should answer:

- What is the assignment?
- What inputs are authoritative?
- What files or artifacts are in scope?
- What decisions are already made?
- What must trigger escalation?

It should not dump transcripts or unrelated repository history.

## Summaries Sharpen Upward

Outputs should become shorter, more evidentiary, and more decision-oriented as
they move upward. Workers report what changed, what evidence supports it, and
where they stopped. Leads combine Worker outputs into lane status, integration
notes, unresolved assumptions, and escalation requests. The Orchestrator
synthesizes lane outputs into completion status, readiness status, and operator
decisions.

Upward summaries should preserve traceability without carrying raw chatter.
Good summaries point to files, commands, prompts, blockers, warnings, and
decisions.

## Implementation Belongs Below The Orchestrator

Implementation should usually stay below the Orchestrator because the
Orchestrator's value is scope control and synthesis. If the same role both
plans the whole system and edits details directly, it is easier to miss scope
creep, bury assumptions, or let one local choice distort the overall plan.

The Orchestrator may make small bridge fixes when they are necessary to land a
prompt coherently, but routine implementation belongs to Leads and Workers.
That keeps broad judgment separate from detailed execution.

## Leads Own Lanes

A lane is a workstream with a coherent purpose, such as a documentation area, a
validation pass, an integration slice, or a repair effort. The Lead owns the
lane's decomposition, local conventions, Worker assignment, review, and upward
summary.

Lead ownership does not mean unilateral scope expansion. A Lead can refine how
the lane is executed, but scope changes that affect the active prompt,
cross-lane commitments, or operator expectations escalate upward.

## Workers Execute Bounded Tasks

Workers receive minimal necessary context and a narrow definition of done. They
should produce structured outputs: changed files, evidence, unresolved
questions, stop conditions reached, and any escalation trigger encountered.

Workers should not infer broad product direction, approve their own completion
for the lane, or promote memory. Their job is execution inside a boundary.

## Manual Operation With Subscription Tools

The hierarchy can be performed manually:

1. The operator opens an Orchestrator session to interpret the prompt, plan
   lanes, and identify required context.
2. The operator opens one or more Lead sessions with lane-specific context.
3. Each Lead session may open or simulate Worker sessions for bounded tasks.
4. Workers return structured summaries rather than transcripts.
5. Leads summarize lane status upward.
6. The Orchestrator performs completion audit, next-prompt preflight, and final
   synthesis for the operator.

No vendor-specific API, background runtime, or autonomous multi-agent system is
required. The durable source of truth remains repo files, validation evidence,
and git history.
