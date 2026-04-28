# Glossary

Short, repo-specific definitions for `agent-harness-lab`.

- **harness** - The docs, prompts, routines, contracts, and small tools that
  shape assistant work into repeatable sessions.
- **human-assisted orchestration** - A workflow where the human operator frames,
  supervises, validates, and sequences assistant work.
- **operator** - The human who starts sessions, chooses prompts, reviews
  results, and decides what becomes durable.
- **orchestrator** - The coordinating role that sequences work, preserves
  boundaries, and keeps the repo ready for the next prompt.
- **lead** - A session role responsible for owning the active prompt's scope,
  integration, audit, and closeout.
- **worker** - A bounded execution role responsible for a specific assigned
  slice of work under the lead's coordination.
- **prompt-bounded work unit** - The scope of work defined by one prompt and its
  explicit deliverables.
- **prompt-authoring session** - A session that creates or refines prompts,
  promptsets, or planning material without executing implementation work unless
  asked.
- **prompt-execution session** - A session that runs exactly one active prompt,
  validates it, preflights the next prompt, and resets.
- **repair session** - A targeted session that fixes blockers or fills small
  gaps left by previous work.
- **bridge artifact** - A temporary handoff or note created only when it
  materially helps the next fresh session continue safely.
- **completion audit** - The check that required deliverables exist, satisfy the
  active prompt, and have appropriate validation evidence.
- **next-prompt preflight** - A closeout check for obvious blockers to the next
  prompt, such as missing navigation, terminology, or prerequisites.
- **memory plane** - The conceptual layer where retained knowledge is organized
  by durability and review status.
- **promotion** - The act of moving useful transient knowledge into a reviewed,
  durable repo artifact.
- **accepted work memory** - Durable knowledge accepted into repo files or git
  history after review.
- **transient run memory** - Temporary session context, notes, observations, or
  logs that have not been promoted.
- **run manifest** - A structured record of a session or command run, including
  inputs, outputs, status, and evidence links.
- **result contract** - The expected shape, fields, status values, and evidence
  for a command, routine, report, or assistant deliverable.
- **escalation contract** - The rule for when a session must ask the operator
  for approval, report a blocker, or change execution posture.
- **readiness report** - A concise statement of whether the repo is ready for a
  next action, with blockers, warnings, and evidence.
- **operator control surface** - The visible commands, files, prompts, and
  decisions through which the operator directs the harness.
- **derived metadata** - Metadata generated from durable sources that can be
  rebuilt and should not replace those sources.
- **traceability** - The ability to connect claims, reports, and decisions back
  to prompts, files, validation evidence, and commits.
