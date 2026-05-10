.PHONY: help doctor resume checkpoint promptset lint-prompts check-docs test domain-pack trace dry-run portable-rehearsal lane-check registry driver outer-plan project-status lifecycle-snippets lifecycle-context-check lifecycle-run-range portable-fixtures outer-dry-run outer-gate outer-run outer-resume memory-check experiment-check

PROMPT ?= PROMPT_26
PORTABLE_PROMPT ?= PROMPT_45
PROJECT ?= .
RANGE_START ?= 18
RANGE_END ?= 27
OUTER_FROM ?= PROMPT_33
OUTER_COUNT ?= 3
DRIVER ?= manual
PLAN ?=
RUN ?=

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

domain-pack:
	@python3 scripts/ahl.py domain-pack check

trace:
	@python3 scripts/ahl.py trace $(PROMPT)

dry-run:
	@python3 scripts/ahl.py dry-run check --all

portable-rehearsal:
	@python3 scripts/ahl.py portable rehearsal

lane-check:
	@python3 scripts/ahl.py lane check simulations/lane-demo

registry:
	@python3 scripts/ahl.py registry check

driver:
	@python3 scripts/ahl.py driver check

outer-plan:
	@python3 scripts/ahl.py outer plan --from $(OUTER_FROM) --count $(OUTER_COUNT) --driver $(DRIVER)

project-status:
	@python3 scripts/ahl.py project status --project $(PROJECT) --json

lifecycle-snippets:
	@python3 scripts/ahl.py lifecycle snippets $(PORTABLE_PROMPT) --project $(PROJECT) --json

lifecycle-context-check:
	@python3 scripts/ahl.py lifecycle context-check $(PORTABLE_PROMPT) --project $(PROJECT) --json

lifecycle-run-range:
	@python3 scripts/ahl.py lifecycle run-range $(RANGE_START) $(RANGE_END) --project $(PROJECT) --dry-run --json

portable-fixtures:
	@python3 scripts/ahl.py project status --project fixtures/portable-operator/projects/basic --json

outer-dry-run:
	@if [ -z "$(PLAN)" ]; then printf '%s\n' 'PLAN=runs/outer-loop/<plan-id>/plan.json is required'; exit 2; fi
	@python3 scripts/ahl.py outer dry-run --plan $(PLAN)

outer-gate:
	@if [ -n "$(PLAN)" ]; then python3 scripts/ahl.py outer gate $(PROMPT) --plan $(PLAN) --json; else python3 scripts/ahl.py outer gate $(PROMPT) --json; fi

outer-run:
	@if [ -z "$(PLAN)" ]; then printf '%s\n' 'PLAN=runs/outer-loop/<plan-id>/plan.json is required'; exit 2; fi
	@python3 scripts/ahl.py outer run --plan $(PLAN) --dry-run

outer-resume:
	@if [ -z "$(RUN)" ]; then printf '%s\n' 'RUN=runs/outer-loop/<run-id>/run-ledger.json is required'; exit 2; fi
	@python3 scripts/ahl.py outer resume --run $(RUN) --dry-run

memory-check:
	@python3 scripts/ahl.py memory check

experiment-check:
	@python3 scripts/ahl.py experiment check
