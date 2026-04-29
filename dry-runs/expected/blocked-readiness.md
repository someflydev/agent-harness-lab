# Blocked Readiness Expected Output

The dry-run checker should confirm that the blocked-readiness scenario manifest
is present, parses as JSON, includes all required structural fields, and points
to existing readiness runbook, runtime guidance, fixture, template, and
expected-output artifacts.

Expected result:

- `status`: `pass`
- No problems for `blocked-readiness`
- The scenario remains a structural readiness check, not a future-prompt repair
