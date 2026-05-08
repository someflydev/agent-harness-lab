# Portable Invocation

`project locate` is the first portable command surface. It reports where AHL
home is and which target project root a later portable command would inspect.
It is read-only and does not run assistants, edit project files, install
dependencies, call networks, read secrets, or require provider authentication.

## From The AHL Repo

From the AHL checkout, run:

```sh
python3 scripts/ahl.py project locate --json
```

The command resolves AHL home from the script location by default and treats
the current working directory as the target project unless `--project` is
provided.

## From Another Repo

From an arbitrary project repo, call the script by absolute or relative path:

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py project locate --json
```

Use `--project` when the target project is not the current working directory:

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py project locate --project /path/to/project --json
```

No checked-in wrapper such as `bin/ahl` exists. Operators may create a local
shell alias or symlink outside the repo for convenience, but that setup is
operator-owned and not part of AHL's committed interface.

## AHL Home

By default, AHL home is derived from the location of `scripts/ahl.py`. This lets
the script find AHL-owned docs, templates, registries, schemas, fixtures, and
tests even when invoked from another repo.

`AHL_HOME` may override that location only when it points to a valid AHL
checkout. Invalid overrides are reported as command problems.

## Target Project Root

The target project starts from the current working directory or from
`--project <path>`. When the path is inside a git work tree and `git` is
available, the nearest containing git root is reported as the project root. If
there is no git work tree, the requested directory is used as the project root.

Missing `.prompts/` is reported as a warning and structured status, not as a
crash. Later portable commands can use this diagnostic to decide whether a
project is ready for prompt-driven workflows.

## Failure Reporting

`project locate --json` returns stable fields for `ok`, `ahl_home`, `project`,
`warnings`, and `problems`. It exits non-zero when AHL home or the requested
project path cannot be resolved. It exits zero for a valid project root even
when `.prompts/` is absent.

The command is intentionally local and cheap. It does not need network access,
provider credentials, subscription APIs, package installation, or expensive
analysis.
