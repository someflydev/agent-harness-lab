# Reports

Reports are retrospective evidence about prompt runs, promptsets, routines, or
phases of work. They summarize what happened, what was checked, what remains
risky, and which decisions need operator review.

Reports are not automatically doctrine. They may support a finding or a memory
promotion later, but the promotion decision must be explicit.

## Report Types

- Session reports: compact summaries of one prompt-execution, repair, bridge,
  review, or authoring session.
- Promptset audit reports: cross-prompt reviews of coverage, ordering,
  readiness, gaps, or regression risk across a promptset.
- Routine evaluation reports: evidence about whether a runbook, routine,
  checklist, or helper script improves the workflow.
- Capstone or phase reports: higher-level summaries after a milestone,
  promptset phase, or significant lab pass.

## Usage

Use a report when evidence needs to outlive a final answer but is not stable
enough to become doctrine. Keep reports traceable to prompts, files, commands,
commits, templates, and validation output.

Reports should:

- state scope and date
- list evidence inspected
- separate observations from conclusions
- identify risks and follow-up
- name any finding or promotion candidates

Reports should not:

- store raw transcripts by default
- present unreviewed lessons as durable rules
- duplicate large command outputs
- become a metrics platform or database

## Templates

- `templates/session-report.md`
- `templates/promptset-audit-report.md`
- `templates/routine-evaluation-report.md`

