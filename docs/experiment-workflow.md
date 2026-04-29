# Experiment Workflow

Experiments are bounded trials for harness behavior. They can produce reports,
findings, or promotion candidates, but they do not change doctrine or memory
without review.

## Start An Experiment

Use an experiment when a workflow question needs evidence before changing a
prompt, routine, template, or helper command.

```sh
python3 scripts/ahl.py experiment new <slug>
```

The scaffold writes to `experiments/active/<slug>/` by default and creates a
plan, log, and closeout file from `experiments/templates/`. The command refuses
to overwrite existing files unless `--force` is provided. It does not update
`experiments/catalog.md`; add or edit the catalog row manually when the
operator decides the experiment belongs there.

Before running, fill in the plan with the question, setup, controlled
variables, evidence plan, baseline, and stop condition. If those fields cannot
be filled, the work is probably a note or report rather than an experiment.

## Log Observations

Record observations in `experiment-log.md` while the trial is active. Keep the
log compact and traceable:

- Link prompts, docs, commands, reports, commits, or validation output.
- Separate what happened from what it might mean.
- Preserve controlled variables and deviations that affect interpretation.
- Avoid raw assistant transcripts unless the operator explicitly needs them.

Run a structural check when useful:

```sh
python3 scripts/ahl.py experiment check
python3 scripts/ahl.py experiment check --json
```

The check validates active experiment directories for required files and
filled fields. It is a lightweight guard, not an evidence judge.

## Close An Experiment

Close the trial in `experiment-closeout.md` when the stop condition is reached,
when evidence is enough for a decision, or when the setup is no longer useful.
Use one result: accepted, rejected, inconclusive, abandoned, or superseded.

The closeout should name the evidence inspected, limitations, follow-up
decision, cleanup, and any promotion recommendation. A recommendation is not
approval; it only says the lesson may deserve review elsewhere.

After closeout, update `experiments/catalog.md` manually with the status,
artifact links, and outcome.

## Observation To Finding

An observation can become a finding when it has traceable support and matters
beyond one unusual run. Good candidates include recurring patterns, repeated
failures, useful workflow improvements, or anti-patterns that should inform
future prompts.

```sh
python3 scripts/ahl.py finding new <slug>
```

The command writes to `findings/draft/<slug>/finding-record.md` by default and
refuses overwrite unless `--force` is provided. Draft findings still need
review, scope, counter-evidence or limitations, and a disposition before they
should influence durable workflow changes.

Do not promote a one-off observation into doctrine. Keep isolated notes local
to the experiment, or preserve them in a report when they are useful context
but not a reusable lesson.

## Findings And Future Prompts

A reviewed finding can feed prompt-authoring by giving prompt writers a
bounded lesson, supporting evidence, scope, and recommended action. Use the
finding to revise future prompt wording, add validation steps, adjust a
runbook, or propose a memory or doctrine promotion.

Prompt-authoring sessions should still make their own scoped change and
validation plan. Findings supply evidence; they do not authorize broad edits
or automatic promotion.

## Avoid Doctrine Drift

Experiments and findings are lab evidence. Treat them as inputs to operator
judgment, not as automatic policy. A lesson should become durable doctrine only
after review confirms that it recurs, has clear scope, and belongs in a stable
artifact.
