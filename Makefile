.PHONY: help doctor resume checkpoint promptset lint-prompts check-docs test trace dry-run registry memory-check experiment-check

PROMPT ?= PROMPT_26

help:
	@python3 scripts/ahl.py help

doctor:
	@python3 scripts/ahl.py doctor

resume:
	@python3 scripts/ahl.py resume

checkpoint:
	@python3 scripts/ahl.py checkpoint

promptset:
	@python3 scripts/ahl.py promptset

lint-prompts:
	@python3 scripts/ahl.py promptset lint

check-docs:
	@python3 scripts/ahl.py docs check

test:
	@python3 -m unittest tests/test_ahl.py

trace:
	@python3 scripts/ahl.py trace $(PROMPT)

dry-run:
	@python3 scripts/ahl.py dry-run check --all

registry:
	@python3 scripts/ahl.py registry check

memory-check:
	@python3 scripts/ahl.py memory check

experiment-check:
	@python3 scripts/ahl.py experiment check
