# Reference Repo Boundaries

Local clones of `agent-context-base`, `pi-mono`, and `claw-code` are reference
material only. They are not implementation targets for `agent-harness-lab`.

Use them to compare ideas such as startup discipline, prompt templates,
doctor-style checks, permission posture, and recoverable workflows. Do not copy
their implementation, vendor assumptions, identity, or repo-specific runtime
contracts into this project without a prompt that explicitly justifies the
adaptation.

Reference repos should be ignored when they sit inside this working tree. A
normal prompt-execution session may inspect them only when the active prompt
asks for reference influence or when a narrow comparison is necessary.

Do not:

- edit reference repos while implementing this repo
- commit reference repo files here
- treat future architecture notes as implemented runtime capabilities
- let reference project terminology override this repo's documented boundaries
