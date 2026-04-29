# Role Packs

Role packs are pasteable startup briefs for manual hierarchy experiments. They
sit beside `docs/roles/` but serve a different purpose: the role docs define
authority, while these packs tell a fresh assistant session what to load, what
to produce, and where to stop.

Use a role pack when the operator wants one session to behave as a specific
role in the Orchestrator -> Lead -> Worker model, or as a supporting review or
repair role. Keep the active assignment narrow and pass durable artifacts, not
raw transcript history.

## Packs

- `orchestrator.md` - plan lanes, assign Leads, synthesize completion.
- `lead.md` - own one lane, decompose Worker tasks, review lane output.
- `worker.md` - execute a bounded task with minimal context.
- `reviewer.md` - inspect a scoped result for findings and risks.
- `auditor.md` - check prompt deliverables and readiness evidence.
- `repair-agent.md` - resolve a bounded blocker from a handoff or review.

## Use Pattern

1. Choose one role pack for the fresh session.
2. Add the operator request, active prompt or lane brief, and only the listed
   startup context.
3. Provide concrete in-scope files, expected outputs, validation expectations,
   and stop conditions.
4. Require a short evidence-based summary when the role finishes.

Role packs do not spawn agents, grant autonomous authority, or replace the
operator. They are copyable instructions for manually simulated role
separation.

