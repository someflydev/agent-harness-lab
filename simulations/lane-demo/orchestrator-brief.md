# Orchestrator Brief

## Intent

Demonstrate a manual lane for a fictional template documentation refresh. The
lane should prove that role-separated work can be coordinated through files and
validated locally before any runtime automation exists.

## Scope

- Inspect the fictional `templates/lane/` documentation surface.
- Ask one Lead to decompose the work into a single Worker assignment.
- Require durable role outputs and a final status JSON file.
- Validate structure with the local `lane check` command.

## Out Of Scope

- Building or changing a real application.
- Spawning sub-agents or invoking model providers.
- Running concurrent processes.
- Changing production template behavior.

## Stop And Escalate

Stop if a required lane artifact is missing, the status JSON cannot be parsed,
the Worker finds that the task requires real implementation work, or the
Reviewer reports a blocking finding.

