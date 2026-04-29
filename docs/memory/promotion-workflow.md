# Promotion Workflow

Memory promotion turns a useful temporary observation into a reviewed durable
repo fact. The workflow is intentionally small: propose, gather evidence,
decide, update the right artifact, and prune stale queue items.

## Propose A Candidate

Use the helper command to create a queue file:

```sh
python3 scripts/ahl.py memory propose <slug>
```

Fill in the candidate fact, source evidence, proposed target artifact, proposed
memory plane, and review need. Keep the candidate compact. Do not paste raw
transcripts or broad session summaries.

## Gather Evidence

Evidence should be traceable enough for a fresh session to verify the claim
without replaying chat history. Good evidence includes repo paths, prompt ids,
commands, reports, findings, tests, or observed failures with bounded scope.

If the claim describes behavior, include validation performed. If the claim is
only an observation from one run, say that clearly and keep the proposed target
narrow.

## Accept Or Reject

Use a decision scaffold after review:

```sh
python3 scripts/ahl.py memory decision <candidate> --accepted
python3 scripts/ahl.py memory decision <candidate> --rejected
```

Accepted decisions belong in `memory/accepted/`. Rejected decisions belong in
`memory/rejected/`. A decision record should name the reviewer, rationale,
durable update made, validation performed, and cleanup needed.

The command scaffolds records only. It does not move facts into doctrine,
modify docs, or approve candidates automatically.

## Accepted Memory And Durable Artifacts

Accepted memory should land in the narrowest useful durable artifact. Findings
can support promotion, but a finding does not approve promotion by itself.
Docs, runbooks, templates, scripts, and tests remain the source of truth for
how the project works.

Use `memory/accepted/` to preserve the decision trail. Use the durable target
artifact to preserve the fact future sessions should rely on.

## Prune Stale Candidates

Review `memory/promotion-queue/` periodically. Reject candidates that are
unverified, superseded, too local, or no longer useful. Delete queue files only
after the decision trail or git history makes the disposition clear.

Run:

```sh
python3 scripts/ahl.py memory check
```

before closeout when memory files changed.
