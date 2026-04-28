# Principles

These principles define how `agent-harness-lab` expects prompt-bounded assistant
work to behave.

## Session Boundaries Are A Feature

Fresh sessions reduce hidden context dependence. A session should have enough
local context to execute one bounded prompt, audit the result, and leave the
repo ready for the next session. The reset is part of the harness design, not a
failure to maintain continuity.

## The Human Operator Is Part Of The Harness

The operator frames work, chooses prompts, approves commits, judges tradeoffs,
and decides what becomes durable. The harness should make that control visible
instead of replacing it with hidden autonomous behavior.

## Prompt-Bounded Work Is The Unit Of Execution

One prompt should define the active work unit. A session may make small bridge
fixes when required for that prompt to land coherently, but it should not absorb
future prompts or quietly redesign the whole system.

## Use The Core Session Rhythm

Prompt-execution sessions follow this rhythm:

1. Execute the active prompt.
2. Audit required deliverables and validation evidence.
3. Preflight the next prompt for obvious readiness issues.
4. Bridge only real blockers or non-trivial warnings.
5. Reset so the next prompt can start in a fresh session.

This rhythm keeps completion and continuity inspectable.

## Completion And Readiness Are Different Checks

Completion asks whether the active prompt's deliverables exist and match the
prompt. Next-prompt readiness asks whether the repo can support the next prompt
without obvious missing navigation, terminology, or prerequisite artifacts.
Passing one check does not automatically pass the other.

## Use Adjacent-Prompt Awareness

A session should inspect the next prompt during closeout and use the current
prompt's neighbors only when the prompt or endcap asks for it. This is a middle
ground between tunnel vision and vague future planning.

## Repo Files And Git History Are Source Of Truth

Durable project state belongs in reviewed repo files and git history. Reports,
findings, manifests, and handoffs can support decisions, but they should remain
traceable to files and commits.

## Raw Agent Chatter Is Not Durable Memory

Conversation transcripts can contain useful clues, but they are unreviewed
runtime data. Durable memory requires promotion into explicit artifacts with a
clear purpose, owner, and review path.

## Automation Follows Human-Operable Routines

Scripts and tools should encode routines that already make sense when performed
manually. Automation should reduce repeat work or improve validation, not hide
the operating model.

## Structured Output Supports Future Automation

When scripts are added later for checks or reports, their output should use
stable field names and predictable status values where future automation may
consume them. Human-readable prose can accompany structured output, but it
should not be the only machine-facing contract.

## Derived Indexes Are Not Primary Truth

Graph, vector, or other index systems may help discovery if introduced later.
They should be rebuildable from repo files and other durable sources, not used
as primary truth stores.
