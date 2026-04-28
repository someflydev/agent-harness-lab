# Design Filters

Use these questions before adding new docs, scripts, metadata, automation, or
infrastructure.

## Fit To The Harness

- Does this improve fresh-session execution, endcap quality, validation, or
  operator control?
- Is the artifact tied to a real prompt, routine, report, or decision?
- Can a fresh assistant understand it without hidden context?
- Does it preserve prompt-bounded work instead of expanding the active scope?
- Does it keep repo files and git history as the source of truth?

## Human Operability

- Can the useful part start as a markdown routine, checklist, template, or tiny
  script?
- Can the operator inspect, override, or skip it?
- Does it work without paid API orchestration or provider-specific runtime
  assumptions?
- Does it reduce repeated human effort without hiding important decisions?
- Does it have an obvious place in the repo?

## Automation Readiness

- Has the manual routine been proven enough to automate?
- What stable inputs, outputs, status values, and evidence should the result
  contract include?
- Can failures produce clear problems instead of prose-only ambiguity?
- Is generated metadata rebuildable from durable sources?
- Is the maintenance cost proportional to the value?

## Memory Discipline

- Is this accepted work memory or transient run memory?
- What review step promotes it into durable memory?
- What source file, prompt, command, or commit supports the claim?
- Could this become metadata hoarding?
- Would a future graph or vector index be derived from this, rather than
  replacing it?

## Compatibility Filter For `claw-code` Ideas

- Can the useful part start as a markdown routine, checklist, template, or tiny
  script?
- Does it improve fresh-session execution or endcap quality?
- Does it work without paid API orchestration?
- Is the operator still able to inspect and override it?
- Does it preserve repo files and git history as source of truth?
