# Review Severity

Severity describes user impact and closeout risk. It is not a measure of how
large a patch is.

## Levels

- Critical: completion is false, data may be lost, destructive commands were
  used incorrectly, or the repo cannot safely proceed.
- High: a required deliverable or validation step is missing, script behavior
  is broken, or the next prompt is blocked.
- Medium: a required detail is weak or ambiguous, docs overstate behavior, or
  evidence is incomplete but recoverable in scope.
- Low: wording, navigation, or consistency issues that do not change the
  result.
- Informational: observations that may help later work but do not require a
  fix now.

## Disposition

Findings should name the file or command, explain the risk, and recommend one
concrete next action. High and Critical findings should be fixed or explicitly
classified as blocked before closeout.
