# Basic Fixture Agent Guide

This is a fake bootstrap file for portable operator tests.

## Startup

1. Read this file.
2. Read the selected `.prompts/PROMPT_XX.txt` file.
3. Treat `.context/` as small project context when present.

## Boundaries

- Do not call provider CLIs.
- Do not use network access.
- Do not commit unless the operator explicitly asks.
