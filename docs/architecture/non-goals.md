# Non-Goals

These boundaries apply to the foundation phase and should remain visible when
future architecture is discussed.

## Foundation-Phase Non-Goals

- No provider abstraction in the foundation phase.
- No always-on multi-agent daemon.
- No full REPL or TUI clone.
- No MCP, plugin, or server infrastructure.
- No graph or vector database dependency.
- No raw transcript warehouse.
- No hidden autonomous system.

## Why These Boundaries Exist

The foundation phase is about making prompt-bounded human-assisted work
coherent, inspectable, and repeatable. Heavy runtime concerns would add
maintenance cost before the repo has enough evidence about which workflows
deserve automation.

Future prompts may revisit these boundaries with evidence, but they should not
treat architecture notes as permission to skip documented routines, templates,
validation, and human approval points.
