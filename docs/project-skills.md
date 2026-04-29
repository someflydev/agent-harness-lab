# Project Skills

Project skills are optional instruction packages for recurring
`agent-harness-lab` routines. They live in `.agents/skills/`, follow a simple
`SKILL.md` shape, and help assistants load focused procedure when a task calls
for it.

They exist because several harness routines are common enough to deserve
copyable, on-demand guidance: running one prompt, auditing completion, checking
next-prompt readiness, composing a justified handoff, reviewing memory
promotion, inspecting the promptset, planning role lanes, and evaluating
closeout trajectory.

## How Skills Differ

Skills are not roles. A role says who owns a responsibility, such as
Orchestrator, Lead, or Worker. A skill says what reusable capability is being
used, such as completion auditing or handoff composing.

Skills are not routines. A routine is the repo's durable procedural source in
`runbooks/` and `docs/routines/`. A skill packages enough instructions for an
assistant to perform that routine without loading every related document.

Skills are not templates. Templates in `prompt-templates/` and `templates/`
provide reusable shapes for prompts, reports, contracts, handoffs, and records.
A skill may point at a template, but it should not replace the source template.

Skills are not scripts. Scripts such as `scripts/ahl.py` perform explicit local
checks or scaffolding. Skills contain instructions only; they do not hide
automation or call providers.

## Tool Use

Different assistants may use these files differently:

- Codex-style tools may load a named skill by command or by reading the
  relevant `.agents/skills/<name>/SKILL.md` file.
- Pi-style tools may treat the skill directory as project context next to
  prompt templates and operator routines.
- Claude-style tools may use the files as Agent Skills-like packages when the
  local environment supports that convention.
- Gemini-style tools or simpler CLIs may read the files as ordinary markdown.

The files intentionally avoid vendor-specific commands. Do not claim every
assistant will discover them automatically.

## Optional Context

Skills remain optional helper context. Startup still begins with `AGENT.md`,
the active prompt, and the prompt's required docs. Load a skill only when its
description matches the current task. Do not preload the whole `.agents/skills/`
tree.

The durable source of truth remains the checked-in docs, runbooks, templates,
registries, scripts, and git history. Skill instructions should point to those
sources instead of duplicating them wholesale.

## Adding A Skill Safely

Add a skill only when a recurring assistant-executed routine needs focused
on-demand guidance and is not already covered by an existing skill.

1. Confirm the routine exists or is clearly described in docs, runbooks, or
   prompt templates.
2. Create `.agents/skills/<name>/SKILL.md` with frontmatter containing `name`
   and a specific `description`.
3. Include when to use it, required context, step-by-step behavior, expected
   output, stop conditions, safety notes, and references.
4. Keep the skill narrow. Do not create broad "do everything" skills.
5. Avoid executable code, provider-specific assumptions, and large context
   loading by default.
6. Update `.agents/skills/README.md`, `docs/project-skills.md`, and relevant
   registries only when the skill is a durable addition.
