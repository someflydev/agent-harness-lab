# Role Skill Map

Roles own responsibility. Skills provide capabilities that roles invoke. The
same skill can be used by multiple roles with different authority boundaries.

## Core Roles

| Role | Common Skill Areas | Typical Use | Boundary |
| --- | --- | --- | --- |
| Operator | Scope boundary detection, prompt quality critique, rate-limit-aware chunking, commit summarization. | Choose prompts, approve direction, decide commits, and keep subscription-friendly workflow practical. | Final authority over direction, commits, destructive actions, and durable promotion. |
| Orchestrator | Requirement extraction, deliverable enumeration, scope boundary detection, lane planning, readiness judgment, escalation handling, synthesis, completion audit, next-prompt preflight. | Interpret the active prompt, define lanes, audit completion, and decide whether a bridge is needed. | Can refine execution scope within operator intent, but cannot silently expand the prompt. |
| Lead | Decomposition, assumption tracking, convention detection, multi-file consistency editing, Worker review, lane-local memory management, validation judgment. | Turn a lane into bounded Worker assignments and integrate reviewed outputs. | Owns lane decisions, not whole-prompt completion or cross-lane scope changes. |
| Worker | Focused file editing, scaffold generation, patch repair, artifact verification, test command discovery, structured result reporting. | Execute a narrow assignment with minimal necessary context. | Stops at assignment boundary and escalates unclear or broader decisions. |

## Supporting Roles

| Supporting Role | Useful Skills | Expected Output |
| --- | --- | --- |
| Prompt Runner | Requirement extraction, deliverable enumeration, focused execution, prompt-vs-implementation cross-checking. | Completed prompt-bounded work unit with evidence. |
| Completion Auditor | Deliverable enumeration, artifact verification, prompt-vs-implementation cross-checking, smoke-test judgment. | Completion audit with gaps, evidence, and residual risk. |
| Next-Prompt Readiness Checker | Structural mapping, assumption diffing, next-prompt preflight, scope boundary detection. | Ready, risky, or blocked statement for the next prompt. |
| Handoff Composer | Handoff writing, recovery planning, assumption diffing. | Temporary bridge artifact only when materially useful. |
| Commit Packager | Commit summarization, artifact verification, scope boundary detection. | Reviewable commit grouping and summary when the operator asks. |
| Repo Cartographer | Structural mapping, convention detection, artifact verification. | Repo navigation and affected-area notes. |
| Convention Keeper | Convention detection, multi-file consistency editing, prompt-vs-implementation cross-checking. | Consistent style, terminology, and references. |
| Workflow Critic | Prompt quality critique, session waste detection, scope boundary detection. | Warnings about ambiguity, overreach, or inefficient session shape. |
| Recovery Planner | Recovery planning, assumption diffing, repair-session startup, validation path discovery. | Narrow repair scope with stop conditions. |

## Mapping Guidance

Use the smallest role that has enough authority for the skill. A Worker can
verify an artifact, but should not declare prompt completion. A Lead can manage
lane-local assumptions, but should escalate assumptions that change cross-lane
direction. The Orchestrator can synthesize and preflight, but should still keep
operator-controlled decisions visible.
