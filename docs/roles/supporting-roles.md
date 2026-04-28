# Supporting Roles

Supporting roles name recurring responsibilities that can be played by the
Orchestrator, a Lead, a Worker, or the human operator. They are not separate
people by default. They clarify session behavior now and provide names for
future templates, routines, checks, and possible automation.

## Orchestration Roles

| Role | Purpose | Classification | Future Automation Candidate |
| --- | --- | --- | --- |
| Session Conductor | Keeps a session aligned to the active prompt rhythm. | Conceptual role with procedural duties. | Partial, through run checklists and closeout checks. |
| Prompt Runner | Executes one prompt-bounded work unit. | Procedural role. | Partial, through prompt execution routines. |
| Completion Auditor | Checks required deliverables against the prompt. | Procedural review role. | Strong candidate for checklist and report support. |
| Next-Prompt Readiness Checker | Inspects the next prompt for obvious blockers. | Procedural review role. | Strong candidate for structured readiness reports. |
| Handoff Composer | Creates bridge artifacts only when useful. | Procedural role. | Partial, through templates. |
| Commit Packager | Groups completed changes into reviewable commits when the operator asks. | Procedural role. | Partial, through commit summaries and status checks. |

These roles are conceptual when discussing responsibility, procedural when
running a session step, and automation candidates only after the manual routine
is stable.

## Cognitive Work Roles

| Role | Purpose | Classification | Future Automation Candidate |
| --- | --- | --- | --- |
| Planner | Turns intent into a bounded plan. | Conceptual cognitive role. | Partial, through planning prompts. |
| Implementer | Performs scoped edits or artifact creation. | Procedural execution role. | Limited; human review remains required. |
| Reviewer | Finds defects, omissions, and risks. | Conceptual and procedural review role. | Partial, through review checklists. |
| Validator | Runs or judges checks and evidence. | Procedural role. | Strong candidate for helper scripts where commands exist. |
| Refiner or Repair Agent | Fixes bounded gaps after review. | Procedural repair role. | Partial, through repair-session startup routines. |

Cognitive roles describe modes of thinking and work. They should not be
confused with skills; the same role may invoke many skills.

## Repo Intelligence Roles

| Role | Purpose | Classification | Future Automation Candidate |
| --- | --- | --- | --- |
| Repo Cartographer | Maps existing structure and navigation. | Conceptual analysis role. | Partial, through repository inventories. |
| Convention Keeper | Detects and preserves local style and patterns. | Conceptual review role. | Partial, through linting or documentation checks. |
| Dependency or Assumption Tracker | Tracks prerequisites, assumptions, and unresolved claims. | Conceptual and procedural role. | Partial, through manifests or reports. |
| Change Impact Estimator | Identifies blast radius and downstream effects. | Conceptual analysis role. | Limited; requires judgment. |

Repo intelligence roles improve traceability. They become automation
candidates only where durable files provide reliable inputs.

## Process And Meta Roles

| Role | Purpose | Classification | Future Automation Candidate |
| --- | --- | --- | --- |
| Workflow Critic | Challenges waste, ambiguity, and overbuilt process. | Conceptual role. | Limited; judgment-heavy. |
| Promptset Quality Inspector | Reviews prompt sequence health and readiness. | Procedural review role. | Partial, through promptset reports. |
| Session Economics Monitor | Watches context, cost, scope, and reset discipline. | Conceptual operating role. | Partial, through run metadata. |
| Recovery Planner | Defines how to resume after blockers or failed sessions. | Procedural planning role. | Partial, through recovery templates. |

Process roles protect the harness from becoming expensive, opaque, or too
automated before the manual workflow is clear.
