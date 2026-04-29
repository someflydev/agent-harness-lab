# Sequential Prompt Run Expected Output

The dry-run checker should confirm that the sequential scenario manifest is
present, parses as JSON, includes all required structural fields, and points to
existing bootstrap, runbook, template, example, and expected-output artifacts.

Expected result:

- `status`: `pass`
- No problems for `sequential-prompt-run`
- No live assistant, provider, or terminal replay is invoked
