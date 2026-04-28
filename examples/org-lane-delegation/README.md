# Org Lane Delegation Example

This scenario shows the Orchestrator -> Lead -> Worker model from
`../../docs/roles/org-model.md` using compact contracts from
`../../templates/contracts/`.

The fictional work is a small documentation improvement: add missing examples
navigation to a docs index. The Orchestrator defines the lane, the Lead turns
that lane into a Worker task, the Worker returns a structured result, and the
Lead reviews the output before summarizing upward.

## Artifacts

- `artifacts/orchestrator-brief.md` - lane charter and boundaries.
- `artifacts/lead-task-contract.md` - lane-level assignment to the Lead.
- `artifacts/worker-task-contract.md` - bounded Worker task.
- `artifacts/worker-result-contract.md` - structured Worker result.
- `artifacts/lead-review.md` - Lead review and upward summary.

## What This Teaches

- Context narrows as it moves downward.
- Workers receive files, scope, stop conditions, and output shape.
- Results sharpen upward into evidence and decisions.
- The Lead reviews Worker output; the Worker does not approve lane completion.
- The Orchestrator receives a summary instead of raw transcripts.
