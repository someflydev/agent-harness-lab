# Lifecycle Snippets

Purpose: reusable copy/paste snippets for one prompt in a target project.

## Inputs

- Prompt id: `<PROMPT_ID>`
- Prompt path: `.prompts/<PROMPT_ID>.txt`
- Bootstrap doc: `<BOOTSTRAP_DOC>` or none
- Context mention: `<CONTEXT_MENTION>`

## Default Snippet Cluster

### Run

```text
<RUN_SNIPPET>
```

### Audit, Next Readiness, And Context Update

```text
<AUDIT_NEXT_READINESS_CONTEXT_UPDATE_SNIPPET>
```

The context-update sentence is a review checkpoint, not an instruction to edit
context files by default. If no durable workflow, architecture, command,
convention, or repo-navigation knowledge changed, the audit can say `no
context update needed`.

### Commit Plan

```text
<COMMIT_PLAN_SNIPPET>
```

### Make Commits

```text
Make the commits
```

### Commit Check

```text
<COMMIT_CHECK_SNIPPET>
```

## Optional Repair Snippet

Keep repair separate from the default reusable cluster. Use it only when an
audit or commit check finds a concrete issue.

```text
<REPAIR_SNIPPET>
```
