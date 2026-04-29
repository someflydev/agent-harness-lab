#!/usr/bin/env python3
"""Small helper CLI for agent-harness-lab."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit


PROMPT_RE = re.compile(r"^PROMPT_(\d+)\.txt$")
STRICT_PROMPT_RE = re.compile(r"^PROMPT_(\d{2})\.txt$")
NEXT_MARKER_RE = re.compile(r"^\s*(?:[-*]\s*)?(?:Next|Next step|## Next)\b", re.I)
PROMPT_HEADING_RE = re.compile(r"^\s*#\s+PROMPT_\d{2}\b", re.M)
CONTEXT_FILES = ("TASK.md", "SESSION.md", "MEMORY.md")
REFERENCE_DIRS = ("agent-context-base", "pi-mono", "claw-code")
REQUIRED_TOP_LEVEL_DIRS = ("docs", "runbooks", "templates", "scripts", "tests", ".prompts")
REQUIRED_DOC_DIRS = ("contracts", "doctrine", "memory", "quality", "roles", "routines", "runtime", "skills")
REQUIRED_REGISTRY_FILES = (
    "artifacts.json",
    "prompts.json",
    "roles.json",
    "routines.json",
    "templates.json",
    "examples.json",
    "scripts.json",
)
REQUIRED_REGISTRY_FIELDS = ("id", "name", "type", "path", "purpose", "status", "related_docs", "safe_use_notes")
DOCS_SCAN_ROOTS = (
    "README.md",
    "AGENT.md",
    "dry-runs",
    "docs",
    "runbooks",
    "templates",
    "scripts",
    "registry",
    "examples",
    "experiments",
    "findings",
    "reports",
    "role-packs",
    "lane-playbooks",
    "prompt-templates",
    "memory",
)
DOCS_NAV_INDEX = "docs/README.md"
DOCS_INDEX_DIRS = (
    "dry-runs",
    "runbooks",
    "templates",
    "scripts",
    "registry",
    "examples",
    "experiments",
    "findings",
    "reports",
    "role-packs",
    "lane-playbooks",
    "prompt-templates",
    "fixtures",
    "memory",
)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]\n]+\]:\s*(\S+)", re.M)
PROMPT_ID_RE = re.compile(r"^PROMPT_\d{2}$")
PROMPT_ID_FIELDS = {"prompt_id", "active_prompt", "next_prompt"}
PROMPT_LINT_SECTIONS = (
    ("startup_instructions", "startup instructions", ("startup instructions", "startup")),
    ("required_deliverables", "required deliverables", ("required deliverables", "deliverables")),
    ("constraints", "constraints", ("constraints",)),
    ("validation", "validation", ("validation",)),
    ("endcap", "endcap", ("endcap",)),
)
FIXTURE_SPECS: dict[str, dict[str, Any]] = {
    "fixtures/run-records/success.json": {
        "schema": "schemas/run-record.schema.json",
        "required": ("prompt_id", "run_id", "assistant_tool", "validation_commands", "completion_audit_status"),
    },
    "fixtures/run-records/blocked.json": {
        "schema": "schemas/run-record.schema.json",
        "required": ("prompt_id", "run_id", "assistant_tool", "validation_commands", "completion_audit_status"),
    },
    "fixtures/readiness-reports/ready.json": {
        "schema": "schemas/readiness-report.schema.json",
        "required": ("artifact_id", "active_prompt", "next_prompt", "readiness_label", "blockers", "next_step"),
    },
    "fixtures/readiness-reports/blocked.json": {
        "schema": "schemas/readiness-report.schema.json",
        "required": ("artifact_id", "active_prompt", "next_prompt", "readiness_label", "blockers", "next_step"),
    },
    "fixtures/promptset-index/valid.json": {
        "schema": "schemas/promptset-index.schema.json",
        "required": ("ok", "prompt_dir", "prompts", "filenames", "numbers", "duplicates", "gaps"),
    },
    "fixtures/lane-records/single-lane.json": {
        "schema": "schemas/lane-record.schema.json",
        "required": ("lane_id", "prompt_id", "owner_role", "scope", "status", "inputs", "outputs"),
    },
    "fixtures/traceability/prompt-to-commit.json": {
        "schema": "schemas/traceability-record.schema.json",
        "required": ("traceability_id", "prompt_id", "source_artifact", "commit_links", "validation_evidence"),
    },
    "fixtures/traceability/working-tree-summary.json": {
        "schema": None,
        "required": ("prompt_id", "prompt_file_exists", "branch", "head", "changed_files", "docs_changed"),
    },
}
DRY_RUN_REQUIRED_FIELDS = (
    "id",
    "purpose",
    "input_artifacts",
    "routine_sequence",
    "expected_checks",
    "expected_outputs",
    "failure_modes_covered",
)
DRY_RUN_LIST_FIELDS = (
    "input_artifacts",
    "routine_sequence",
    "expected_checks",
    "expected_outputs",
    "failure_modes_covered",
)
LANE_REQUIRED_FILES = (
    "README.md",
    "orchestrator-brief.md",
    "lead-plan.md",
    "worker-01-task.md",
    "worker-01-result.md",
    "reviewer-report.md",
    "auditor-closeout.md",
    "lane-status.json",
)
LANE_STATUS_REQUIRED_FIELDS = (
    "lane_id",
    "simulation",
    "state",
    "roles",
    "artifacts",
    "current_step",
    "stop_escalation",
)
LANE_STATES = ("pending", "active", "review", "audited", "blocked", "escalated", "done")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
EXPERIMENT_TEMPLATE_FILES = (
    ("experiments/templates/experiment-plan.md", "experiment-plan.md"),
    ("experiments/templates/experiment-log.md", "experiment-log.md"),
    ("experiments/templates/experiment-closeout.md", "experiment-closeout.md"),
)
EXPERIMENT_REQUIRED_FILES = ("experiment-plan.md", "experiment-log.md")
EXPERIMENT_REQUIRED_FIELDS = {
    "experiment-plan.md": (
        "- Experiment id:",
        "- Date opened:",
        "- Status:",
        "- Hypothesis or question:",
        "- Workflow problem:",
        "- Stop condition:",
    ),
    "experiment-log.md": (
        "- Experiment id:",
        "- Log date:",
        "- What happened:",
        "- Validation result:",
        "- Current read:",
    ),
}
FINDING_TEMPLATE_FILES = (("findings/templates/finding-record.md", "finding-record.md"),)
MEMORY_CANDIDATE_TEMPLATE = "templates/memory/promotion-candidate.md"
MEMORY_DECISION_TEMPLATE = "templates/memory/promotion-decision.md"
MEMORY_CANDIDATE_REQUIRED_FIELDS = (
    "- Candidate id:",
    "- Date proposed:",
    "- Proposed by:",
    "- Status:",
    "- Candidate fact:",
    "- Source evidence:",
    "- Proposed target artifact:",
    "- Proposed memory plane:",
    "- Review needed:",
)
MEMORY_CANDIDATE_REQUIRED_HEADINGS = (
    "# Promotion Candidate",
    "## Candidate",
    "## Evidence",
    "## Review Notes",
    "## Disposition",
)
COMMAND_HELP: tuple[dict[str, str], ...] = (
    {
        "name": "help",
        "command": "python3 scripts/ahl.py help",
        "summary": "List common operator console commands.",
        "safety": "read-only",
    },
    {
        "name": "doctor",
        "command": "python3 scripts/ahl.py doctor",
        "summary": "Check expected repo foundations.",
        "safety": "read-only",
    },
    {
        "name": "resume",
        "command": "python3 scripts/ahl.py resume",
        "summary": "Print a grounded session context briefing.",
        "safety": "read-only",
    },
    {
        "name": "checkpoint",
        "command": "python3 scripts/ahl.py checkpoint",
        "summary": "Scaffold missing context notes.",
        "safety": "writes context/*.md when missing",
    },
    {
        "name": "promptset",
        "command": "python3 scripts/ahl.py promptset",
        "summary": "Inspect prompt numbering.",
        "safety": "read-only",
    },
    {
        "name": "lint-prompts",
        "command": "python3 scripts/ahl.py promptset lint",
        "summary": "Check prompt structure and registry alignment.",
        "safety": "read-only",
    },
    {
        "name": "check-docs",
        "command": "python3 scripts/ahl.py docs check",
        "summary": "Check local docs links, navigation, and registry paths.",
        "safety": "read-only",
    },
    {
        "name": "test",
        "command": "python3 -m unittest tests/test_ahl.py",
        "summary": "Run helper CLI unit tests.",
        "safety": "read-only",
    },
    {
        "name": "trace",
        "command": "python3 scripts/ahl.py trace PROMPT_26",
        "summary": "Summarize prompt-related working tree traceability.",
        "safety": "read-only",
    },
    {
        "name": "dry-run",
        "command": "python3 scripts/ahl.py dry-run check --all",
        "summary": "Validate deterministic dry-run scenarios.",
        "safety": "read-only",
    },
    {
        "name": "lane-check",
        "command": "python3 scripts/ahl.py lane check simulations/lane-demo",
        "summary": "Validate a manual lane simulation workspace.",
        "safety": "read-only",
    },
    {
        "name": "registry",
        "command": "python3 scripts/ahl.py registry check",
        "summary": "Validate curated registry indexes.",
        "safety": "read-only",
    },
    {
        "name": "memory-check",
        "command": "python3 scripts/ahl.py memory check",
        "summary": "Check reviewed memory promotion candidates.",
        "safety": "read-only",
    },
    {
        "name": "experiment-check",
        "command": "python3 scripts/ahl.py experiment check",
        "summary": "Check active experiment records.",
        "safety": "read-only",
    },
)


def repo_root() -> Path:
    return Path.cwd()


def read_gitignore(root: Path) -> set[str]:
    path = root / ".gitignore"
    if not path.exists():
        return set()
    ignored: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            ignored.add(stripped.rstrip("/"))
    return ignored


def line_count(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8").splitlines())
    except UnicodeDecodeError:
        return 0


def git_value(args: list[str], default: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root(),
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return default
    return result.stdout.strip() or default


def git_changed_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=repo_root(),
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def run_git(root: Path, args: list[str]) -> tuple[subprocess.CompletedProcess[str] | None, str | None]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        return None, f"git unavailable: {exc}"
    return result, None


def changed_paths_from_status(lines: list[str]) -> list[str]:
    paths: list[str] = []
    for line in lines:
        path = line[3:] if len(line) > 3 else line.strip()
        if " -> " in path:
            paths.extend(part.strip() for part in path.split(" -> ") if part.strip())
        elif path.strip():
            paths.append(path.strip())
    return paths


def changed_directories(paths: list[str]) -> list[str]:
    directories: set[str] = set()
    for path in paths:
        if "/" in path:
            directories.add(path.split("/", 1)[0])
        elif path:
            directories.add(".")
    return sorted(directories)


def trace_data(root: Path, prompt_id: str) -> dict[str, Any]:
    prompt_path = root / ".prompts" / f"{prompt_id}.txt"
    git_problems: list[str] = []
    branch: str | None = None
    head: str | None = None
    status_lines: list[str] = []
    inside_work_tree = False

    rev_parse, problem = run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if problem:
        git_problems.append(problem)
    elif rev_parse is None or rev_parse.returncode != 0 or rev_parse.stdout.strip() != "true":
        git_problems.append("not inside a git working tree")
    else:
        inside_work_tree = True
        branch_result, branch_problem = run_git(root, ["branch", "--show-current"])
        if branch_problem:
            git_problems.append(branch_problem)
        elif branch_result is not None and branch_result.returncode == 0:
            branch = branch_result.stdout.strip() or None
        else:
            git_problems.append("could not read current git branch")

        head_result, head_problem = run_git(root, ["rev-parse", "--short", "HEAD"])
        if head_problem:
            git_problems.append(head_problem)
        elif head_result is not None and head_result.returncode == 0:
            head = head_result.stdout.strip() or None
        else:
            git_problems.append("could not read current HEAD commit")

        status_result, status_problem = run_git(root, ["status", "--short", "--untracked-files=all"])
        if status_problem:
            git_problems.append(status_problem)
        elif status_result is not None and status_result.returncode == 0:
            status_lines = [line for line in status_result.stdout.splitlines() if line.strip()]
        else:
            git_problems.append("could not read git status")

    paths = changed_paths_from_status(status_lines)
    docs_changed = any(path == "docs" or path.startswith("docs/") for path in paths)
    tests_changed = any(path == "tests" or path.startswith("tests/") for path in paths)
    templates_changed = any(path == "templates" or path.startswith("templates/") for path in paths)
    suggested_missing = [
        "assistant_tool",
        "model",
        "reasoning_or_thinking_setting",
        "permission_posture",
        "invocation_command",
        "started_at",
        "ended_at",
        "validation_commands",
        "completion_audit_status",
        "next_prompt_ready",
        "readiness_blockers",
        "associated_commit_hashes",
    ]

    return {
        "prompt_id": prompt_id,
        "prompt_file": str(prompt_path.relative_to(root)),
        "prompt_file_exists": prompt_path.is_file(),
        "branch": branch,
        "head": head,
        "git": {
            "available": not any(item.startswith("git unavailable:") for item in git_problems),
            "inside_work_tree": inside_work_tree,
            "degraded": bool(git_problems),
            "problems": git_problems,
        },
        "changed_files": status_lines,
        "changed_paths": paths,
        "changed_directories": changed_directories(paths),
        "docs_changed": docs_changed,
        "tests_changed": tests_changed,
        "templates_changed": templates_changed,
        "handoff_exists": (root / "tmp" / "HANDOFF.md").is_file(),
        "suggested_run_record_missing_fields": suggested_missing,
        "run_record_skeleton": {
            "prompt_id": prompt_id,
            "prompt_batch_id": "promptset",
            "run_id": f"{prompt_id}-YYYYMMDD-HHMMSS",
            "assistant_tool": None,
            "permission_posture": None,
            "started_at": None,
            "ended_at": None,
            "changed_files": status_lines,
            "changed_directories": changed_directories(paths),
            "docs_changed": docs_changed,
            "tests_changed": tests_changed,
            "validation_commands": [],
            "completion_audit_status": None,
            "next_prompt_ready": None,
            "readiness_blockers": [],
            "handoff_created": (root / "tmp" / "HANDOFF.md").is_file(),
            "follow_up_fix_required": None,
            "reusable_pattern_observations": [],
            "associated_commit_hashes": [],
        },
    }


def command_trace(args: argparse.Namespace) -> int:
    root = repo_root()
    prompt_id = normalize_prompt_id(args.prompt)
    data = trace_data(root, prompt_id)
    human = [
        f"trace: {prompt_id}",
        f"- Prompt file: {'present' if data['prompt_file_exists'] else 'missing'} ({data['prompt_file']})",
        f"- Branch: {data['branch'] or 'unknown'}",
        f"- HEAD: {data['head'] or 'unknown'}",
        f"- Changed files: {len(data['changed_files'])}",
        f"- Docs changed: {data['docs_changed']}",
        f"- Tests changed: {data['tests_changed']}",
        f"- Templates changed: {data['templates_changed']}",
        f"- Handoff exists: {data['handoff_exists']}",
    ]
    if data["git"]["degraded"]:
        human.append("- Git state: degraded (" + "; ".join(data["git"]["problems"]) + ")")
    if not data["prompt_file_exists"]:
        human.append("- Warning: matching prompt file is missing")
    return emit(data, args.json, human, 0)


def emit(data: dict[str, Any], as_json: bool, human_lines: list[str], code: int = 0) -> int:
    if as_json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print("\n".join(human_lines))
    return code


def command_doctor(args: argparse.Namespace) -> int:
    root = repo_root()
    ignored = read_gitignore(root)
    checks: list[dict[str, Any]] = []
    problems: list[str] = []

    def check(name: str, path: Path, required: bool = True, kind: str | None = None) -> None:
        exists = path.exists()
        if kind == "dir":
            ok = path.is_dir()
        elif kind == "file":
            ok = path.is_file()
        else:
            ok = exists
        status = ok if required else True
        checks.append({"name": name, "path": str(path.relative_to(root)), "required": required, "ok": status})
        if required and not ok:
            problems.append(f"missing {name}: {path.relative_to(root)}")

    check("README.md", root / "README.md", kind="file")
    check("AGENT.md", root / "AGENT.md", kind="file")
    check(".prompts", root / ".prompts", kind="dir")
    check("docs", root / "docs", kind="dir")
    check("runbooks", root / "runbooks", kind="dir")
    check("templates", root / "templates", kind="dir")

    tmp_ignored = "tmp" in ignored
    checks.append({"name": "tmp ignored", "path": ".gitignore", "required": True, "ok": tmp_ignored})
    if not tmp_ignored:
        problems.append("tmp/ is not ignored by .gitignore")

    for dirname in REFERENCE_DIRS:
        present = (root / dirname).exists()
        ignored_ok = dirname in ignored
        checks.append(
            {
                "name": f"{dirname} ignored if present",
                "path": dirname,
                "required": False,
                "present": present,
                "ok": (not present) or ignored_ok,
            }
        )
        if present and not ignored_ok:
            problems.append(f"{dirname}/ exists but is not ignored by .gitignore")

    ok = not problems
    data = {"ok": ok, "checks": checks, "problems": problems}
    human = ["doctor: ok" if ok else "doctor: problems found"]
    human.extend(f"- {problem}" for problem in problems)
    return emit(data, args.json, human, 0 if ok else 1)


def promptset_data(root: Path) -> dict[str, Any]:
    return promptset_numbering_data(root, root / ".prompts")


def promptset_numbering_data(root: Path, prompt_dir: Path) -> dict[str, Any]:
    files = sorted(prompt_dir.glob("PROMPT_*.txt")) if prompt_dir.is_dir() else []
    prompts: list[dict[str, Any]] = []
    numbers: list[int] = []
    malformed: list[str] = []
    for path in files:
        name = path.name
        match = PROMPT_RE.match(name)
        strict = bool(STRICT_PROMPT_RE.match(name))
        number = int(match.group(1)) if match else None
        if number is not None:
            numbers.append(number)
        if not strict:
            malformed.append(name)
        prompts.append({"filename": name, "number": number, "strict": strict})

    counts: dict[int, int] = {}
    for number in numbers:
        counts[number] = counts.get(number, 0) + 1
    duplicates = sorted(number for number, count in counts.items() if count > 1)
    unique_numbers = sorted(counts)
    gaps: list[int] = []
    if unique_numbers:
        expected = range(unique_numbers[0], unique_numbers[-1] + 1)
        gaps = [number for number in expected if number not in counts]

    return {
        "ok": bool(prompt_dir.is_dir()) and not duplicates and not gaps and not malformed,
        "prompt_dir": str(prompt_dir.relative_to(root)) if prompt_dir.is_relative_to(root) else str(prompt_dir),
        "prompts": prompts,
        "filenames": [item["filename"] for item in prompts],
        "numbers": numbers,
        "duplicates": duplicates,
        "gaps": gaps,
        "strict_two_digit": not malformed,
        "malformed": malformed,
    }


def has_prompt_section(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def immediate_next_reference(text: str, next_number: int) -> bool:
    strict_id = f"PROMPT_{next_number:02d}"
    plain = f"prompt {next_number:02d}"
    return strict_id in text or plain.lower() in text.lower()


def lint_registry_data(root: Path, prompt_dir: Path) -> dict[str, Any]:
    registry_path = root / "registry" / "prompts.json"
    if not registry_path.exists():
        return {"present": False, "ok": True, "path": "registry/prompts.json", "problems": []}

    data, problem = load_registry(registry_path)
    if problem:
        return {"present": True, "ok": False, "path": "registry/prompts.json", "problems": [problem]}

    assert data is not None
    registered_paths = [item.get("path") for item in data["items"] if isinstance(item, dict)]
    actual_paths = [str(path.relative_to(root)) for path in sorted(prompt_dir.glob("PROMPT_*.txt"))]
    ok = registered_paths == actual_paths
    problems = [] if ok else ["registry/prompts.json does not match prompt files"]
    return {
        "present": True,
        "ok": ok,
        "path": "registry/prompts.json",
        "registered_paths": registered_paths,
        "actual_paths": actual_paths,
        "problems": problems,
    }


def promptset_lint_data(root: Path, prompt_dir: Path | None = None) -> dict[str, Any]:
    prompt_dir = prompt_dir or (root / ".prompts")
    numbering = promptset_numbering_data(root, prompt_dir)
    problems: list[str] = []
    problems.extend(f"malformed prompt filename: {name}" for name in numbering["malformed"])
    problems.extend(f"duplicate prompt number: {number:02d}" for number in numbering["duplicates"])
    problems.extend(f"missing prompt number: {number:02d}" for number in numbering["gaps"])
    if not prompt_dir.is_dir():
        problems.append(f"missing prompt directory: {numbering['prompt_dir']}")

    unique_numbers = sorted(set(numbering["numbers"]))
    final_number = unique_numbers[-1] if unique_numbers else None
    prompt_reports: list[dict[str, Any]] = []
    for item in numbering["prompts"]:
        filename = item["filename"]
        number = item["number"]
        path = prompt_dir / filename
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        checks: dict[str, bool] = {"heading": bool(PROMPT_HEADING_RE.search(text))}
        for key, _label, terms in PROMPT_LINT_SECTIONS:
            checks[key] = has_prompt_section(text, terms)
        if number is not None and final_number is not None and number < final_number:
            checks["next_prompt_reference"] = immediate_next_reference(text, number + 1)
        else:
            checks["next_prompt_reference"] = True

        missing = [key for key, ok in checks.items() if not ok]
        total = len(checks)
        present = total - len(missing)
        score = round(present / total, 3) if total else 1.0
        for key in missing:
            problems.append(f"{filename}: missing {key.replace('_', ' ')}")
        prompt_reports.append(
            {
                "filename": filename,
                "number": number,
                "strict": item["strict"],
                "checks": checks,
                "missing": missing,
                "readiness_score": score,
                "readiness_present": present,
                "readiness_total": total,
            }
        )

    registry = lint_registry_data(root, prompt_dir)
    problems.extend(registry["problems"])
    ok = not problems
    return {
        "ok": ok,
        "prompt_dir": numbering["prompt_dir"],
        "summary": {
            "prompt_count": len(prompt_reports),
            "problem_count": len(problems),
            "average_readiness_score": round(
                sum(item["readiness_score"] for item in prompt_reports) / len(prompt_reports), 3
            )
            if prompt_reports
            else 0.0,
        },
        "problems": problems,
        "numbering": numbering,
        "registry": registry,
        "prompts": prompt_reports,
    }


def command_promptset(args: argparse.Namespace) -> int:
    if args.action == "lint":
        data = promptset_lint_data(repo_root())
        human = [f"promptset lint: {data['summary']['prompt_count']} prompts"]
        human.append(f"readiness average: {data['summary']['average_readiness_score']:.3f}")
        if data["ok"]:
            human.append("lint: ok")
        else:
            human.append("lint: problems found")
            human.extend(f"- {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)

    data = promptset_data(repo_root())
    human = [f"promptset: {len(data['prompts'])} prompts"]
    if data["gaps"]:
        human.append("gaps: " + ", ".join(str(n) for n in data["gaps"]))
    if data["duplicates"]:
        human.append("duplicates: " + ", ".join(str(n) for n in data["duplicates"]))
    if data["malformed"]:
        human.append("malformed: " + ", ".join(data["malformed"]))
    if data["ok"]:
        human.append("numbering: ok")
    return emit(data, args.json, human, 0 if data["ok"] else 1)


def validate_data(root: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    problems: list[str] = []

    def add_check(name: str, path: str, ok: bool) -> None:
        checks.append({"name": name, "path": path, "ok": ok})
        if not ok:
            problems.append(f"missing or invalid {name}: {path}")

    for filename in ("AGENT.md", "README.md"):
        add_check(filename, filename, (root / filename).is_file())

    for dirname in REQUIRED_TOP_LEVEL_DIRS:
        add_check(f"{dirname} directory", dirname, (root / dirname).is_dir())

    for dirname in REQUIRED_DOC_DIRS:
        path = f"docs/{dirname}"
        add_check(f"{path} directory", path, (root / path).is_dir())

    tests_present = (root / "tests" / "test_ahl.py").is_file()
    add_check("helper script tests", "tests/test_ahl.py", tests_present)

    promptset = promptset_data(root)
    promptset_ok = bool(promptset["ok"])
    checks.append(
        {
            "name": "prompt files strictly numbered",
            "path": ".prompts",
            "ok": promptset_ok,
            "count": len(promptset["prompts"]),
            "gaps": promptset["gaps"],
            "duplicates": promptset["duplicates"],
            "malformed": promptset["malformed"],
        }
    )
    if not promptset_ok:
        problems.append("prompt files are not strictly numbered")

    return {"ok": not problems, "checks": checks, "problems": problems, "promptset": promptset}


def command_validate(args: argparse.Namespace) -> int:
    data = validate_data(repo_root())
    human = ["validate: ok" if data["ok"] else "validate: problems found"]
    human.extend(f"- {problem}" for problem in data["problems"])
    return emit(data, args.json, human, 0 if data["ok"] else 1)


def registry_files(root: Path) -> list[Path]:
    registry_dir = root / "registry"
    if not registry_dir.is_dir():
        return []
    return sorted(registry_dir.glob("*.json"))


def load_registry(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, f"{path.name}: invalid JSON at line {exc.lineno}: {exc.msg}"
    if not isinstance(data, dict):
        return None, f"{path.name}: top-level value must be an object"
    items = data.get("items")
    if not isinstance(items, list):
        return None, f"{path.name}: missing items list"
    return data, None


def registry_check_data(root: Path) -> dict[str, Any]:
    registry_dir = root / "registry"
    checks: list[dict[str, Any]] = []
    problems: list[str] = []

    def add_check(name: str, path: str, ok: bool, **extra: Any) -> None:
        check = {"name": name, "path": path, "ok": ok}
        check.update(extra)
        checks.append(check)

    add_check("registry directory", "registry", registry_dir.is_dir())
    if not registry_dir.is_dir():
        problems.append("missing registry directory: registry")
        return {"ok": False, "checks": checks, "problems": problems, "registries": []}

    seen_files = {path.name for path in registry_files(root)}
    for filename in REQUIRED_REGISTRY_FILES:
        exists = filename in seen_files
        add_check(f"registry/{filename}", f"registry/{filename}", exists)
        if not exists:
            problems.append(f"missing registry file: registry/{filename}")

    registries: list[dict[str, Any]] = []
    for path in registry_files(root):
        rel = str(path.relative_to(root))
        data, problem = load_registry(path)
        if problem:
            add_check(f"{rel} parses", rel, False)
            problems.append(problem)
            continue
        assert data is not None
        items = data["items"]
        item_count = len(items)
        add_check(f"{rel} parses", rel, True, item_count=item_count)
        registries.append({"path": rel, "item_count": item_count})

        ids: set[str] = set()
        for index, item in enumerate(items):
            item_ref = f"{rel} item {index + 1}"
            if not isinstance(item, dict):
                problems.append(f"{item_ref}: item must be an object")
                continue
            missing = [field for field in REQUIRED_REGISTRY_FIELDS if field not in item]
            if missing:
                problems.append(f"{item_ref}: missing fields: {', '.join(missing)}")
            item_id = item.get("id")
            if isinstance(item_id, str):
                if item_id in ids:
                    problems.append(f"{item_ref}: duplicate id {item_id}")
                ids.add(item_id)
            else:
                problems.append(f"{item_ref}: id must be a string")
            path_value = item.get("path")
            if not isinstance(path_value, str) or not path_value:
                problems.append(f"{item_ref}: path must be a non-empty string")
            elif not (root / path_value).exists():
                problems.append(f"{item_ref}: referenced path does not exist: {path_value}")

    prompts_path = registry_dir / "prompts.json"
    if prompts_path.exists():
        data, problem = load_registry(prompts_path)
        if problem:
            problems.append(problem)
        else:
            assert data is not None
            registered_paths = [item.get("path") for item in data["items"] if isinstance(item, dict)]
            actual_paths = [str(path.relative_to(root)) for path in sorted((root / ".prompts").glob("PROMPT_*.txt"))]
            prompts_ok = registered_paths == actual_paths
            add_check("prompt registry ordering", "registry/prompts.json", prompts_ok)
            if not prompts_ok:
                problems.append("registry/prompts.json ordering does not match .prompts/PROMPT_*.txt")

    return {"ok": not problems, "checks": checks, "problems": problems, "registries": registries}


def registry_list_data(root: Path) -> dict[str, Any]:
    registries: list[dict[str, Any]] = []
    for path in registry_files(root):
        data, problem = load_registry(path)
        if problem:
            registries.append({"path": str(path.relative_to(root)), "ok": False, "problem": problem})
            continue
        assert data is not None
        registries.append(
            {
                "path": str(path.relative_to(root)),
                "ok": True,
                "item_count": len(data["items"]),
                "description": data.get("description", ""),
            }
        )
    return {"ok": all(item["ok"] for item in registries), "registries": registries}


def command_registry(args: argparse.Namespace) -> int:
    if args.action == "list":
        data = registry_list_data(repo_root())
        human = ["registry files:"]
        if not data["registries"]:
            human.append("- none")
        else:
            for item in data["registries"]:
                if item["ok"]:
                    human.append(f"- {item['path']}: {item['item_count']} items")
                else:
                    human.append(f"- {item['path']}: invalid")
        return emit(data, args.json, human, 0 if data["ok"] else 1)

    data = registry_check_data(repo_root())
    human = ["registry: ok" if data["ok"] else "registry: problems found"]
    human.extend(f"- {problem}" for problem in data["problems"])
    return emit(data, args.json, human, 0 if data["ok"] else 1)


def markdown_files_for_docs_check(root: Path) -> list[Path]:
    files: list[Path] = []
    for rel in DOCS_SCAN_ROOTS:
        path = root / rel
        if path.is_file() and path.suffix.lower() == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.glob("**/*.md")))
    return sorted(set(files))


def markdown_link_targets(text: str) -> list[str]:
    targets = [match.group(1).strip() for match in MARKDOWN_LINK_RE.finditer(text)]
    targets.extend(match.group(1).strip() for match in REFERENCE_LINK_RE.finditer(text))
    return targets


def clean_markdown_target(target: str) -> str:
    if not target:
        return ""
    if target.startswith("<") and ">" in target:
        target = target[1 : target.find(">")]
    else:
        target = target.split()[0]
    return unquote(target.strip())


def is_external_or_anchor_target(target: str) -> bool:
    if not target or target.startswith("#"):
        return True
    parsed = urlsplit(target)
    return bool(parsed.scheme or parsed.netloc)


def resolve_markdown_target(source: Path, target: str) -> Path:
    target = target.split("#", 1)[0]
    return (source.parent / target).resolve()


def index_text_links_dir(index_text: str, dirname: str) -> bool:
    return (
        f"`../{dirname}/" in index_text
        or f"`{dirname}/" in index_text
        or f"](../{dirname}/" in index_text
        or f"]({dirname}/" in index_text
    )


def docs_check_data(root: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    problems: list[str] = []
    links: list[dict[str, Any]] = []
    missing_links: list[dict[str, Any]] = []
    resolved_root = root.resolve()

    markdown_files = markdown_files_for_docs_check(root)
    checks.append({"name": "markdown scan roots", "path": ".", "ok": bool(markdown_files), "count": len(markdown_files)})
    if not markdown_files:
        problems.append("no markdown files found in documentation scan roots")

    docs_readme = root / DOCS_NAV_INDEX
    docs_readme_exists = docs_readme.is_file()
    checks.append({"name": "docs index exists", "path": DOCS_NAV_INDEX, "ok": docs_readme_exists})
    if not docs_readme_exists:
        problems.append(f"missing docs index page: {DOCS_NAV_INDEX}")

    for source in markdown_files:
        rel_source = str(source.relative_to(root))
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems.append(f"{rel_source}: not valid UTF-8")
            continue
        for raw_target in markdown_link_targets(text):
            target = clean_markdown_target(raw_target)
            if is_external_or_anchor_target(target):
                continue
            target_path = resolve_markdown_target(source, target)
            target_without_anchor = target.split("#", 1)[0]
            exists = bool(target_without_anchor) and target_path.exists()
            rel_target = (
                str(target_path.relative_to(resolved_root))
                if target_path.is_relative_to(resolved_root)
                else str(target_path)
            )
            item = {"source": rel_source, "target": target, "resolved": rel_target, "ok": exists}
            links.append(item)
            if not exists:
                missing_links.append(item)
                problems.append(f"{rel_source}: missing local link target {target}")

    nav_problems: list[str] = []
    navigation = {"index": DOCS_NAV_INDEX, "linked_dirs": [], "missing_dirs": []}
    if docs_readme_exists:
        index_text = docs_readme.read_text(encoding="utf-8")
        for dirname in DOCS_INDEX_DIRS:
            if index_text_links_dir(index_text, dirname):
                navigation["linked_dirs"].append(dirname)
            else:
                navigation["missing_dirs"].append(dirname)
                nav_problems.append(f"{DOCS_NAV_INDEX}: missing navigation link for {dirname}/")
    problems.extend(nav_problems)
    checks.append(
        {
            "name": "major documentation directories linked",
            "path": DOCS_NAV_INDEX,
            "ok": not nav_problems and docs_readme_exists,
            "missing_dirs": navigation["missing_dirs"],
        }
    )

    registry = {"present": bool(registry_files(root)), "ok": True, "problems": []}
    if registry["present"]:
        registry_data = registry_check_data(root)
        registry = {
            "present": True,
            "ok": registry_data["ok"],
            "problems": registry_data["problems"],
            "registries": registry_data["registries"],
        }
        problems.extend(f"registry consistency: {problem}" for problem in registry_data["problems"])
    checks.append({"name": "registry paths consistent", "path": "registry", "ok": registry["ok"], "required": False})

    return {
        "ok": not problems,
        "scan_roots": list(DOCS_SCAN_ROOTS),
        "anchors_validated": False,
        "checks": checks,
        "problems": problems,
        "scanned_files": [str(path.relative_to(root)) for path in markdown_files],
        "links": links,
        "missing_links": missing_links,
        "navigation": navigation,
        "registry": registry,
    }


def command_docs(args: argparse.Namespace) -> int:
    data = docs_check_data(repo_root())
    human = ["docs check: ok" if data["ok"] else "docs check: problems found"]
    human.append(f"- scanned markdown files: {len(data['scanned_files'])}")
    human.append(f"- checked local links: {len(data['links'])}")
    human.append(f"- missing local links: {len(data['missing_links'])}")
    if data["navigation"]["missing_dirs"]:
        human.append("- missing navigation dirs: " + ", ".join(data["navigation"]["missing_dirs"]))
    human.extend(f"- {problem}" for problem in data["problems"])
    return emit(data, args.json, human, 0 if data["ok"] else 1)


def load_json_file(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as exc:
        return None, f"{path}: invalid JSON at line {exc.lineno}: {exc.msg}"


def prompt_id_references(value: Any) -> list[tuple[str, Any]]:
    found: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in PROMPT_ID_FIELDS:
                found.append((key, item))
            found.extend(prompt_id_references(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(prompt_id_references(item))
    return found


def fixture_check_data(root: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    problems: list[str] = []
    fixture_root = root / "fixtures"

    def add_check(name: str, path: str, ok: bool, **extra: Any) -> None:
        check = {"name": name, "path": path, "ok": ok}
        check.update(extra)
        checks.append(check)

    add_check("fixtures directory", "fixtures", fixture_root.is_dir())
    if not fixture_root.is_dir():
        problems.append("missing fixtures directory: fixtures")
        return {"ok": False, "checks": checks, "problems": problems, "fixtures": []}

    fixtures: list[dict[str, Any]] = []
    for rel, spec in FIXTURE_SPECS.items():
        path = root / rel
        schema_rel = spec["schema"]
        exists = path.is_file()
        add_check(f"{rel} exists", rel, exists, schema=schema_rel)
        if not exists:
            problems.append(f"missing fixture: {rel}")
            continue

        if schema_rel is not None:
            schema_path = root / schema_rel
            schema_exists = schema_path.is_file()
            add_check(f"{rel} schema exists", schema_rel, schema_exists)
            if not schema_exists:
                problems.append(f"{rel}: expected schema file is missing: {schema_rel}")

        data, problem = load_json_file(path)
        if problem:
            add_check(f"{rel} parses", rel, False)
            problems.append(problem)
            continue
        add_check(f"{rel} parses", rel, True)
        if not isinstance(data, dict):
            problems.append(f"{rel}: top-level value must be an object")
            continue

        missing = [field for field in spec["required"] if field not in data]
        add_check(f"{rel} required top-level fields", rel, not missing, missing=missing)
        if missing:
            problems.append(f"{rel}: missing top-level fields: {', '.join(missing)}")

        bad_prompt_ids = [
            f"{field}={value!r}"
            for field, value in prompt_id_references(data)
            if not isinstance(value, str) or not PROMPT_ID_RE.fullmatch(value)
        ]
        add_check(f"{rel} prompt id references", rel, not bad_prompt_ids, bad_prompt_ids=bad_prompt_ids)
        if bad_prompt_ids:
            problems.append(f"{rel}: invalid prompt id references: {', '.join(bad_prompt_ids)}")

        fixtures.append({"path": rel, "schema": schema_rel})

    known = set(FIXTURE_SPECS)
    extra = sorted(str(path.relative_to(root)) for path in fixture_root.glob("**/*.json") if str(path.relative_to(root)) not in known)
    add_check("no unexpected fixture JSON files", "fixtures", not extra, extra=extra)
    if extra:
        problems.append("unexpected fixture JSON files: " + ", ".join(extra))

    return {"ok": not problems, "checks": checks, "problems": problems, "fixtures": fixtures}


def command_fixtures(args: argparse.Namespace) -> int:
    data = fixture_check_data(repo_root())
    human = ["fixtures: ok" if data["ok"] else "fixtures: problems found"]
    human.extend(f"- {problem}" for problem in data["problems"])
    return emit(data, args.json, human, 0 if data["ok"] else 1)


def dry_run_dirs(root: Path) -> tuple[Path, Path]:
    base = root / "dry-runs"
    return base / "scenarios", base / "expected"


def dry_run_scenario_files(root: Path) -> list[Path]:
    scenarios_dir, _expected_dir = dry_run_dirs(root)
    if not scenarios_dir.is_dir():
        return []
    return sorted(scenarios_dir.glob("*.json"))


def dry_run_ids(root: Path) -> list[str]:
    return [path.stem for path in dry_run_scenario_files(root)]


def parity_scenario_ids(root: Path) -> tuple[list[str], list[str]]:
    parity_path = root / "dry-runs" / "PARITY.md"
    if not parity_path.is_file():
        return [], ["missing dry-run parity tracker: dry-runs/PARITY.md"]

    ids: list[str] = []
    problems: list[str] = []
    in_table = False
    for line in parity_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table:
                break
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 4:
            continue
        header = cells[0].lower()
        if header == "scenario id":
            in_table = True
            continue
        if set(cells[0]) <= {"-", ":"}:
            continue
        if in_table and cells[0]:
            ids.append(cells[0])

    if not ids:
        problems.append("dry-runs/PARITY.md: no scenario rows found")
    return ids, problems


def relative_path_exists(root: Path, value: Any) -> tuple[bool, str | None]:
    if not isinstance(value, str) or not value:
        return False, "path value must be a non-empty string"
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return False, f"path escapes repository root: {value}"
    if not candidate.exists():
        return False, f"referenced path does not exist: {value}"
    return True, None


def dry_run_check_one(root: Path, scenario_id: str) -> dict[str, Any]:
    path = root / "dry-runs" / "scenarios" / f"{scenario_id}.json"
    problems: list[str] = []
    if not path.is_file():
        return {"id": scenario_id, "status": "missing", "problems": [f"missing scenario file: {path.relative_to(root)}"]}

    data, problem = load_json_file(path)
    if problem:
        return {"id": scenario_id, "status": "fail", "problems": [problem]}
    if not isinstance(data, dict):
        return {"id": scenario_id, "status": "fail", "problems": ["scenario top-level value must be an object"]}

    missing = [field for field in DRY_RUN_REQUIRED_FIELDS if field not in data]
    if missing:
        problems.append("missing required fields: " + ", ".join(missing))
    if data.get("id") != scenario_id:
        problems.append(f"id field must match scenario filename: {scenario_id}")

    for field in DRY_RUN_LIST_FIELDS:
        value = data.get(field)
        if not isinstance(value, list) or not value:
            problems.append(f"{field} must be a non-empty list")

    for field in ("input_artifacts", "expected_outputs"):
        value = data.get(field)
        if isinstance(value, list):
            for item in value:
                ok, path_problem = relative_path_exists(root, item)
                if not ok and path_problem:
                    problems.append(f"{field}: {path_problem}")

    return {"id": scenario_id, "status": "fail" if problems else "pass", "problems": problems}


def dry_run_check_data(root: Path, requested_id: str | None = None, check_all: bool = False) -> dict[str, Any]:
    listed_ids = dry_run_ids(root)
    parity_ids, parity_problems = parity_scenario_ids(root)
    ids = sorted(set(listed_ids).union(parity_ids)) if check_all else [requested_id or ""]
    results = [dry_run_check_one(root, scenario_id) for scenario_id in ids if scenario_id]

    scenario_file_ids = set(listed_ids)
    parity_missing = [scenario_id for scenario_id in parity_ids if scenario_id not in scenario_file_ids]
    problems = list(parity_problems)
    problems.extend(f"dry-runs/PARITY.md: missing backing JSON for {scenario_id}" for scenario_id in parity_missing)
    for result in results:
        problems.extend(f"{result['id']}: {problem}" for problem in result["problems"])

    ok = not problems
    return {
        "ok": ok,
        "scenario_count": len(results),
        "checked": [result["id"] for result in results],
        "results": results,
        "parity": {
            "path": "dry-runs/PARITY.md",
            "scenario_ids": parity_ids,
            "missing_backing_json": parity_missing,
            "problems": parity_problems,
        },
        "problems": problems,
    }


def dry_run_list_data(root: Path) -> dict[str, Any]:
    scenarios = []
    for path in dry_run_scenario_files(root):
        data, problem = load_json_file(path)
        scenario_id = path.stem
        purpose = ""
        if isinstance(data, dict):
            scenario_id = str(data.get("id") or scenario_id)
            purpose = str(data.get("purpose") or "")
        scenarios.append({"id": scenario_id, "path": str(path.relative_to(root)), "purpose": purpose, "ok": problem is None})
    return {"ok": True, "scenario_count": len(scenarios), "scenarios": scenarios}


def command_dry_run(args: argparse.Namespace) -> int:
    root = repo_root()
    if args.action == "list":
        data = dry_run_list_data(root)
        human = [f"dry-run scenarios: {data['scenario_count']}"]
        human.extend(f"- {item['id']}: {item['path']}" for item in data["scenarios"])
        return emit(data, args.json, human, 0)

    if not args.all and not args.scenario:
        raise SystemExit("dry-run check requires a scenario id or --all")
    data = dry_run_check_data(root, requested_id=args.scenario, check_all=args.all)
    human = ["dry-run check: ok" if data["ok"] else "dry-run check: problems found"]
    for result in data["results"]:
        human.append(f"- {result['id']}: {result['status']}")
        human.extend(f"  - {problem}" for problem in result["problems"])
    if data["parity"]["missing_backing_json"]:
        human.append("- parity missing backing JSON: " + ", ".join(data["parity"]["missing_backing_json"]))
    return emit(data, args.json, human, 0 if data["ok"] else 1)


def lane_dir(root: Path, value: str) -> tuple[Path, str | None]:
    path = (root / value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return path, f"lane path escapes repository root: {value}"
    return path, None


def lane_status_path(root: Path, directory: str) -> tuple[Path, str, str | None]:
    path, problem = lane_dir(root, directory)
    rel = str(path.relative_to(root.resolve())) if not problem else directory
    return path / "lane-status.json", rel, problem


def lane_status_data(root: Path, directory: str) -> dict[str, Any]:
    status_path, lane_rel, path_problem = lane_status_path(root, directory)
    resolved_root = root.resolve()
    problems: list[str] = []
    if path_problem:
        problems.append(path_problem)
        return {
            "ok": False,
            "lane_dir": lane_rel,
            "status_path": str(status_path),
            "state": None,
            "status": None,
            "problems": problems,
        }

    rel_status = str(status_path.relative_to(resolved_root))
    if not status_path.is_file():
        problems.append(f"missing lane status JSON: {rel_status}")
        return {
            "ok": False,
            "lane_dir": lane_rel,
            "status_path": rel_status,
            "state": None,
            "status": None,
            "problems": problems,
        }

    data, problem = load_json_file(status_path)
    if problem:
        problems.append(problem)
        return {
            "ok": False,
            "lane_dir": lane_rel,
            "status_path": rel_status,
            "state": None,
            "status": None,
            "problems": problems,
        }
    if not isinstance(data, dict):
        problems.append(f"{rel_status}: top-level value must be an object")
        return {
            "ok": False,
            "lane_dir": lane_rel,
            "status_path": rel_status,
            "state": None,
            "status": data,
            "problems": problems,
        }

    missing = [field for field in LANE_STATUS_REQUIRED_FIELDS if field not in data]
    if missing:
        problems.append(f"{rel_status}: missing required fields: {', '.join(missing)}")
    state = data.get("state")
    if not isinstance(state, str) or state not in LANE_STATES:
        problems.append(f"{rel_status}: state must be one of: {', '.join(LANE_STATES)}")
    if not isinstance(data.get("roles"), dict) or not data.get("roles"):
        problems.append(f"{rel_status}: roles must be a non-empty object")
    if not isinstance(data.get("artifacts"), list) or not data.get("artifacts"):
        problems.append(f"{rel_status}: artifacts must be a non-empty list")
    if not isinstance(data.get("stop_escalation"), dict):
        problems.append(f"{rel_status}: stop_escalation must be an object")

    return {
        "ok": not problems,
        "lane_dir": lane_rel,
        "status_path": rel_status,
        "state": state if isinstance(state, str) else None,
        "status": data,
        "problems": problems,
    }


def lane_check_data(root: Path, directory: str) -> dict[str, Any]:
    lane_path, path_problem = lane_dir(root, directory)
    resolved_root = root.resolve()
    lane_rel = str(lane_path.relative_to(resolved_root)) if not path_problem else directory
    checks: list[dict[str, Any]] = []
    problems: list[str] = []

    def add_check(name: str, path: str, ok: bool, **extra: Any) -> None:
        check = {"name": name, "path": path, "ok": ok}
        check.update(extra)
        checks.append(check)

    if path_problem:
        add_check("lane directory", directory, False)
        problems.append(path_problem)
        return {"ok": False, "lane_dir": lane_rel, "checks": checks, "missing_artifacts": [], "state": None, "problems": problems}

    add_check("lane directory", lane_rel, lane_path.is_dir())
    if not lane_path.is_dir():
        problems.append(f"missing lane directory: {lane_rel}")
        return {"ok": False, "lane_dir": lane_rel, "checks": checks, "missing_artifacts": [], "state": None, "problems": problems}

    missing_artifacts: list[str] = []
    for filename in LANE_REQUIRED_FILES:
        rel = f"{lane_rel}/{filename}"
        exists = (lane_path / filename).is_file()
        add_check(f"{filename} exists", rel, exists)
        if not exists:
            missing_artifacts.append(rel)
            problems.append(f"missing lane artifact: {rel}")

    status = lane_status_data(root, directory)
    add_check("lane status parses", status["status_path"], status["ok"], state=status["state"])
    problems.extend(status["problems"])

    status_data = status.get("status")
    if isinstance(status_data, dict):
        artifact_values = status_data.get("artifacts")
        if isinstance(artifact_values, list):
            for item in artifact_values:
                ok, path_problem = relative_path_exists(root, item)
                add_check(f"status artifact exists: {item}", str(item), ok)
                if not ok and path_problem:
                    problems.append(f"lane-status.json artifacts: {path_problem}")

    return {
        "ok": not problems,
        "lane_dir": lane_rel,
        "checks": checks,
        "missing_artifacts": missing_artifacts,
        "state": status["state"],
        "status": status_data if isinstance(status_data, dict) else None,
        "problems": problems,
    }


def command_lane(args: argparse.Namespace) -> int:
    root = repo_root()
    if args.action == "status":
        data = lane_status_data(root, args.directory)
        human = [
            f"lane status: {data['lane_dir']}",
            f"- state: {data['state'] or 'unknown'}",
        ]
        human.extend(f"- {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)

    data = lane_check_data(root, args.directory)
    human = ["lane check: ok" if data["ok"] else "lane check: problems found"]
    human.append(f"- lane: {data['lane_dir']}")
    human.append(f"- state: {data['state'] or 'unknown'}")
    human.append(f"- missing artifacts: {len(data['missing_artifacts'])}")
    human.extend(f"- {problem}" for problem in data["problems"])
    return emit(data, args.json, human, 0 if data["ok"] else 1)


def validate_slug(value: str) -> str:
    if not SLUG_RE.fullmatch(value):
        raise SystemExit("slug must use lowercase letters, numbers, and hyphens")
    return value


def path_within_root(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def relative_out_dir(root: Path, value: str) -> Path:
    path = root / value
    if not path_within_root(root, path):
        raise SystemExit(f"output directory escapes repository root: {value}")
    return path


def replace_template_fields(text: str, replacements: dict[str, str]) -> str:
    lines = [replacements.get(line, line) for line in text.splitlines()]
    return "\n".join(lines) + "\n"


def scaffold_from_templates(
    root: Path,
    target_dir: Path,
    templates: tuple[tuple[str, str], ...],
    replacements: dict[str, str],
    force: bool,
) -> tuple[list[str], list[str]]:
    collisions: list[str] = []
    created: list[str] = []
    for _template_rel, target_name in templates:
        target = target_dir / target_name
        if target.exists() and not force:
            collisions.append(str(target.relative_to(root)))
    if collisions:
        return [], collisions

    target_dir.mkdir(parents=True, exist_ok=True)
    for template_rel, target_name in templates:
        template_path = root / template_rel
        content = template_path.read_text(encoding="utf-8") if template_path.exists() else f"# {Path(target_name).stem.title()}\n"
        target = target_dir / target_name
        target.write_text(replace_template_fields(content, replacements), encoding="utf-8")
        created.append(str(target.relative_to(root)))
    return created, []


def command_experiment(args: argparse.Namespace) -> int:
    root = repo_root()
    if args.action == "check":
        data = experiment_check_data(root, args.dir)
        human = ["experiment check: ok" if data["ok"] else "experiment check: problems found"]
        human.append(f"- experiments checked: {len(data['experiments'])}")
        human.extend(f"- {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)

    if not args.slug:
        raise SystemExit("experiment new requires a slug")
    slug = validate_slug(args.slug)
    target_base = relative_out_dir(root, args.out_dir)
    target_dir = target_base / slug
    today = dt.date.today().isoformat()
    replacements = {
        "- Experiment id:": f"- Experiment id: {slug}",
        "- Date opened:": f"- Date opened: {today}",
        "- Status: Planned / Active": "- Status: Active",
        "- Log date:": f"- Log date: {today}",
        "- Status: Closed / Abandoned / Superseded": "- Status: Closed / Abandoned / Superseded",
    }
    created, collisions = scaffold_from_templates(
        root,
        target_dir,
        EXPERIMENT_TEMPLATE_FILES,
        replacements,
        args.force,
    )
    if collisions:
        data = {"ok": False, "slug": slug, "created": [], "collisions": collisions}
        return emit(data, args.json, ["refusing to overwrite: " + ", ".join(collisions)], 1)

    data = {
        "ok": True,
        "slug": slug,
        "directory": str(target_dir.relative_to(root)),
        "created": created,
        "forced": args.force,
        "catalog_updated": False,
    }
    human = [f"created experiment scaffold: {data['directory']}"]
    human.extend(f"- {path}" for path in created)
    return emit(data, args.json, human, 0)


def field_has_value(text: str, field: str) -> bool:
    for line in text.splitlines():
        if line.startswith(field):
            return bool(line[len(field) :].strip())
    return False


def experiment_check_data(root: Path, directory: str) -> dict[str, Any]:
    base = relative_out_dir(root, directory)
    checks: list[dict[str, Any]] = []
    problems: list[str] = []
    experiments: list[dict[str, Any]] = []

    checks.append(
        {
            "name": "experiment directory",
            "path": directory,
            "ok": True,
            "required": False,
            "present": base.is_dir(),
        }
    )
    if not base.is_dir():
        return {"ok": True, "directory": directory, "checks": checks, "problems": [], "experiments": []}

    experiment_dirs = sorted(path for path in base.iterdir() if path.is_dir())
    checks.append({"name": "experiment entries", "path": directory, "ok": True, "count": len(experiment_dirs)})

    for experiment_dir in experiment_dirs:
        rel_dir = str(experiment_dir.relative_to(root))
        item_problems: list[str] = []
        for filename in EXPERIMENT_REQUIRED_FILES:
            path = experiment_dir / filename
            if not path.is_file():
                item_problems.append(f"missing required file: {filename}")
                continue
            text = path.read_text(encoding="utf-8")
            missing_fields = [
                field
                for field in EXPERIMENT_REQUIRED_FIELDS.get(filename, ())
                if not field_has_value(text, field)
            ]
            item_problems.extend(f"{filename}: missing value for {field}" for field in missing_fields)
        status = "fail" if item_problems else "pass"
        experiments.append({"id": experiment_dir.name, "path": rel_dir, "status": status, "problems": item_problems})
        problems.extend(f"{rel_dir}: {problem}" for problem in item_problems)

    return {
        "ok": not problems,
        "directory": directory,
        "checks": checks,
        "problems": problems,
        "experiments": experiments,
    }


def command_finding(args: argparse.Namespace) -> int:
    root = repo_root()
    slug = validate_slug(args.slug)
    target_base = relative_out_dir(root, args.out_dir)
    target_dir = target_base / slug
    today = dt.date.today().isoformat()
    replacements = {
        "- Finding id:": f"- Finding id: {slug}",
        "- Date:": f"- Date: {today}",
        "- Status: Draft / Reviewed / Superseded / Rejected": "- Status: Draft",
    }
    created, collisions = scaffold_from_templates(root, target_dir, FINDING_TEMPLATE_FILES, replacements, args.force)
    if collisions:
        data = {"ok": False, "slug": slug, "created": [], "collisions": collisions}
        return emit(data, args.json, ["refusing to overwrite: " + ", ".join(collisions)], 1)

    data = {
        "ok": True,
        "slug": slug,
        "directory": str(target_dir.relative_to(root)),
        "created": created,
        "forced": args.force,
    }
    return emit(data, args.json, [f"created finding scaffold: {data['directory']}"], 0)


def memory_candidate_path(root: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.suffix == ".md" or "/" in value:
        path = root / candidate
    else:
        slug = validate_slug(value)
        path = root / "memory" / "promotion-queue" / f"{slug}.md"
    if not path_within_root(root, path):
        raise SystemExit(f"candidate path escapes repository root: {value}")
    return path


def fill_memory_candidate(template: str, slug: str) -> str:
    today = dt.date.today().isoformat()
    replacements = {
        "- Candidate id:": f"- Candidate id: {slug}",
        "- Date proposed:": f"- Date proposed: {today}",
        "- Status: Proposed / In Review / Accepted / Rejected / Superseded": "- Status: Proposed",
    }
    return replace_template_fields(template, replacements)


def fill_memory_decision(template: str, slug: str, decision: str, candidate_rel: str) -> str:
    today = dt.date.today().isoformat()
    title = decision.capitalize()
    replacements = {
        "- Decision id:": f"- Decision id: {slug}-{decision}",
        "- Candidate id:": f"- Candidate id: {slug}",
        "- Candidate source:": f"- Candidate source: {candidate_rel}",
        "- Decision date:": f"- Decision date: {today}",
        "- Decision: Accepted / Rejected": f"- Decision: {title}",
        "- Status: Draft / Reviewed": "- Status: Draft",
    }
    return replace_template_fields(template, replacements)


def memory_candidate_check(root: Path, path: Path) -> dict[str, Any]:
    rel = str(path.relative_to(root))
    item_problems: list[str] = []
    if not path.is_file():
        return {"path": rel, "status": "missing", "problems": ["candidate file is missing"]}

    text = path.read_text(encoding="utf-8")
    missing_headings = [heading for heading in MEMORY_CANDIDATE_REQUIRED_HEADINGS if heading not in text]
    missing_fields = [field for field in MEMORY_CANDIDATE_REQUIRED_FIELDS if not field_has_value(text, field)]
    item_problems.extend(f"missing heading: {heading}" for heading in missing_headings)
    item_problems.extend(f"missing value for {field}" for field in missing_fields)
    status = "fail" if item_problems else "pass"
    return {"path": rel, "status": status, "problems": item_problems}


def memory_check_data(root: Path) -> dict[str, Any]:
    queue = root / "memory" / "promotion-queue"
    checks = [
        {
            "name": "promotion queue directory",
            "path": "memory/promotion-queue",
            "ok": True,
            "required": False,
            "present": queue.is_dir(),
        }
    ]
    if not queue.is_dir():
        return {"ok": True, "checks": checks, "problems": [], "candidates": []}

    candidates: list[dict[str, Any]] = []
    problems: list[str] = []
    for path in sorted(queue.glob("*.md")):
        if path.name == "README.md":
            continue
        result = memory_candidate_check(root, path)
        candidates.append(result)
        problems.extend(f"{result['path']}: {problem}" for problem in result["problems"])

    checks.append({"name": "promotion candidates", "path": "memory/promotion-queue", "ok": not problems, "count": len(candidates)})
    return {"ok": not problems, "checks": checks, "problems": problems, "candidates": candidates}


def command_memory(args: argparse.Namespace) -> int:
    root = repo_root()
    if args.action == "check":
        data = memory_check_data(root)
        human = ["memory check: ok" if data["ok"] else "memory check: problems found"]
        human.append(f"- candidates checked: {len(data['candidates'])}")
        human.extend(f"- {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)

    if args.action == "propose":
        if not args.target:
            raise SystemExit("memory propose requires a slug")
        slug = validate_slug(args.target)
        target = root / "memory" / "promotion-queue" / f"{slug}.md"
        if target.exists() and not args.force:
            data = {"ok": False, "slug": slug, "created": None, "collisions": [str(target.relative_to(root))]}
            return emit(data, args.json, ["refusing to overwrite: " + str(target.relative_to(root))], 1)
        template_path = root / MEMORY_CANDIDATE_TEMPLATE
        template = template_path.read_text(encoding="utf-8") if template_path.exists() else "# Promotion Candidate\n"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(fill_memory_candidate(template, slug), encoding="utf-8")
        data = {"ok": True, "slug": slug, "created": str(target.relative_to(root)), "forced": args.force}
        return emit(data, args.json, [f"created memory promotion candidate: {data['created']}"], 0)

    if not args.target:
        raise SystemExit("memory decision requires a candidate slug or path")
    if not args.accepted and not args.rejected:
        raise SystemExit("memory decision requires --accepted or --rejected")
    candidate = memory_candidate_path(root, args.target)
    if not candidate.is_file():
        data = {"ok": False, "candidate": str(candidate.relative_to(root)), "created": None, "problem": "candidate file is missing"}
        return emit(data, args.json, [f"candidate file is missing: {data['candidate']}"], 1)
    decision = "accepted" if args.accepted else "rejected"
    slug = candidate.stem
    target = root / "memory" / decision / f"{slug}-decision.md"
    if target.exists() and not args.force:
        data = {"ok": False, "candidate": str(candidate.relative_to(root)), "created": None, "collisions": [str(target.relative_to(root))]}
        return emit(data, args.json, ["refusing to overwrite: " + str(target.relative_to(root))], 1)
    template_path = root / MEMORY_DECISION_TEMPLATE
    template = template_path.read_text(encoding="utf-8") if template_path.exists() else "# Promotion Decision\n"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        fill_memory_decision(template, slug, "accepted" if args.accepted else "rejected", str(candidate.relative_to(root))),
        encoding="utf-8",
    )
    data = {
        "ok": True,
        "candidate": str(candidate.relative_to(root)),
        "decision": decision,
        "created": str(target.relative_to(root)),
        "forced": args.force,
    }
    return emit(data, args.json, [f"created memory promotion decision: {data['created']}"], 0)


def normalize_prompt_id(value: str) -> str:
    path_name = Path(value).name
    strict = STRICT_PROMPT_RE.match(path_name)
    if strict:
        return f"PROMPT_{strict.group(1)}"
    if re.fullmatch(r"\d+", value):
        return f"PROMPT_{int(value):02d}"
    if re.fullmatch(r"PROMPT_\d{2}", value):
        return value
    raise SystemExit(f"invalid prompt id or filename: {value}")


def fill_manifest(template: str, prompt_id: str, run_id: str, assistant: str, posture: str) -> str:
    today = dt.date.today().isoformat()
    replacements = {
        "- Artifact id:": f"- Artifact id: {run_id}",
        "- Prompt id:": f"- Prompt id: {prompt_id}",
        "- Run id:": f"- Run id: {run_id}",
        "- Date:": f"- Date: {today}",
        "- Assistant/tool:": f"- Assistant/tool: {assistant}",
        "- Permission posture:": f"- Permission posture: {posture}",
    }
    lines = [replacements.get(line, line) for line in template.splitlines()]
    return "\n".join(lines) + "\n"


def command_scaffold_run(args: argparse.Namespace) -> int:
    root = repo_root()
    prompt_id = normalize_prompt_id(args.prompt)
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id = f"{prompt_id}-{timestamp}"
    out_dir = root / args.out_dir
    target_dir = out_dir / run_id
    target = target_dir / "run-manifest.md"
    if target.exists() and not args.force:
        data = {"ok": False, "created": None, "problem": f"{target} already exists"}
        return emit(data, args.json, [f"refusing to overwrite {target}"], 1)
    template_path = root / "templates" / "runs" / "run-manifest.md"
    template = template_path.read_text(encoding="utf-8") if template_path.exists() else "# Run Manifest\n"
    target_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(
        fill_manifest(template, prompt_id, run_id, args.assistant, args.permission_posture),
        encoding="utf-8",
    )
    data = {"ok": True, "created": str(target.relative_to(root)), "run_id": run_id, "prompt_id": prompt_id}
    return emit(data, args.json, [f"created {target.relative_to(root)}"], 0)


def runtime_file_info(root: Path) -> tuple[list[dict[str, Any]], int]:
    paths = [root / "context" / name for name in CONTEXT_FILES] + [root / "PLAN.md"]
    infos = []
    total = 0
    for path in paths:
        exists = path.exists()
        lines = line_count(path) if exists else 0
        total += lines
        infos.append({"path": str(path.relative_to(root)), "exists": exists, "lines": lines})
    return infos, total


def command_resume(args: argparse.Namespace) -> int:
    root = repo_root()
    changed = git_changed_files()
    runtime_files, runtime_lines = runtime_file_info(root)
    tmp_count = len(list((root / "tmp").glob("*.md"))) if (root / "tmp").is_dir() else 0
    if runtime_lines < 100:
        posture = "lean"
    elif runtime_lines <= 300:
        posture = "moderate"
    else:
        posture = "heavy"
    if changed:
        recommendation = "Review working-tree changes before editing."
    elif tmp_count:
        recommendation = "Review active tmp markdown notes before starting."
    else:
        recommendation = "Load AGENT.md and the active prompt."
    data = {
        "branch": git_value(["branch", "--show-current"], "unknown"),
        "head": git_value(["rev-parse", "--short", "HEAD"], "unknown"),
        "clean": not changed,
        "changed_count": len(changed),
        "runtime_files": runtime_files,
        "tmp_markdown_count": tmp_count,
        "runtime_note_lines": runtime_lines,
        "posture": posture,
        "recommendation": recommendation,
    }
    human = [
        "Session Context Briefing",
        f"- Branch: {data['branch']}",
        f"- HEAD: {data['head']}",
        f"- Working tree: {'clean' if data['clean'] else str(data['changed_count']) + ' changed files'}",
        f"- Runtime notes: {runtime_lines} lines ({posture})",
        f"- tmp/*.md: {tmp_count}",
        f"- Recommended next action: {recommendation}",
    ]
    return emit(data, args.json, human, 0)


def minimal_context(name: str) -> str:
    title = Path(name).stem.title()
    return f"# {title}\n\n## Status\n\n- Created by `scripts/ahl.py checkpoint`.\n- Next step:\n"


def command_checkpoint(args: argparse.Namespace) -> int:
    root = repo_root()
    context_dir = root / "context"
    context_dir.mkdir(exist_ok=True)
    existing: list[str] = []
    scaffolded: list[str] = []
    for name in CONTEXT_FILES:
        target = context_dir / name
        rel = str(target.relative_to(root))
        if target.exists() and not args.force:
            existing.append(rel)
            continue
        example = context_dir / f"{Path(name).stem}.example.md"
        content = example.read_text(encoding="utf-8") if example.exists() else minimal_context(name)
        target.write_text(content, encoding="utf-8")
        scaffolded.append(rel)

    session = context_dir / "SESSION.md"
    stale = False
    if session.exists():
        stale = not any(NEXT_MARKER_RE.match(line) for line in session.read_text(encoding="utf-8").splitlines())

    data = {"ok": True, "existing": existing, "scaffolded": scaffolded, "stale": {"context/SESSION.md": stale}}
    human = ["checkpoint: ok"]
    if scaffolded:
        human.append("scaffolded: " + ", ".join(scaffolded))
    if existing:
        human.append("existing: " + ", ".join(existing))
    if stale:
        human.append("stale: context/SESSION.md lacks a next-step marker")
    return emit(data, args.json, human, 0)


def command_new_handoff(args: argparse.Namespace) -> int:
    root = repo_root()
    tmp_dir = root / "tmp"
    target = tmp_dir / "HANDOFF.md"
    if target.exists() and not args.force:
        data = {"ok": False, "created": None, "problem": "tmp/HANDOFF.md already exists"}
        return emit(data, args.json, ["refusing to overwrite tmp/HANDOFF.md"], 1)
    template_path = root / "templates" / "handoffs" / "handoff.md"
    content = template_path.read_text(encoding="utf-8") if template_path.exists() else "# Handoff\n"
    tmp_dir.mkdir(exist_ok=True)
    target.write_text(content, encoding="utf-8")
    data = {"ok": True, "created": "tmp/HANDOFF.md", "forced": args.force}
    return emit(data, args.json, ["created tmp/HANDOFF.md"], 0)


def command_metadata_example(args: argparse.Namespace) -> int:
    prompt_id = normalize_prompt_id(args.prompt)
    today = (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    data: dict[str, Any] = {
        "prompt_id": prompt_id,
        "prompt_batch_id": args.prompt_batch_id,
        "run_id": f"{prompt_id}-YYYYMMDD-HHMMSS",
        "assistant_tool": args.assistant,
        "permission_posture": args.permission_posture,
        "started_at": today,
        "ended_at": None,
        "changed_files": [],
        "changed_directories": [],
        "docs_changed": False,
        "tests_changed": False,
        "validation_commands": [],
        "completion_audit_status": "not_started",
        "next_prompt_ready": None,
        "readiness_blockers": [],
        "handoff_created": False,
        "follow_up_fix_required": False,
        "reusable_pattern_observations": [],
        "associated_commit_hashes": [],
    }
    human = [
        f"Run record skeleton for {prompt_id}",
        f"- Run id: {data['run_id']}",
        f"- Assistant/tool: {data['assistant_tool']}",
        f"- Permission posture: {data['permission_posture']}",
        "- Fill changed files, validation, audit, readiness, and commit hashes when known.",
    ]
    return emit(data, args.json, human, 0)


def command_help(args: argparse.Namespace) -> int:
    data = {
        "ok": True,
        "commands": list(COMMAND_HELP),
        "makefile_targets": [item["name"] for item in COMMAND_HELP],
    }
    human = ["operator console targets:"]
    human.extend(
        f"- {item['name']}: {item['command']} ({item['safety']})"
        for item in COMMAND_HELP
    )
    return emit(data, args.json, human, 0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ahl", description="Small helper tooling for agent-harness-lab.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    help_command = subparsers.add_parser("help", help="List common operator console commands.")
    help_command.add_argument("--json", action="store_true")
    help_command.set_defaults(func=command_help)

    doctor = subparsers.add_parser("doctor", help="Check expected repository foundations.")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=command_doctor)

    promptset = subparsers.add_parser("promptset", help="Inspect prompt filenames, numbering, and readiness.")
    promptset.add_argument("action", nargs="?", choices=("lint",), help="Run promptset prose-structure linting.")
    promptset.add_argument("--json", action="store_true")
    promptset.set_defaults(func=command_promptset)

    validate = subparsers.add_parser("validate", help="Check promptset and expected quality foundations.")
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(func=command_validate)

    registry = subparsers.add_parser("registry", help="List or validate curated registry indexes.")
    registry.add_argument("action", choices=("list", "check"))
    registry.add_argument("--json", action="store_true")
    registry.set_defaults(func=command_registry)

    docs = subparsers.add_parser("docs", help="Check markdown navigation and local links.")
    docs.add_argument("action", choices=("check",))
    docs.add_argument("--json", action="store_true")
    docs.set_defaults(func=command_docs)

    fixtures = subparsers.add_parser("fixtures", help="Validate artificial JSON fixtures structurally.")
    fixtures.add_argument("action", choices=("check",))
    fixtures.add_argument("--json", action="store_true")
    fixtures.set_defaults(func=command_fixtures)

    dry_run = subparsers.add_parser("dry-run", help="List and structurally check deterministic dry-run scenarios.")
    dry_run.add_argument("action", choices=("list", "check"))
    dry_run.add_argument("scenario", nargs="?", help="Scenario id to check.")
    dry_run.add_argument("--all", action="store_true", help="Check every scenario and PARITY.md backing file.")
    dry_run.add_argument("--json", action="store_true")
    dry_run.set_defaults(func=command_dry_run)

    lane = subparsers.add_parser("lane", help="Inspect manual lane simulation artifacts.")
    lane.add_argument("action", choices=("check", "status"))
    lane.add_argument("directory", help="Lane simulation directory, such as simulations/lane-demo.")
    lane.add_argument("--json", action="store_true")
    lane.set_defaults(func=command_lane)

    experiment = subparsers.add_parser("experiment", help="Scaffold and check lightweight experiment artifacts.")
    experiment.add_argument("action", choices=("new", "check"))
    experiment.add_argument("slug", nargs="?", help="Experiment slug for `experiment new`.")
    experiment.add_argument("--dir", default="experiments/active", help="Directory checked by `experiment check`.")
    experiment.add_argument("--out-dir", default="experiments/active", help="Base directory for `experiment new`.")
    experiment.add_argument("--force", action="store_true", help="Overwrite an existing experiment scaffold.")
    experiment.add_argument("--json", action="store_true")
    experiment.set_defaults(func=command_experiment)

    finding = subparsers.add_parser("finding", help="Scaffold reviewed finding artifacts.")
    finding.add_argument("action", choices=("new",))
    finding.add_argument("slug", help="Finding slug.")
    finding.add_argument("--out-dir", default="findings/draft", help="Base directory for new finding records.")
    finding.add_argument("--force", action="store_true", help="Overwrite an existing finding scaffold.")
    finding.add_argument("--json", action="store_true")
    finding.set_defaults(func=command_finding)

    memory = subparsers.add_parser("memory", help="Scaffold and check reviewed memory promotion artifacts.")
    memory.add_argument("action", choices=("propose", "check", "decision"))
    memory.add_argument("target", nargs="?", help="Slug for `memory propose`; slug or path for `memory decision`.")
    decision_group = memory.add_mutually_exclusive_group()
    decision_group.add_argument("--accepted", action="store_true", help="Scaffold an accepted decision record.")
    decision_group.add_argument("--rejected", action="store_true", help="Scaffold a rejected decision record.")
    memory.add_argument("--force", action="store_true", help="Overwrite an existing memory scaffold.")
    memory.add_argument("--json", action="store_true")
    memory.set_defaults(func=command_memory)

    resume = subparsers.add_parser("resume", help="Print a grounded session context briefing.")
    resume.add_argument("--json", action="store_true")
    resume.set_defaults(func=command_resume)

    trace = subparsers.add_parser("trace", help="Summarize prompt-related working tree traceability.")
    trace.add_argument("prompt", help="Prompt id, number, or prompt filename.")
    trace.add_argument("--json", action="store_true")
    trace.set_defaults(func=command_trace)

    checkpoint = subparsers.add_parser("checkpoint", help="Report and scaffold local context files.")
    checkpoint.add_argument("--json", action="store_true")
    checkpoint.add_argument("--force", action="store_true", help="Overwrite existing context files.")
    checkpoint.set_defaults(func=command_checkpoint)

    scaffold = subparsers.add_parser("scaffold-run", help="Create a run manifest from the template.")
    scaffold.add_argument("prompt")
    scaffold.add_argument("--assistant", default="unspecified")
    scaffold.add_argument("--permission-posture", default="unspecified")
    scaffold.add_argument("--out-dir", default="runs")
    scaffold.add_argument("--force", action="store_true", help="Overwrite an existing generated file.")
    scaffold.add_argument("--json", action="store_true")
    scaffold.set_defaults(func=command_scaffold_run)

    handoff = subparsers.add_parser("new-handoff", help="Create tmp/HANDOFF.md from the handoff template.")
    handoff.add_argument("--force", action="store_true", help="Overwrite tmp/HANDOFF.md if it exists.")
    handoff.add_argument("--json", action="store_true")
    handoff.set_defaults(func=command_new_handoff)

    metadata = subparsers.add_parser("metadata-example", help="Print a skeleton run record.")
    metadata.add_argument("prompt")
    metadata.add_argument("--assistant", default="unspecified")
    metadata.add_argument(
        "--permission-posture",
        choices=("read-only", "workspace-write", "manual-required"),
        default="workspace-write",
    )
    metadata.add_argument("--prompt-batch-id", default="promptset")
    metadata.add_argument("--json", action="store_true")
    metadata.set_defaults(func=command_metadata_example)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
