# Known Limitations

`agent-harness-lab` is intentionally human-assisted first. The operator chooses
the prompt, grants permissions, reviews changes, decides whether a bridge
handoff is justified, and controls commits.

## Runtime Limits

- No provider credential manager, model router, queue worker, server, TUI, or
  background scheduler is implemented.
- No live multi-agent daemon exists.
- Phase-two outer-loop helpers can plan batches, dry-run plans, collect gates,
  build prompt payloads and run ledgers, rehearse manual-driver runs, plan
  resumes, generate commit plans, and invoke supported local assistant CLIs
  only through explicit `outer run --execute` consent.
- Portable-operator helpers can locate a target project, report status,
  generate lifecycle snippets, advise on context-update candidates, dry-run a
  prompt range, inspect recent commits, and run an offline rehearsal. They do
  not run target-project prompts, invoke assistant CLIs, edit target files,
  schedule continuation, or commit.
- Live assistant CLI runs can consume quota and depend on local authentication
  outside AHL.
- Portable helpers require no provider secrets, network access, expensive
  APIs, or machine-readable subscription usage checks.
- Claude Code remains a manual or terminal workflow surface. AHL does not
  automate external Claude subscription APIs, browser sessions, cookies, or
  subscription quota checks.
- Pi support remains guarded by `manual-confirmation-required` unless the local
  command and output contract are verified.

## Validation Limits

- Helper scripts are structural checks, not semantic proof that a prompt was
  completed correctly.
- Outer-loop gate reports do not replace human completion audits.
- Dry-runs validate deterministic scenario fixtures; they do not replace real
  prompt execution or human closeout review.
- Portable run-range plans are dry-run/read-only by default and one prompt at
  a time. They do not prove that any prompt was implemented.
- `human-notes.md` is informational and never machine-authoritative; portable
  helpers do not edit it.
- Commit inspection never rewrites history automatically.
- Documentation link checks are local navigation checks, not external link
  audits or content-quality proofs.
- The doctor command performs conservative path and repo hygiene checks; it is
  not a full secret scanner or security product.

## Architecture Limits

- Graph and vector retrieval are future architecture only.
- Future architecture docs do not imply implemented runtime capability.
- Raw assistant transcripts are not durable repo memory. Durable memory must be
  promoted through reviewed artifacts.
- The outer loop is not a daemon, autonomous coding platform, transcript store,
  graph database, or vector retrieval system.
- The portable operator is not a daemon, scheduler, external provider
  integration, production orchestration platform, or autonomous coding-agent
  runtime.
