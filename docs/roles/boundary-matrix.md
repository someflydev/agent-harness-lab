# Boundary Matrix

This matrix defines default authority for the role model. The human operator
retains final authority over project direction, commits, destructive actions,
and durable promotion decisions.

## Decision Authority

| Boundary Question | Operator | Orchestrator | Lead | Worker |
| --- | --- | --- | --- | --- |
| Who can assign work? | Can choose prompts and start sessions. | Assigns lanes and Leads. | Assigns bounded Worker tasks inside a lane. | Cannot assign work except local subtasks within the task. |
| Who can change scope? | Can change any scope. | Can refine prompt execution scope within operator intent. | Can refine lane execution, not active-prompt scope. | Cannot change scope. |
| Who can approve memory promotion? | Final approval. | Recommends and routes promotion. | Proposes lane-local promotion candidates. | Cannot approve; may flag candidates. |
| Who can declare completion? | Can accept or reject final completion. | Declares prompt completion after audit. | Declares lane completion to Orchestrator. | Declares assigned task completion only. |
| Who can create handoff artifacts? | Can request or author any handoff. | Creates bridge handoffs when materially useful. | Creates lane handoff notes when needed. | Provides structured result notes; does not create broad handoffs. |
| Who can escalate blockers? | Receives escalations and decides. | Escalates to operator. | Escalates to Orchestrator. | Escalates to Lead. |
| Who should inspect the next prompt? | May inspect directly. | Owns next-prompt preflight at closeout. | May inspect only for lane impact when asked. | Should not inspect next prompt unless assigned. |
| Who should package a commit if the operator asks? | Approves commit intent. | Groups and summarizes completed changes. | May package lane-specific changes when assigned. | Provides file-level summary for packaging. |

## Default Output Boundaries

| Role | Normal Output | Should Avoid |
| --- | --- | --- |
| Orchestrator | Plans, assignments, cross-lane synthesis, completion audit, readiness report. | Routine implementation and unreviewed memory promotion. |
| Lead | Task briefs, reviewed lane outputs, lane summaries, escalation notes. | Overall completion claims and cross-lane scope changes. |
| Worker | Narrow edits, checks, result summaries, local escalation notes. | Broad architecture decisions and lane-level approvals. |

## Memory Promotion Boundary

| Stage | Responsible Role | Expected Evidence |
| --- | --- | --- |
| Candidate identified | Worker, Lead, or Orchestrator | Specific fact, source file, and reason it may be durable. |
| Candidate reviewed | Lead or Orchestrator | Fit with doctrine, scope, and artifact boundaries. |
| Promotion approved | Operator or explicit approved process | Durable repo artifact and traceable change. |
| Promotion recorded | Assigned implementing role | File path, summary, and validation evidence. |
