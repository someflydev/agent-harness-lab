# Portable Operator Known Limitations

The portable operator baseline is local helper tooling for a human-governed
one-prompt workflow. These limits are part of the supported behavior.

## Execution Limits

- Portable helpers do not run assistant CLIs, call model providers, schedule
  prompt ranges, or continue across prompt boundaries.
- No background daemon, queue, server, provider credential manager, browser
  automation, or hidden state store exists.
- No provider secrets, network access, expensive APIs, or machine-readable
  subscription usage checks are required.
- Claude Code is supported only as a manual or terminal workflow surface. AHL
  does not automate external Claude subscription APIs, browser sessions,
  cookies, or subscription quota checks.
- Codex, Gemini, and generic chat surfaces remain operator-run unless a
  separate reviewed integration explicitly says otherwise.

## Validation Limits

- `project status` and promptset diagnostics are structural. They do not prove
  prompt quality or semantic implementation completion.
- `lifecycle snippets` prints reusable instruction text. It cannot prove that
  an assistant followed the text.
- `lifecycle context-check` is advisory and read-only. It suggests review
  questions from changed paths but does not decide that context must be
  updated.
- `portable rehearsal` proves deterministic helper composition against
  fixtures. It does not run real prompts or validate a real target project.

## Data And Git Limits

- `human-notes.md` is informational and operator-owned. AHL may report that it
  exists, but it never treats the file as machine-authoritative and does not
  edit it.
- `commit check` reads git history and changed-file lists only. It never
  stages files, commits, amends, rebases, resets, pushes, tags, publishes, or
  rewrites history automatically.
- Commit grouping remains a human review decision. The helper can report
  evidence and warnings, not final semantic correctness.

## Run-Range Limits

- `lifecycle run-range` is dry-run/read-only by default and one prompt at a
  time by design.
- It does not invoke assistants, run validation commands, edit target-project
  files, edit `human-notes.md`, stage, commit, or schedule continuation.
- It writes a JSON artifact only when `--artifact` is explicit and refuses to
  overwrite existing artifacts unless `--force` is explicit.

## Architecture Limits

- Portable operator is not a production orchestration platform, autonomous
  coding-agent runtime, transcript store, model router, graph database, vector
  retrieval system, or provider billing monitor.
- Outer-loop live execution remains separate from the portable helper
  boundary and requires explicit `outer run --execute` consent for supported
  local driver contracts.
