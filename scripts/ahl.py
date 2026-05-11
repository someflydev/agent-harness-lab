#!/usr/bin/env python3
"""Small helper CLI for agent-harness-lab."""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit


PROMPT_RE = re.compile(r"^PROMPT_(\d+)\.txt$")
STRICT_PROMPT_RE = re.compile(r"^PROMPT_(\d{2})\.txt$")
PROMPT_COMMIT_RE = re.compile(r"\[PROMPT_(\d{2,})\]")
PROMPT_COMMIT_SUBJECT_RE = re.compile(r"^\[PROMPT_\d{2,}\]\s+\S")
NEXT_MARKER_RE = re.compile(r"^\s*(?:[-*]\s*)?(?:Next|Next step|## Next)\b", re.I)
PROMPT_HEADING_RE = re.compile(r"^\s*#\s+PROMPT_\d{2}\b", re.M)
COMMIT_SUBJECT_LIMIT = 72
COMMIT_BODY_LINE_LIMIT = 72
COMMIT_CHECK_DEFAULT_LIMIT = 10
CONTEXT_FILES = ("TASK.md", "SESSION.md", "MEMORY.md")
CONTEXT_ROOTS = ("context", ".context")
BOOTSTRAP_CONTEXT_FILES = ("AGENT.md", "CLAUDE.md")
REFERENCE_DIRS = ("agent-context-base", "pi-mono", "claw-code")
TRANSCRIPT_DUMP_PATHS = (
    "transcripts",
    "conversation-dumps",
    "chat-transcripts",
    "assistant-transcripts",
    "chatgpt-export",
    "claude-export",
)
TRANSCRIPT_DUMP_FILES = (
    "transcripts.md",
    "transcript.md",
    "conversation-dump.md",
    "conversation-dump.json",
    "chat-export.md",
    "chat-export.json",
)
SECRET_NAME_PATTERNS = (
    ".env",
    ".env.*",
    "secret",
    "secrets",
    "secret.*",
    "secrets.*",
    "credential",
    "credentials",
    "credential.*",
    "credentials.*",
    "*.pem",
    "*.key",
    "id_rsa",
    "id_ed25519",
)
REQUIRED_IGNORE_PATTERNS = (
    "tmp/",
    ".runtime/",
    ".session/",
    "agent-context-base/",
    "pi-mono/",
    "claw-code/",
    "transcripts/",
    "conversation-dumps/",
    "chat-transcripts/",
    "assistant-transcripts/",
    "chatgpt-export/",
    "claude-export/",
    "transcripts.md",
    "transcript.md",
    "conversation-dump.md",
    "conversation-dump.json",
    "chat-export.md",
    "chat-export.json",
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "id_rsa",
    "id_ed25519",
)
REQUIRED_TOP_LEVEL_DIRS = ("docs", "runbooks", "templates", "scripts", "tests", ".prompts")
REQUIRED_DOC_DIRS = ("contracts", "doctrine", "memory", "quality", "roles", "routines", "runtime", "safety", "skills")
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
    "domain-packs",
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
    "domain-packs",
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
    "fixtures/outer-loop/plans/valid-next-three.json": {
        "schema": "schemas/outer-loop-plan.schema.json",
        "required": ("plan_id", "created_at", "requested_range", "prompts", "driver", "required_ahl_checks", "stop_conditions", "commit_policy", "run_artifact_dir"),
    },
    "fixtures/outer-loop/plans/missing-prompt.json": {
        "schema": "schemas/outer-loop-plan.schema.json",
        "required": ("plan_id", "created_at", "requested_range", "prompts", "driver", "required_ahl_checks", "stop_conditions", "commit_policy", "run_artifact_dir"),
    },
    "fixtures/outer-loop/reports/dry-run-pass.json": {
        "schema": "schemas/outer-loop-dry-run-report.schema.json",
        "required": ("ok", "plan_id", "steps", "problems"),
    },
    "fixtures/portable-operator/run-range/valid-plan.json": {
        "schema": "schemas/portable-operator-run-plan.schema.json",
        "required": ("ok", "schema", "plan_id", "mode", "dry_run", "project", "requested_range", "prompt_ids", "steps", "next_prompt", "safety_notes", "problems"),
    },
    "fixtures/outer-loop/gates/pass.json": {
        "schema": "schemas/outer-loop-gate-report.schema.json",
        "required": ("ok", "status", "prompt_id", "changed_files", "validation_commands", "validation_outcomes", "ahl_checks", "completion_audit", "next_prompt_readiness", "handoff", "commit_plan", "decision"),
    },
    "fixtures/outer-loop/gates/blocked.json": {
        "schema": "schemas/outer-loop-gate-report.schema.json",
        "required": ("ok", "status", "prompt_id", "changed_files", "validation_commands", "validation_outcomes", "ahl_checks", "completion_audit", "next_prompt_readiness", "handoff", "commit_plan", "decision"),
    },
    "fixtures/outer-loop/runs/live-runner-example.json": {
        "schema": "schemas/outer-loop-run-ledger.schema.json",
        "required": ("ok", "status", "run_id", "plan_id", "mode", "driver", "steps", "problems"),
    },
    "fixtures/outer-loop/runs/interrupted-ledger.json": {
        "schema": "schemas/outer-loop-run-ledger.schema.json",
        "required": ("ok", "status", "run_id", "plan_id", "mode", "driver", "steps", "problems", "resume_pointer", "stop_reason", "recovery_recommendation"),
    },
    "fixtures/outer-loop/runs/blocked-ledger.json": {
        "schema": "schemas/outer-loop-run-ledger.schema.json",
        "required": ("ok", "status", "run_id", "plan_id", "mode", "driver", "steps", "problems", "resume_pointer", "stop_reason", "recovery_recommendation"),
    },
    "fixtures/outer-loop/runs/resumable-ledger.json": {
        "schema": "schemas/outer-loop-run-ledger.schema.json",
        "required": ("ok", "status", "run_id", "plan_id", "mode", "driver", "steps", "problems", "resume_pointer", "stop_reason", "recovery_recommendation"),
    },
    "fixtures/outer-loop/commits/plan-one-prompt.json": {
        "schema": "schemas/commit-plan.schema.json",
        "required": ("ok", "schema", "plan_id", "mode", "prompt_ids", "groups", "git", "problems"),
    },
    "fixtures/outer-loop/commits/plan-batch.json": {
        "schema": "schemas/commit-plan.schema.json",
        "required": ("ok", "schema", "plan_id", "mode", "prompt_ids", "groups", "git", "problems"),
    },
    "fixtures/assistant-drivers/codex.json": {
        "schema": "schemas/assistant-driver.schema.json",
        "required": ("id", "display_name", "driver_kind", "executable_name", "probe_expectation", "live_run_status"),
    },
    "fixtures/assistant-drivers/gemini.json": {
        "schema": "schemas/assistant-driver.schema.json",
        "required": ("id", "display_name", "driver_kind", "executable_name", "probe_expectation", "live_run_status"),
    },
    "fixtures/assistant-drivers/pi.json": {
        "schema": "schemas/assistant-driver.schema.json",
        "required": ("id", "display_name", "driver_kind", "executable_name", "probe_expectation", "live_run_status"),
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
DOMAIN_PACK_ID_RE = re.compile(r"^_template$|^[a-z0-9][a-z0-9-]*$")
DOMAIN_PACK_REQUIRED_FIELDS = (
    "schema_version",
    "id",
    "name",
    "status",
    "purpose",
    "entrypoint",
    "files",
    "optional",
    "core_doctrine_changes",
)
DOMAIN_PACK_STATUSES = ("template", "example", "draft", "active", "retired")
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
ASSISTANT_DRIVER_REGISTRY = "registry/assistant-drivers.json"
ASSISTANT_DRIVER_REQUIRED_FIELDS = (
    "id",
    "display_name",
    "driver_kind",
    "executable_name",
    "supported_invocation_modes",
    "prompt_input_methods",
    "structured_output_support",
    "final_message_capture_support",
    "sandbox_approval_controls",
    "model_selection_support",
    "reasoning_selection_support",
    "fresh_session_behavior",
    "resume_behavior",
    "known_limitations",
    "unsupported_operations",
)
ASSISTANT_DRIVER_KINDS = ("subscription-cli", "api-cli", "external-harness", "manual")
ASSISTANT_DRIVER_PROMPT_INPUT_METHODS = ("argument", "stdin", "prompt_file", "tool_specific_option", "manual")
OUTER_PLAN_SCHEMA = "schemas/outer-loop-plan.schema.json"
OUTER_DRY_RUN_REPORT_SCHEMA = "schemas/outer-loop-dry-run-report.schema.json"
OUTER_GATE_REPORT_SCHEMA = "schemas/outer-loop-gate-report.schema.json"
OUTER_RUN_LEDGER_SCHEMA = "schemas/outer-loop-run-ledger.schema.json"
PORTABLE_RUN_PLAN_SCHEMA = "schemas/portable-operator-run-plan.schema.json"
COMMIT_PLAN_SCHEMA = "schemas/commit-plan.schema.json"
PORTABLE_REHEARSAL_REPORT_SCHEMA = "schemas/portable-operator-rehearsal.schema.json"
OUTER_DEFAULT_PERMISSION_POSTURE = "workspace-write"
OUTER_DEFAULT_COMMIT_POLICY = "none"
OUTER_DEFAULT_TRANSCRIPT_POLICY = {
    "capture": False,
    "mode": "off-by-default",
    "notes": "Do not store raw transcripts unless a later explicit policy authorizes it.",
}
OUTER_REQUIRED_AHL_CHECKS = (
    "python3 scripts/ahl.py promptset lint",
    "python3 scripts/ahl.py doctor",
)
OUTER_STOP_CONDITIONS = (
    "missing_prompt_file",
    "missing_driver_record",
    "driver-failed",
    "missing_validation_commands",
    "missing_stop_conditions",
    "failed_prompt_validation",
    "failed_ahl_check",
    "unsafe_git_state",
    "unexpected_plan_mutation",
    "operator_approval_required",
)
PORTABLE_RUN_RANGE_PHASES = (
    "run",
    "audit_next_readiness_context_update",
    "optional_repair",
    "commit_plan",
    "make_commits_explicit_only",
    "commit_check",
    "fresh_session_boundary",
    "stop_boundary",
)
OUTER_RUN_STOP_GATE_STATUSES = ("blocked", "failed-validation", "driver-failed", "unsafe-git-state")
OUTER_GATE_STATUSES = (
    "pass",
    "pass-with-warnings",
    "blocked",
    "failed-validation",
    "needs-human-review",
    "driver-failed",
    "unsafe-git-state",
)
OUTER_GATE_ALLOWED_AHL_CHECKS = (
    "python3 scripts/ahl.py promptset lint",
    "python3 scripts/ahl.py doctor",
)
OUTER_STEP_COMPLETED_STATUSES = ("completed", "dry-run", "skipped")
OUTER_STEP_FAILED_STATUSES = (
    "blocked",
    "driver-failed",
    "failed-validation",
    "unsafe-git-state",
    "unexpected-plan-mutation",
)
OUTER_RESUME_SAFE_STATUSES = ("interrupted", "driver-timeout", "driver-rate-limit", "user-interrupted")
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
        "name": "domain-pack",
        "command": "python3 scripts/ahl.py domain-pack check",
        "summary": "Validate optional domain pack manifests.",
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
        "name": "driver",
        "command": "python3 scripts/ahl.py driver check",
        "summary": "Validate assistant driver records and safe local probes.",
        "safety": "read-only",
    },
    {
        "name": "outer-plan",
        "command": "python3 scripts/ahl.py outer plan --from PROMPT_33 --count 3 --driver manual",
        "summary": "Create an inspectable sequential outer-loop batch plan.",
        "safety": "writes runs/outer-loop/<plan-id>/plan.json",
    },
    {
        "name": "project-status",
        "command": "python3 scripts/ahl.py project status --json",
        "summary": "Report target project promptset, git, bootstrap, and likely next prompt state.",
        "safety": "read-only",
    },
    {
        "name": "lifecycle-snippets",
        "command": "python3 scripts/ahl.py lifecycle snippets PROMPT_45 --json",
        "summary": "Print reusable one-prompt lifecycle snippets for a target project.",
        "safety": "read-only",
    },
    {
        "name": "lifecycle-context-check",
        "command": "python3 scripts/ahl.py lifecycle context-check PROMPT_45 --json",
        "summary": "Suggest context-update review questions from target-project changed paths.",
        "safety": "read-only",
    },
    {
        "name": "lifecycle-run-range",
        "command": "python3 scripts/ahl.py lifecycle run-range 18 27 --project /path/to/project --dry-run --json",
        "summary": "Dry-run a one-prompt-at-a-time phase plan for a target project prompt range.",
        "safety": "read-only; writes only with explicit --artifact",
    },
    {
        "name": "portable-fixtures",
        "command": "python3 scripts/ahl.py project status --project fixtures/portable-operator/projects/basic --json",
        "summary": "Exercise portable helpers against artificial external-project fixtures.",
        "safety": "read-only",
    },
    {
        "name": "portable-rehearsal",
        "command": "python3 scripts/ahl.py portable rehearsal --json",
        "summary": "Run the deterministic portable-operator end-to-end fixture rehearsal.",
        "safety": "read-only except isolated temporary git fixture commits",
    },
    {
        "name": "outer-dry-run",
        "command": "python3 scripts/ahl.py outer dry-run --plan runs/outer-loop/<plan-id>/plan.json",
        "summary": "Validate a batch plan without invoking assistant CLIs.",
        "safety": "read-only",
    },
    {
        "name": "outer-gate",
        "command": "python3 scripts/ahl.py outer gate PROMPT_36 --json",
        "summary": "Collect post-prompt validation, audit, and readiness gate evidence.",
        "safety": "read-only; records prompt validation commands without executing arbitrary shell",
    },
    {
        "name": "outer-run",
        "command": "python3 scripts/ahl.py outer run --plan runs/outer-loop/<plan-id>/plan.json --dry-run",
        "summary": "Build prompt payloads and, with explicit consent, run sequential assistant CLI steps.",
        "safety": "dry-run by default; live assistant invocation requires --execute",
    },
    {
        "name": "outer-resume",
        "command": "python3 scripts/ahl.py outer resume --run <run-id> --dry-run",
        "summary": "Plan the next prompt to resume from a run ledger.",
        "safety": "read-only; refuses dirty or unsafe worktrees",
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


def script_ahl_home() -> Path:
    return Path(__file__).resolve().parents[1]


def is_valid_ahl_home(path: Path) -> bool:
    return (
        path.is_dir()
        and (path / "AGENT.md").is_file()
        and (path / "scripts" / "ahl.py").is_file()
        and (path / "docs").is_dir()
        and (path / "templates").is_dir()
    )


def resolve_ahl_home(environ: dict[str, str] | None = None) -> dict[str, Any]:
    env = environ if environ is not None else os.environ
    override = env.get("AHL_HOME")
    problems: list[str] = []
    if override:
        path = Path(override).expanduser().resolve()
        valid = is_valid_ahl_home(path)
        if not valid:
            problems.append(f"AHL_HOME does not point to a valid AHL checkout: {override}")
        return {
            "path": str(path),
            "source": "AHL_HOME",
            "valid": valid,
            "problems": problems,
        }

    path = script_ahl_home()
    valid = is_valid_ahl_home(path)
    if not valid:
        problems.append(f"script location does not resolve to a valid AHL checkout: {path}")
    return {
        "path": str(path),
        "source": "script",
        "valid": valid,
        "problems": problems,
    }


def nearest_git_root(path: Path) -> tuple[Path | None, bool, str | None]:
    result, problem = run_git(path, ["rev-parse", "--show-toplevel"])
    if problem:
        return None, False, problem
    if result is None:
        return None, False, "git command did not return a result"
    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "not a git repository" in stderr:
            stderr = "not inside a git work tree"
        return None, True, stderr or "not inside a git work tree"
    text = result.stdout.strip()
    if not text:
        return None, True, "git returned an empty work tree path"
    return Path(text).resolve(), True, None


def prompt_files_in(path: Path) -> list[str]:
    if not path.is_dir():
        return []
    return sorted(item.name for item in path.iterdir() if item.is_file() and PROMPT_RE.match(item.name))


def project_locate_data(project_value: str | None = None, environ: dict[str, str] | None = None) -> dict[str, Any]:
    problems: list[str] = []
    warnings: list[str] = []
    ahl_home = resolve_ahl_home(environ)
    problems.extend(ahl_home["problems"])

    requested_path = Path(project_value).expanduser() if project_value else Path.cwd()
    requested_exists = requested_path.exists()
    requested_is_dir = requested_path.is_dir()
    requested_resolved = requested_path.resolve() if requested_exists else requested_path.absolute()
    project_root = requested_resolved
    git_root = None
    git_available = False
    inside_git_work_tree = False
    git_problem = None

    if not requested_exists:
        problems.append(f"project path does not exist: {project_value}")
    elif not requested_is_dir:
        problems.append(f"project path is not a directory: {project_value}")
    else:
        detected_git_root, git_available, git_problem = nearest_git_root(requested_resolved)
        requested_prompt_dir = requested_resolved / ".prompts"
        if requested_prompt_dir.is_dir() and detected_git_root is not None and detected_git_root != requested_resolved:
            project_root = requested_resolved
        elif detected_git_root is not None:
            git_root = str(detected_git_root)
            project_root = detected_git_root
            inside_git_work_tree = True
        elif git_problem:
            warnings.append(git_problem)

    prompt_dir = project_root / ".prompts"
    prompt_files = prompt_files_in(prompt_dir)
    prompt_dir_exists = prompt_dir.is_dir()
    if requested_exists and requested_is_dir and not prompt_dir_exists:
        warnings.append("project root does not contain .prompts/")

    data = {
        "ok": not problems,
        "ahl_home": ahl_home,
        "project": {
            "requested": str(requested_path),
            "requested_exists": requested_exists,
            "requested_is_dir": requested_is_dir,
            "root": str(project_root),
            "source": "git-root" if inside_git_work_tree else "path",
            "git": {
                "available": git_available,
                "inside_work_tree": inside_git_work_tree,
                "root": git_root,
            },
            "prompt_dir": str(prompt_dir),
            "prompt_dir_exists": prompt_dir_exists,
            "prompt_count": len(prompt_files),
            "prompt_files": prompt_files,
        },
        "warnings": warnings,
        "problems": problems,
    }
    return data


def git_status_summary(root: Path, inside_work_tree: bool) -> dict[str, Any]:
    summary = {
        "available": False,
        "inside_work_tree": inside_work_tree,
        "found": inside_work_tree,
        "dot_git_exists": (root / ".git").is_dir(),
        "root": None,
        "branch": None,
        "dirty_count": 0,
        "untracked_count": 0,
        "status_lines": [],
        "problems": [],
    }
    if not inside_work_tree:
        return summary

    summary["available"] = True
    root_result, root_problem = run_git(root, ["rev-parse", "--show-toplevel"])
    if root_problem:
        summary["problems"].append(root_problem)
        summary["available"] = False
    elif root_result is not None and root_result.returncode == 0:
        summary["root"] = root_result.stdout.strip() or None

    branch_result, branch_problem = run_git(root, ["branch", "--show-current"])
    if branch_problem:
        summary["problems"].append(branch_problem)
        summary["available"] = False
    elif branch_result is not None and branch_result.returncode == 0:
        summary["branch"] = branch_result.stdout.strip() or None

    status_result, status_problem = run_git(root, ["status", "--short", "--untracked-files=all"])
    if status_problem:
        summary["problems"].append(status_problem)
        summary["available"] = False
    elif status_result is not None and status_result.returncode == 0:
        lines = [line for line in status_result.stdout.splitlines() if line.strip()]
        summary["status_lines"] = lines
        summary["untracked_count"] = sum(1 for line in lines if line.startswith("??"))
        summary["dirty_count"] = len(lines) - summary["untracked_count"]
    elif status_result is not None:
        summary["problems"].append(status_result.stderr.strip() or "could not read git status")

    return summary


def prompt_commit_history(root: Path, inside_work_tree: bool, limit: int = 25) -> dict[str, Any]:
    history = {
        "available": False,
        "max_prompt_number": None,
        "next_after_highest_prompt_commit": None,
        "prompt_prefixed_commits": [],
        "problems": [],
    }
    if not inside_work_tree:
        return history

    result, problem = run_git(root, ["log", f"-n{limit}", "--pretty=format:%h%x09%s"])
    if problem:
        history["problems"].append(problem)
        return history
    if result is None:
        history["problems"].append("git log did not return a result")
        return history
    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "does not have any commits yet" in stderr:
            history["available"] = True
            return history
        history["problems"].append(stderr or "could not read git commit history")
        return history

    history["available"] = True
    prompt_numbers: list[int] = []
    commits: list[dict[str, Any]] = []
    for line in result.stdout.splitlines():
        if "\t" in line:
            commit_hash, subject = line.split("\t", 1)
        else:
            commit_hash, subject = "", line
        matches = [int(match) for match in PROMPT_COMMIT_RE.findall(subject)]
        if not matches:
            continue
        prompt_numbers.extend(matches)
        commits.append(
            {
                "hash": commit_hash,
                "subject": subject,
                "prompt_numbers": matches,
            }
        )

    highest_commit = max(prompt_numbers) if prompt_numbers else None
    history["max_prompt_number"] = highest_commit
    history["next_after_highest_prompt_commit"] = f"PROMPT_{highest_commit + 1:02d}" if highest_commit is not None else None
    history["prompt_prefixed_commits"] = commits[:5]
    return history


def promptset_state(prompt_dir_exists: bool, numbering: dict[str, Any]) -> str:
    if not prompt_dir_exists:
        return "missing"
    if not numbering["prompts"]:
        return "empty"
    if numbering["ok"]:
        return "valid-sequential"
    if numbering["duplicates"]:
        return "duplicates"
    if numbering["gaps"]:
        return "gaps"
    if numbering["malformed"]:
        return "malformed"
    return "invalid"


def infer_next_prompt(promptset: dict[str, Any], commit_history: dict[str, Any]) -> dict[str, Any]:
    file_next = promptset["next_after_highest_prompt_file"]
    commit_next = commit_history["next_after_highest_prompt_commit"]
    if file_next and commit_next and file_next == commit_next:
        return {
            "next_after_highest_prompt_file": file_next,
            "prompt_prefixed_commit_summary": commit_history,
            "likely_next_prompt": file_next,
            "confidence": "high",
            "reason": "highest prompt file and prompt-prefixed commit history agree",
        }
    if commit_next and file_next:
        return {
            "next_after_highest_prompt_file": file_next,
            "prompt_prefixed_commit_summary": commit_history,
            "likely_next_prompt": commit_next,
            "confidence": "medium",
            "reason": "prompt files and prompt-prefixed commit history disagree; using commit progress as completed-work evidence",
        }
    if file_next:
        return {
            "next_after_highest_prompt_file": file_next,
            "prompt_prefixed_commit_summary": commit_history,
            "likely_next_prompt": file_next,
            "confidence": "medium",
            "reason": "prompt files exist but no prompt-prefixed commit evidence was found",
        }
    if commit_next:
        return {
            "next_after_highest_prompt_file": file_next,
            "prompt_prefixed_commit_summary": commit_history,
            "likely_next_prompt": commit_next,
            "confidence": "low",
            "reason": "prompt-prefixed commits exist but no prompt files were found",
        }
    return {
        "next_after_highest_prompt_file": file_next,
        "prompt_prefixed_commit_summary": commit_history,
        "likely_next_prompt": None,
        "confidence": "low",
        "reason": "no prompt files or prompt-prefixed commit history found",
    }


def project_status_data(project_value: str | None = None, environ: dict[str, str] | None = None) -> dict[str, Any]:
    locate = project_locate_data(project_value, environ)
    problems = list(locate["problems"])
    warnings = list(locate["warnings"])
    project = dict(locate["project"])
    project_root = Path(project["root"])
    prompt_dir = project_root / ".prompts"
    prompt_dir_exists = prompt_dir.is_dir()
    numbering = promptset_numbering_data(project_root, prompt_dir)
    numbers = numbering["numbers"]
    lowest = min(numbers) if numbers else None
    highest = max(numbers) if numbers else None
    next_after_file = f"PROMPT_{highest + 1:02d}" if highest is not None else None
    state = promptset_state(prompt_dir_exists, numbering)

    if prompt_dir_exists and not numbering["prompts"]:
        warnings.append("project .prompts/ directory is empty")
    for number in numbering["gaps"]:
        warnings.append(f"promptset gap: missing PROMPT_{number:02d}.txt")
    for number in numbering["duplicates"]:
        warnings.append(f"duplicate prompt number: {number:02d}")
    for name in numbering["malformed"]:
        warnings.append(f"malformed prompt filename: {name}")

    git = git_status_summary(project_root, bool(project["git"]["inside_work_tree"]))
    commit_history = prompt_commit_history(project_root, bool(project["git"]["inside_work_tree"]))
    next_prompt = infer_next_prompt(
        {
            "next_after_highest_prompt_file": next_after_file,
        },
        commit_history,
    )

    project.update(
        {
            "git": git,
            "promptset": {
                "prompt_dir": str(prompt_dir),
                "prompt_dir_exists": prompt_dir_exists,
                "prompt_count": len(numbering["prompts"]),
                "state": state,
                "lowest_prompt_number": lowest,
                "highest_prompt_number": highest,
                "gaps": numbering["gaps"],
                "duplicates": numbering["duplicates"],
                "malformed": numbering["malformed"],
                "strict_two_digit": numbering["strict_two_digit"],
                "filenames": numbering["filenames"],
                "numbers": numbers,
            },
            "next_prompt": next_prompt,
            "files": {
                "AGENT.md": (project_root / "AGENT.md").is_file(),
                "CLAUDE.md": (project_root / "CLAUDE.md").is_file(),
                ".context": (project_root / ".context").is_dir(),
                "human-notes.md": (project_root / "human-notes.md").is_file(),
            },
        }
    )

    return {
        "ok": not problems,
        "ahl_home": locate["ahl_home"],
        "project": project,
        "warnings": warnings,
        "problems": problems,
    }


def normalize_bootstrap_choice(value: str | None) -> str:
    if value is None:
        return "auto"
    normalized = value.strip().lower()
    aliases = {
        "auto": "auto",
        "default": "auto",
        "agent": "AGENT.md",
        "agent.md": "AGENT.md",
        "AGENT.md": "AGENT.md",
        "claude": "CLAUDE.md",
        "claude.md": "CLAUDE.md",
        "CLAUDE.md": "CLAUDE.md",
        "none": "none",
        "no": "none",
    }
    if normalized in aliases:
        return aliases[normalized]
    raise SystemExit(f"invalid bootstrap selection: {value}")


def selected_bootstrap_doc(project_root: Path, choice: str) -> str | None:
    if choice == "none":
        return None
    if choice in ("AGENT.md", "CLAUDE.md"):
        return choice
    if (project_root / "AGENT.md").is_file():
        return "AGENT.md"
    return None


def lifecycle_update_targets(bootstrap_doc: str | None, include_context: bool) -> str:
    targets: list[str] = []
    if bootstrap_doc:
        targets.append(bootstrap_doc)
    if include_context:
        targets.append(".context/")
    if not targets:
        return "bootstrap/context files"
    if len(targets) == 1:
        return targets[0]
    return " or ".join(targets)


def lifecycle_snippet_text(prompt_id: str, bootstrap_doc: str | None, include_context: bool, include_repair: bool) -> dict[str, str]:
    number = prompt_id_to_number(prompt_id)
    next_prompt_id = prompt_number_to_id(number + 1)
    prompt_path = f".prompts/{prompt_id}.txt"
    update_targets = lifecycle_update_targets(bootstrap_doc, include_context)
    run_prefix = f"Load {bootstrap_doc}, then run" if bootstrap_doc else "Run"
    snippets = {
        "run": f"{run_prefix} {prompt_path}",
        "audit_next_readiness_context_update": (
            f"Does everything look appropriately implemented for {prompt_id}? Do not run\n"
            f"{next_prompt_id}, but look at it to make sure it is setup for success. Also check\n"
            f"whether {update_targets} should be updated to reflect anything introduced\n"
            f"(or changed) by this prompt. Do not update them just because they ran."
        ),
        "commit_plan": (
            "Suggest grouped Tim Pope style multi-line commits for the changes (grouping\n"
            "hunks appropriately with `git add -p` if needed). The commits should be easy\n"
            "to review, use heredoc EOF so no \\n end up in the commit string, be prefixed\n"
            f"with [{prompt_id}], and should not have a co-author section"
        ),
        "make_commits": "Make the commits",
        "commit_check": (
            f"Run `python3 scripts/ahl.py commit check --project <path> --prompt {prompt_id} --json`,\n"
            "or inspect the just-created commits manually and verify:\n"
            "- Tim Pope-style subject/body formatting;\n"
            "- wrapped secondary/body lines;\n"
            "- no literal `\\n` sequences;\n"
            "- no co-author trailer;\n"
            f"- prefix such as `[{prompt_id}]` is present;\n"
            "- commit grouping matches the implemented changes;\n"
            "- amend or rebase guidance is suggested only when there is a clear issue."
        ),
    }
    if include_repair:
        snippets["repair"] = (
            f"Repair the specific issue found in {prompt_id}. Keep the scope limited to the\n"
            "reviewed defect, preserve unrelated changes, rerun the relevant validation,\n"
            "and stop without running a later prompt or committing unless explicitly asked."
        )
    return snippets


def lifecycle_snippets_data(
    prompt_value: str,
    project_value: str | None = None,
    bootstrap_value: str | None = None,
    context_value: str = "auto",
    include_repair: bool = False,
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    prompt_id = normalize_prompt_id(prompt_value)
    locate = project_locate_data(project_value, environ)
    problems = list(locate["problems"])
    warnings = list(locate["warnings"])
    project = dict(locate["project"])
    project_root = Path(project["root"])
    bootstrap_choice = normalize_bootstrap_choice(bootstrap_value)
    bootstrap_doc = selected_bootstrap_doc(project_root, bootstrap_choice)
    if bootstrap_choice in ("AGENT.md", "CLAUDE.md") and not (project_root / bootstrap_choice).is_file():
        warnings.append(f"requested bootstrap doc is not present in target project: {bootstrap_choice}")

    if context_value not in ("auto", "include", "omit"):
        raise SystemExit(f"invalid context selection: {context_value}")
    context_detected = (project_root / ".context").is_dir()
    include_context = context_value == "include" or (
        context_value == "auto" and (context_detected or bootstrap_doc == "AGENT.md")
    )
    prompt_path = project_root / ".prompts" / f"{prompt_id}.txt"
    if project["requested_exists"] and project["requested_is_dir"] and not prompt_path.is_file():
        warnings.append(f"target prompt file is not present: .prompts/{prompt_id}.txt")

    snippets = lifecycle_snippet_text(prompt_id, bootstrap_doc, include_context, include_repair)
    return {
        "ok": not problems,
        "ahl_home": locate["ahl_home"],
        "project": {
            "requested": project["requested"],
            "root": project["root"],
            "source": project["source"],
            "prompt_dir": project["prompt_dir"],
            "prompt_dir_exists": project["prompt_dir_exists"],
        },
        "prompt": {
            "input": prompt_value,
            "id": prompt_id,
            "number": prompt_id_to_number(prompt_id),
            "path": f".prompts/{prompt_id}.txt",
            "exists": prompt_path.is_file(),
        },
        "configuration": {
            "bootstrap": bootstrap_choice,
            "bootstrap_doc": bootstrap_doc,
            "context": context_value,
            "context_detected": context_detected,
            "context_mentioned": include_context,
            "repair_included": include_repair,
        },
        "snippets": snippets,
        "warnings": warnings,
        "problems": problems,
    }


def context_change_kind(path: str) -> str:
    if path in BOOTSTRAP_CONTEXT_FILES:
        return "bootstrap"
    if path == "human-notes.md":
        return "operator-notes"
    if path == "README.md" or path == "Makefile":
        return "repo-navigation"
    if path == "scripts/ahl.py" or path.startswith("scripts/"):
        return "command-surface"
    if path.startswith("docs/"):
        return "durable-docs"
    if path.startswith("runbooks/"):
        return "workflow"
    if path.startswith("prompt-templates/") or path.startswith("templates/"):
        return "template"
    if path.startswith(".prompts/"):
        return "prompt"
    first = path.split("/", 1)[0]
    if first in CONTEXT_ROOTS:
        return "context-file"
    if path.startswith("tests/"):
        return "test"
    if path.startswith("fixtures/") or path.startswith("dry-runs/expected/"):
        return "fixture"
    if path.startswith("runs/") or path.startswith("tmp/") or path.startswith(".runtime/") or path.startswith(".session/"):
        return "transient"
    return "ordinary"


def context_candidate_for_path(path: str) -> dict[str, Any] | None:
    kind = context_change_kind(path)
    if kind in ("operator-notes", "test", "fixture", "transient", "ordinary"):
        return None
    if kind == "context-file":
        return {
            "path": path,
            "kind": kind,
            "confidence": "review",
            "reason": "context or bootstrap-adjacent file changed; verify the edit was intentional and concise",
            "questions": [
                "Does this context edit reflect durable workflow, architecture, command, convention, or navigation knowledge?",
                "Can the same broad guidance live better in checked-in docs or templates?",
            ],
        }
    if kind == "prompt":
        return {
            "path": path,
            "kind": kind,
            "confidence": "low",
            "reason": "prompt text changed; only context-relevant doctrine or workflow changes may justify context updates",
            "questions": [
                "Did the prompt introduce a reusable rule future fresh sessions need before reading the prompt itself?",
            ],
        }
    return {
        "path": path,
        "kind": kind,
        "confidence": "medium",
        "reason": "changed path often carries durable workflow, command, convention, or navigation knowledge",
        "questions": [
            "Should AGENT.md, CLAUDE.md, .context/, or context/ mention this durable change for future fresh sessions?",
            "Would updating a checked-in doc or template be clearer than editing a context file?",
        ],
    }


def lifecycle_context_check_data(
    prompt_value: str,
    project_value: str | None = None,
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    prompt_id = normalize_prompt_id(prompt_value)
    locate = project_locate_data(project_value, environ)
    problems = list(locate["problems"])
    warnings = list(locate["warnings"])
    project = dict(locate["project"])
    project_root = Path(project["root"])
    prompt_path = project_root / ".prompts" / f"{prompt_id}.txt"
    if project["requested_exists"] and project["requested_is_dir"] and not prompt_path.is_file():
        warnings.append(f"target prompt file is not present: .prompts/{prompt_id}.txt")

    git = git_status_summary(project_root, bool(project["git"]["inside_work_tree"]))
    if not git["inside_work_tree"]:
        warnings.append("target project is not inside a git work tree; changed paths cannot be inferred")
    changed_paths = changed_paths_from_status(git["status_lines"])
    candidates: list[dict[str, Any]] = []
    ignored_changes: list[dict[str, str]] = []
    for path in changed_paths:
        candidate = context_candidate_for_path(path)
        if candidate:
            candidates.append(candidate)
        else:
            ignored_changes.append({"path": path, "kind": context_change_kind(path)})

    questions: list[str] = []
    for candidate in candidates:
        for question in candidate["questions"]:
            if question not in questions:
                questions.append(question)

    conclusion = (
        "review context update candidates"
        if candidates
        else "no context update candidates detected; record no context update needed in the audit if that matches review"
    )

    return {
        "ok": not problems and not git["problems"],
        "ahl_home": locate["ahl_home"],
        "project": {
            "requested": project["requested"],
            "root": project["root"],
            "source": project["source"],
            "prompt_dir": project["prompt_dir"],
            "prompt_dir_exists": project["prompt_dir_exists"],
        },
        "prompt": {
            "input": prompt_value,
            "id": prompt_id,
            "number": prompt_id_to_number(prompt_id),
            "path": f".prompts/{prompt_id}.txt",
            "exists": prompt_path.is_file(),
        },
        "git": git,
        "changed_paths": changed_paths,
        "candidates": candidates,
        "ignored_changes": ignored_changes,
        "questions": questions,
        "conclusion": conclusion,
        "read_only": True,
        "warnings": warnings,
        "problems": problems + git["problems"],
    }


def portable_run_range_plan_id(start: int, end: int) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"portable-run-range-{prompt_number_to_id(start)}-{prompt_number_to_id(end)}-{stamp}".lower()


def portable_run_range_requested(start_value: str, end_value: str) -> tuple[int | None, int | None, dict[str, Any], list[str]]:
    problems: list[str] = []
    requested = {"start": start_value, "end": end_value}
    start_number: int | None = None
    end_number: int | None = None
    try:
        start_number = prompt_id_to_number(normalize_prompt_id(start_value))
    except SystemExit as exc:
        problems.append(str(exc))
    try:
        end_number = prompt_id_to_number(normalize_prompt_id(end_value))
    except SystemExit as exc:
        problems.append(str(exc))
    if start_number is not None and end_number is not None and start_number > end_number:
        problems.append("requested prompt range is reversed; start must be less than or equal to end")
    if start_number is not None:
        requested["start_prompt_id"] = prompt_number_to_id(start_number)
    if end_number is not None:
        requested["end_prompt_id"] = prompt_number_to_id(end_number)
    return start_number, end_number, requested, problems


def portable_run_range_phase_records(prompt_id: str, snippets: dict[str, str]) -> list[dict[str, Any]]:
    next_prompt_id = prompt_number_to_id(prompt_id_to_number(prompt_id) + 1)
    return [
        {
            "name": "run",
            "order": 1,
            "snippet_key": "run",
            "snippet": snippets["run"],
            "boundary": "start this prompt in a fresh assistant session",
        },
        {
            "name": "audit_next_readiness_context_update",
            "order": 2,
            "snippet_key": "audit_next_readiness_context_update",
            "snippet": snippets["audit_next_readiness_context_update"],
            "boundary": "audit the completed prompt before any commit planning or next prompt",
        },
        {
            "name": "optional_repair",
            "order": 3,
            "snippet_key": "repair",
            "snippet": snippets["repair"],
            "boundary": "use only for a bounded defect found during audit; otherwise skip",
            "optional": True,
        },
        {
            "name": "commit_plan",
            "order": 4,
            "snippet_key": "commit_plan",
            "snippet": snippets["commit_plan"],
            "boundary": "plan commits only after implementation and validation review",
        },
        {
            "name": "make_commits_explicit_only",
            "order": 5,
            "snippet_key": "make_commits",
            "snippet": snippets["make_commits"],
            "boundary": "make commits only after explicit operator approval",
            "requires_explicit_operator_approval": True,
        },
        {
            "name": "commit_check",
            "order": 6,
            "snippet_key": "commit_check",
            "snippet": snippets["commit_check"],
            "boundary": "inspect prompt-prefixed commits after commits exist",
        },
        {
            "name": "fresh_session_boundary",
            "order": 7,
            "boundary": f"stop this assistant session before {next_prompt_id}; start the next prompt in a fresh session",
        },
        {
            "name": "stop_boundary",
            "order": 8,
            "boundary": "do not automatically continue after validation, audit, repair, commit, or readiness failure",
        },
    ]


def lifecycle_run_range_data(
    start_value: str,
    end_value: str,
    project_value: str | None = None,
    bootstrap_value: str | None = None,
    artifact_value: str | None = None,
    plan_id_value: str | None = None,
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    locate = project_locate_data(project_value, environ)
    problems = list(locate["problems"])
    warnings = list(locate["warnings"])
    project = dict(locate["project"])
    project_root = Path(project["root"])
    prompt_dir = project_root / ".prompts"
    start_number, end_number, requested, range_problems = portable_run_range_requested(start_value, end_value)
    problems.extend(range_problems)

    numbering = promptset_numbering_data(project_root, prompt_dir)
    for name in numbering["malformed"]:
        problems.append(f"malformed prompt filename in target project: {name}")
    for number in numbering["duplicates"]:
        problems.append(f"duplicate prompt number in target project: {number:02d}")

    selected_numbers: list[int] = []
    if start_number is not None and end_number is not None and start_number <= end_number:
        selected_numbers = list(range(start_number, end_number + 1))
    prompt_ids = [prompt_number_to_id(number) for number in selected_numbers]

    missing_prompt_ids: list[str] = []
    steps: list[dict[str, Any]] = []
    bootstrap_choice = normalize_bootstrap_choice(bootstrap_value)
    bootstrap_doc = selected_bootstrap_doc(project_root, bootstrap_choice)
    if bootstrap_choice in ("AGENT.md", "CLAUDE.md") and not (project_root / bootstrap_choice).is_file():
        warnings.append(f"requested bootstrap doc is not present in target project: {bootstrap_choice}")
    context_detected = (project_root / ".context").is_dir()
    include_context = context_detected or bootstrap_doc == "AGENT.md"

    for index, number in enumerate(selected_numbers, start=1):
        prompt_id = prompt_number_to_id(number)
        prompt_path = prompt_dir / f"{prompt_id}.txt"
        if not prompt_path.is_file():
            missing_prompt_ids.append(prompt_id)
            problems.append(f"missing prompt file: .prompts/{prompt_id}.txt")
        snippets = lifecycle_snippet_text(prompt_id, bootstrap_doc, include_context, include_repair=True)
        phases = portable_run_range_phase_records(prompt_id, snippets)
        steps.append(
            {
                "prompt_id": prompt_id,
                "number": number,
                "path": f".prompts/{prompt_id}.txt",
                "exists": prompt_path.is_file(),
                "sequence_index": index,
                "phase_order": list(PORTABLE_RUN_RANGE_PHASES),
                "phases": phases,
                "validation_commands": validation_commands_for_prompt(prompt_path),
                "fresh_session_boundary": f"After {prompt_id}, stop and start a fresh assistant session before any later prompt.",
                "next_prompt": prompt_number_to_id(number + 1) if number < (end_number or number) else None,
            }
        )

    if selected_numbers:
        expected = list(range(selected_numbers[0], selected_numbers[-1] + 1))
        if selected_numbers != expected:
            problems.append("resolved prompts are not strictly sequential")

    git = git_status_summary(project_root, bool(project["git"]["inside_work_tree"]))
    safety_notes = [
        "dry-run/read-only plan; no assistant CLI invocation is performed",
        "target project files are not edited unless the operator separately runs a prompt",
        "commits require an explicit later operator approval boundary",
        "human-notes.md is operator-owned and is not parsed or edited",
    ]
    if git["status_lines"]:
        safety_notes.append("target worktree has uncommitted or untracked changes; review before running a prompt")
    if missing_prompt_ids:
        safety_notes.append("requested range has missing prompts; stop before running the range")

    plan_id = plan_id_value or (portable_run_range_plan_id(start_number, end_number) if start_number and end_number else "portable-run-range-invalid")
    artifact = None
    if artifact_value:
        artifact_path = Path(artifact_value).expanduser()
        if not artifact_path.is_absolute():
            artifact_path = Path(locate["ahl_home"]["path"]) / artifact_path
        artifact = str(artifact_path)

    next_prompt = prompt_ids[0] if prompt_ids and not missing_prompt_ids and not problems else None
    stop_reason = None if not problems else "range-validation-failed"
    return {
        "ok": not problems,
        "schema": PORTABLE_RUN_PLAN_SCHEMA,
        "plan_id": plan_id,
        "created_at": utc_timestamp(),
        "mode": "dry-run",
        "dry_run": True,
        "read_only": True,
        "project": {
            "requested": project["requested"],
            "root": project["root"],
            "source": project["source"],
            "prompt_dir": project["prompt_dir"],
            "prompt_dir_exists": project["prompt_dir_exists"],
            "git": git,
        },
        "configuration": {
            "bootstrap": bootstrap_choice,
            "bootstrap_doc": bootstrap_doc,
            "context_detected": context_detected,
            "context_mentioned": include_context,
            "assistant_invocation": "disabled",
            "artifact_requested": bool(artifact_value),
        },
        "requested_range": requested,
        "prompt_ids": prompt_ids,
        "missing_prompt_ids": missing_prompt_ids,
        "malformed_prompt_filenames": numbering["malformed"],
        "steps": steps,
        "planned_artifact": artifact,
        "next_prompt": next_prompt,
        "stop_reason": stop_reason,
        "restart_state": {
            "project_root": project["root"],
            "prompt_ids": prompt_ids,
            "next_prompt": next_prompt,
            "planned_artifact": artifact,
            "stop_reason": stop_reason,
        },
        "safety_notes": safety_notes,
        "warnings": warnings + git["problems"],
        "problems": problems,
    }


def command_lifecycle(args: argparse.Namespace) -> int:
    if args.action == "run-range":
        data = lifecycle_run_range_data(
            args.start_prompt,
            args.end_prompt,
            project_value=args.project,
            bootstrap_value=args.bootstrap,
            artifact_value=args.artifact,
            plan_id_value=args.plan_id,
        )
        if args.artifact and data["ok"]:
            artifact_path = Path(data["planned_artifact"])
            if artifact_path.exists() and not args.force:
                data["ok"] = False
                data["problems"].append(f"refusing to overwrite existing run-range artifact: {artifact_path}")
            else:
                artifact_path.parent.mkdir(parents=True, exist_ok=True)
                artifact_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                data["artifact"] = str(artifact_path)
        human = [
            "lifecycle run-range: ok" if data["ok"] else "lifecycle run-range: problems found",
            f"- project root: {data['project']['root']}",
            f"- prompts: {', '.join(data['prompt_ids']) if data['prompt_ids'] else 'none'}",
            f"- mode: {data['mode']}",
            f"- next prompt: {data['next_prompt'] or 'none'}",
        ]
        if data.get("artifact"):
            human.append(f"- artifact: {data['artifact']}")
        human.extend(f"- warning: {warning}" for warning in data["warnings"])
        human.extend(f"- problem: {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)

    if args.action == "context-check":
        data = lifecycle_context_check_data(args.prompt, project_value=args.project)
        human = [
            f"lifecycle context-check: {data['prompt']['id']}",
            f"- project root: {data['project']['root']}",
            f"- changed paths: {len(data['changed_paths'])}",
            f"- candidates: {len(data['candidates'])}",
            f"- conclusion: {data['conclusion']}",
        ]
        for candidate in data["candidates"]:
            human.append(f"- candidate: {candidate['path']} ({candidate['kind']}, {candidate['confidence']})")
        human.extend(f"- warning: {warning}" for warning in data["warnings"])
        human.extend(f"- problem: {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)

    context_value = "include" if args.context else "auto"
    if args.no_context:
        context_value = "omit"
    data = lifecycle_snippets_data(
        args.prompt,
        project_value=args.project,
        bootstrap_value=args.bootstrap,
        context_value=context_value,
        include_repair=args.include_repair,
    )
    human = [
        f"lifecycle snippets: {data['prompt']['id']}",
        f"- project root: {data['project']['root']}",
        f"- bootstrap: {data['configuration']['bootstrap_doc'] or 'none'}",
        f"- context mentioned: {data['configuration']['context_mentioned']}",
        "",
    ]
    labels = {
        "run": "Run",
        "audit_next_readiness_context_update": "Audit / Next Readiness / Context Update",
        "commit_plan": "Commit Plan",
        "make_commits": "Make Commits",
        "commit_check": "Commit Check",
        "repair": "Repair",
    }
    for key, text in data["snippets"].items():
        human.extend([f"## {labels.get(key, key)}", "", text, ""])
    human.extend(f"- warning: {warning}" for warning in data["warnings"])
    human.extend(f"- problem: {problem}" for problem in data["problems"])
    return emit(data, args.json, human, 0 if data["ok"] else 1)


def command_project(args: argparse.Namespace) -> int:
    if args.action == "status":
        data = project_status_data(args.project)
        promptset = data["project"]["promptset"]
        git = data["project"]["git"]
        inference = data["project"]["next_prompt"]
        human = ["project status: ok" if data["ok"] else "project status: problems found"]
        human.extend(
            [
                f"- AHL home: {data['ahl_home']['path']} ({data['ahl_home']['source']})",
                f"- project root: {data['project']['root']}",
                f"- git: {'present' if git['found'] else 'not found'}"
                + (f", branch {git['branch']}" if git.get("branch") else ""),
                f"- .prompts: {promptset['state']} ({promptset['prompt_count']} prompts)",
                f"- prompt range: {promptset['lowest_prompt_number']}..{promptset['highest_prompt_number']}",
                f"- likely next prompt: {inference['likely_next_prompt'] or 'unknown'}"
                f" ({inference['confidence']}; {inference['reason']})",
            ]
        )
        human.extend(f"- warning: {warning}" for warning in data["warnings"])
        human.extend(f"- problem: {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)

    data = project_locate_data(args.project)
    human = ["project locate: ok" if data["ok"] else "project locate: problems found"]
    human.extend(
        [
            f"- AHL home: {data['ahl_home']['path']} ({data['ahl_home']['source']})",
            f"- project root: {data['project']['root']}",
            f"- .prompts: {'present' if data['project']['prompt_dir_exists'] else 'missing'}",
        ]
    )
    human.extend(f"- warning: {warning}" for warning in data["warnings"])
    return emit(data, args.json, human, 0 if data["ok"] else 1)


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


def read_gitignore_patterns(root: Path) -> list[str]:
    path = root / ".gitignore"
    if not path.exists():
        return []
    patterns: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            patterns.append(stripped)
    return patterns


def is_ignored_by_patterns(relative_path: str, patterns: list[str]) -> bool:
    ignored = False
    normalized = relative_path.replace("\\", "/").lstrip("/")
    basename = normalized.rsplit("/", 1)[-1]
    for raw_pattern in patterns:
        negated = raw_pattern.startswith("!")
        pattern = raw_pattern[1:] if negated else raw_pattern
        pattern = pattern.strip().lstrip("/")
        if not pattern:
            continue
        directory_pattern = pattern.endswith("/")
        comparable = pattern.rstrip("/")
        matched = False
        if directory_pattern:
            matched = normalized == comparable or normalized.startswith(f"{comparable}/")
        elif "/" in comparable:
            matched = fnmatch.fnmatch(normalized, comparable)
        else:
            matched = fnmatch.fnmatch(basename, comparable) or fnmatch.fnmatch(normalized, comparable)
        if matched:
            ignored = not negated
    return ignored


def required_ignore_present(pattern: str, patterns: list[str]) -> bool:
    normalized_required = pattern.rstrip("/")
    return any(item.rstrip("/") == normalized_required for item in patterns if not item.startswith("!"))


def git_status_paths(root: Path) -> list[dict[str, str]]:
    result, problem = run_git(root, ["status", "--short", "--untracked-files=all"])
    if problem or result is None or result.returncode != 0:
        return []
    entries: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        status = line[:2]
        path = line[3:] if len(line) > 3 else line.strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        entries.append({"status": status, "path": path})
    return entries


def path_has_secret_name(relative_path: str) -> bool:
    parts = [part for part in relative_path.replace("\\", "/").split("/") if part]
    safe_examples = {".env.example", "env.example", "example.env"}
    return any(
        fnmatch.fnmatch(part.lower(), pattern)
        for part in parts
        if part.lower() not in safe_examples
        for pattern in SECRET_NAME_PATTERNS
    )


def unignored_files(root: Path, patterns: list[str]) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        directory = Path(dirpath)
        relative_dir = directory.relative_to(root).as_posix() if directory != root else ""
        kept_dirs: list[str] = []
        for dirname in dirnames:
            relative = f"{relative_dir}/{dirname}".lstrip("/")
            if dirname == ".git" or is_ignored_by_patterns(f"{relative}/", patterns):
                continue
            kept_dirs.append(dirname)
        dirnames[:] = kept_dirs
        for filename in filenames:
            relative = f"{relative_dir}/{filename}".lstrip("/")
            if not is_ignored_by_patterns(relative, patterns):
                files.append(directory / filename)
    return files


def safety_hygiene_checks(root: Path, ignored: set[str], patterns: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    problems: list[str] = []

    handoff = root / "tmp" / "HANDOFF.md"
    handoff_ok = not handoff.exists()
    checks.append(
        {
            "name": "tmp/HANDOFF.md absent unless actively needed",
            "path": "tmp/HANDOFF.md",
            "required": False,
            "present": handoff.exists(),
            "ok": handoff_ok,
        }
    )
    if not handoff_ok:
        problems.append("tmp/HANDOFF.md is present; confirm it is current or remove it after use")

    for required in REQUIRED_IGNORE_PATTERNS:
        ok = required_ignore_present(required, patterns) or required.rstrip("/") in ignored
        checks.append({"name": f"{required} ignored", "path": ".gitignore", "required": True, "ok": ok})
        if not ok:
            problems.append(f"missing .gitignore entry for {required}")

    for path_text in TRANSCRIPT_DUMP_PATHS:
        path = root / path_text
        present = path.exists()
        ok = not present
        checks.append({"name": f"{path_text} transcript dump absent", "path": path_text, "required": False, "present": present, "ok": ok})
        if present:
            problems.append(f"{path_text}/ exists; do not store raw transcript dumps in the repo")

    for path_text in TRANSCRIPT_DUMP_FILES:
        path = root / path_text
        present = path.exists()
        ok = not present
        checks.append({"name": f"{path_text} transcript dump file absent", "path": path_text, "required": False, "present": present, "ok": ok})
        if present:
            problems.append(f"{path_text} exists; do not store raw transcript dumps in the repo")

    status_entries = git_status_paths(root)
    for entry in status_entries:
        path = entry["path"]
        if path_has_secret_name(path) and entry["status"][0] != " ":
            problems.append(f"secret-looking path is staged, modified, or untracked: {path}")
            checks.append({"name": "secret-looking staged path", "path": path, "required": False, "ok": False})

    for path in unignored_files(root, patterns):
        relative = path.relative_to(root).as_posix()
        if path_has_secret_name(relative):
            checks.append({"name": "secret-looking file ignored", "path": relative, "required": False, "ok": False})
            problems.append(f"secret-looking file is not ignored by .gitignore: {relative}")

    return checks, problems


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
    patterns = read_gitignore_patterns(root)
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

    safety_checks, safety_problems = safety_hygiene_checks(root, ignored, patterns)
    checks.extend(safety_checks)
    problems.extend(safety_problems)

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


def load_assistant_driver_registry(root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    path = root / ASSISTANT_DRIVER_REGISTRY
    if not path.is_file():
        return [], [f"missing assistant driver registry: {ASSISTANT_DRIVER_REGISTRY}"]
    data, problem = load_registry(path)
    if problem:
        return [], [f"{ASSISTANT_DRIVER_REGISTRY}: {problem}"]
    assert data is not None
    drivers: list[dict[str, Any]] = []
    problems: list[str] = []
    for index, item in enumerate(data["items"]):
        item_ref = f"{ASSISTANT_DRIVER_REGISTRY} item {index + 1}"
        if not isinstance(item, dict):
            problems.append(f"{item_ref}: item must be an object")
            continue
        drivers.append(item)
    return drivers, problems


def driver_public_record(driver: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": driver.get("id"),
        "display_name": driver.get("display_name"),
        "driver_kind": driver.get("driver_kind"),
        "executable_name": driver.get("executable_name"),
        "supported_invocation_modes": driver.get("supported_invocation_modes"),
        "prompt_input_methods": driver.get("prompt_input_methods"),
        "status": driver.get("status"),
        "live_run_status": driver.get("live_run_status"),
        "manual_confirmation_required": bool(driver.get("manual_confirmation_required")),
    }


def validate_assistant_driver(driver: dict[str, Any], index: int, root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    item_ref = f"{ASSISTANT_DRIVER_REGISTRY} item {index + 1}"
    driver_id = driver.get("id", f"item-{index + 1}")
    checks: list[dict[str, Any]] = []
    problems: list[str] = []

    missing = [field for field in ASSISTANT_DRIVER_REQUIRED_FIELDS if field not in driver]
    checks.append({"name": f"{driver_id} required fields", "driver_id": driver_id, "ok": not missing})
    if missing:
        problems.append(f"{item_ref}: missing driver fields: {', '.join(missing)}")

    kind = driver.get("driver_kind")
    kind_ok = kind in ASSISTANT_DRIVER_KINDS
    checks.append({"name": f"{driver_id} driver kind", "driver_id": driver_id, "ok": kind_ok})
    if not kind_ok:
        problems.append(f"{item_ref}: driver_kind must be one of {', '.join(ASSISTANT_DRIVER_KINDS)}")

    executable = driver.get("executable_name")
    executable_ok = executable is None or isinstance(executable, str)
    checks.append({"name": f"{driver_id} executable name", "driver_id": driver_id, "ok": executable_ok})
    if not executable_ok:
        problems.append(f"{item_ref}: executable_name must be a string or null")
    if kind != "manual" and not executable:
        problems.append(f"{item_ref}: non-manual drivers must name an executable")

    modes = driver.get("supported_invocation_modes")
    modes_ok = isinstance(modes, list) and all(isinstance(item, str) and item for item in modes)
    checks.append({"name": f"{driver_id} invocation modes", "driver_id": driver_id, "ok": modes_ok})
    if not modes_ok:
        problems.append(f"{item_ref}: supported_invocation_modes must be a list of strings")

    methods = driver.get("prompt_input_methods")
    methods_ok = (
        isinstance(methods, list)
        and bool(methods)
        and all(isinstance(item, str) and item in ASSISTANT_DRIVER_PROMPT_INPUT_METHODS for item in methods)
    )
    checks.append({"name": f"{driver_id} prompt input methods", "driver_id": driver_id, "ok": methods_ok})
    if not methods_ok:
        problems.append(
            f"{item_ref}: prompt_input_methods must use {', '.join(ASSISTANT_DRIVER_PROMPT_INPUT_METHODS)}"
        )

    for field in ("known_limitations", "unsupported_operations"):
        value = driver.get(field)
        ok = isinstance(value, list) and all(isinstance(item, str) and item for item in value)
        checks.append({"name": f"{driver_id} {field}", "driver_id": driver_id, "ok": ok})
        if not ok:
            problems.append(f"{item_ref}: {field} must be a list of strings")

    path_value = driver.get("path")
    if isinstance(path_value, str) and path_value:
        path_ok = (root / path_value).exists()
        checks.append({"name": f"{driver_id} fixture path exists", "driver_id": driver_id, "path": path_value, "ok": path_ok})
        if not path_ok:
            problems.append(f"{item_ref}: referenced path does not exist: {path_value}")

    return checks, problems


def assistant_driver_check_data(root: Path) -> dict[str, Any]:
    drivers, problems = load_assistant_driver_registry(root)
    checks: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, driver in enumerate(drivers):
        driver_id = driver.get("id")
        if not isinstance(driver_id, str) or not driver_id:
            problems.append(f"{ASSISTANT_DRIVER_REGISTRY} item {index + 1}: id must be a non-empty string")
        elif driver_id in seen_ids:
            problems.append(f"{ASSISTANT_DRIVER_REGISTRY} item {index + 1}: duplicate id {driver_id}")
        else:
            seen_ids.add(driver_id)
        item_checks, item_problems = validate_assistant_driver(driver, index, root)
        checks.extend(item_checks)
        problems.extend(item_problems)
    return {
        "ok": not problems,
        "drivers": [driver_public_record(driver) for driver in drivers],
        "checks": checks,
        "problems": problems,
    }


def assistant_driver_list_data(root: Path) -> dict[str, Any]:
    drivers, problems = load_assistant_driver_registry(root)
    return {
        "ok": not problems,
        "drivers": [driver_public_record(driver) for driver in drivers],
        "checks": [],
        "problems": problems,
    }


def assistant_driver_probe_data(root: Path, driver_id: str, help_only: bool) -> dict[str, Any]:
    drivers, load_problems = load_assistant_driver_registry(root)
    selected = next((driver for driver in drivers if driver.get("id") == driver_id), None)
    checks: list[dict[str, Any]] = []
    problems = list(load_problems)
    probe: dict[str, Any] = {"driver_id": driver_id, "help_only": help_only, "executed_help": False}
    if selected is None:
        problems.append(f"unknown assistant driver: {driver_id}")
        return {"ok": False, "drivers": [], "checks": checks, "problems": problems, "probe": probe}

    executable = selected.get("executable_name")
    if executable is None:
        checks.append({"name": "manual driver has no executable", "driver_id": driver_id, "ok": True})
        probe.update({"executable_name": None, "available": None, "path": None})
        return {
            "ok": not problems,
            "drivers": [driver_public_record(selected)],
            "checks": checks,
            "problems": problems,
            "probe": probe,
        }

    executable_path = shutil.which(executable)
    available = executable_path is not None
    checks.append({"name": "executable on PATH", "driver_id": driver_id, "executable": executable, "ok": available})
    probe.update({"executable_name": executable, "available": available, "path": executable_path})
    if not available:
        problems.append(f"{driver_id}: executable not found on PATH: {executable}")
        return {
            "ok": False,
            "drivers": [driver_public_record(selected)],
            "checks": checks,
            "problems": problems,
            "probe": probe,
        }

    if help_only:
        help_args = selected.get("capability_probe", {}).get("help_args", ["--help"])
        if not isinstance(help_args, list) or not all(isinstance(item, str) for item in help_args):
            help_args = ["--help"]
        command = [executable, *help_args]
        try:
            result = subprocess.run(
                command,
                cwd=root,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            problems.append(f"{driver_id}: help probe failed: {exc}")
            checks.append({"name": "help-only command", "driver_id": driver_id, "ok": False})
        else:
            ok = result.returncode == 0
            checks.append({"name": "help-only command", "driver_id": driver_id, "ok": ok, "returncode": result.returncode})
            if not ok:
                problems.append(f"{driver_id}: help probe exited with {result.returncode}")
            probe.update(
                {
                    "executed_help": True,
                    "returncode": result.returncode,
                    "stdout_preview": result.stdout[:400],
                    "stderr_preview": result.stderr[:400],
                }
            )
    return {
        "ok": not problems,
        "drivers": [driver_public_record(selected)],
        "checks": checks,
        "problems": problems,
        "probe": probe,
    }


def command_driver(args: argparse.Namespace) -> int:
    root = repo_root()
    if args.action == "list":
        data = assistant_driver_list_data(root)
        human = ["assistant drivers:"]
        human.extend(f"- {driver['id']}: {driver['driver_kind']} ({driver['executable_name']})" for driver in data["drivers"])
        if not data["drivers"]:
            human.append("- none")
        human.extend(f"- {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)
    if args.action == "check":
        data = assistant_driver_check_data(root)
        human = ["assistant drivers: ok" if data["ok"] else "assistant drivers: problems found"]
        human.extend(f"- {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)

    if not args.driver_id:
        data = {"ok": False, "drivers": [], "checks": [], "problems": ["driver probe requires a driver id"]}
        return emit(data, args.json, ["driver probe requires a driver id"], 1)
    data = assistant_driver_probe_data(root, args.driver_id, args.help_only)
    human = [f"assistant driver probe: {args.driver_id}"]
    human.extend(f"- {problem}" for problem in data["problems"])
    return emit(data, args.json, human, 0 if data["ok"] else 1)


def prompt_id_to_number(prompt_id: str) -> int:
    match = re.fullmatch(r"PROMPT_(\d{2})", prompt_id)
    if not match:
        raise SystemExit(f"invalid prompt id: {prompt_id}")
    return int(match.group(1))


def prompt_number_to_id(number: int) -> str:
    return f"PROMPT_{number:02d}"


def load_assistant_driver_map(root: Path) -> tuple[dict[str, dict[str, Any]], list[str]]:
    drivers, problems = load_assistant_driver_registry(root)
    driver_map: dict[str, dict[str, Any]] = {}
    for driver in drivers:
        driver_id = driver.get("id")
        if isinstance(driver_id, str) and driver_id:
            driver_map[driver_id] = driver
    return driver_map, problems


def available_prompt_numbers(root: Path) -> list[int]:
    data = promptset_numbering_data(root, root / ".prompts")
    return sorted(set(number for number in data["numbers"] if isinstance(number, int)))


def resolve_outer_prompt_range(root: Path, args: argparse.Namespace) -> tuple[list[int], dict[str, Any], list[str]]:
    problems: list[str] = []
    numbers = available_prompt_numbers(root)
    if args.next is not None:
        count = args.next
        requested = {"mode": "next", "count": count}
        if count < 1:
            return [], requested, ["--next must be greater than zero"]
        selected = numbers[:count]
        if len(selected) != count:
            problems.append(f"requested next {count} prompts but only found {len(selected)}")
        if selected:
            expected = list(range(selected[0], selected[0] + len(selected)))
            if selected != expected:
                problems.append("next prompt selection is not strictly sequential")
        return selected, requested, problems

    start_id = normalize_prompt_id(args.from_prompt)
    start = prompt_id_to_number(start_id)
    count = args.count
    requested = {"mode": "explicit", "from": start_id, "count": count}
    if count is None:
        return [], requested, ["--count is required with --from"]
    if count < 1:
        return [], requested, ["--count must be greater than zero"]
    selected = list(range(start, start + count))
    return selected, requested, problems


def validation_commands_for_prompt(path: Path) -> list[str]:
    if not path.is_file():
        return []
    commands: list[str] = []
    in_validation = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            in_validation = line.lower().startswith("## validation")
            continue
        if not in_validation:
            continue
        candidate = line.lstrip("-").strip().strip("`")
        if candidate.startswith(("python3 ", "make ", "./scripts/", "scripts/")):
            commands.append(candidate)
    return commands or ["python3 -m unittest tests/test_ahl.py"]


def utc_timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def outer_plan_id(numbers: list[int], driver_id: str) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if numbers:
        span = f"{prompt_number_to_id(numbers[0])}-{prompt_number_to_id(numbers[-1])}"
    else:
        span = "empty"
    return f"outer-{span}-{driver_id}-{stamp}".lower()


def create_outer_plan_data(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    numbers, requested, problems = resolve_outer_prompt_range(root, args)
    driver_map, driver_problems = load_assistant_driver_map(root)
    problems.extend(driver_problems)
    driver = driver_map.get(args.driver)
    if driver is None:
        problems.append(f"unknown assistant driver: {args.driver}")

    prompts: list[dict[str, Any]] = []
    seen: set[int] = set()
    for number in numbers:
        prompt_id = prompt_number_to_id(number)
        path = root / ".prompts" / f"{prompt_id}.txt"
        rel_path = f".prompts/{prompt_id}.txt"
        if number in seen:
            problems.append(f"duplicate prompt in requested range: {prompt_id}")
        seen.add(number)
        if not path.is_file():
            problems.append(f"missing prompt file: {rel_path}")
        prompts.append(
            {
                "prompt_id": prompt_id,
                "path": rel_path,
                "validation_commands": validation_commands_for_prompt(path),
            }
        )

    if numbers:
        expected = list(range(numbers[0], numbers[-1] + 1))
        if numbers != expected:
            problems.append("resolved prompts are not strictly sequential")

    plan_id = args.plan_id or outer_plan_id(numbers, args.driver)
    run_artifact_dir = f"runs/outer-loop/{plan_id}"
    return {
        "ok": not problems,
        "plan_id": plan_id,
        "created_at": utc_timestamp(),
        "requested_range": requested,
        "prompts": prompts,
        "driver": {
            "id": args.driver,
            "display_name": driver.get("display_name") if driver else None,
            "driver_kind": driver.get("driver_kind") if driver else None,
        },
        "model": args.model,
        "reasoning": args.reasoning,
        "permission_posture": args.permission_posture,
        "required_ahl_checks": list(OUTER_REQUIRED_AHL_CHECKS),
        "stop_conditions": list(OUTER_STOP_CONDITIONS),
        "commit_policy": args.commit_policy,
        "transcript_capture_policy": dict(OUTER_DEFAULT_TRANSCRIPT_POLICY),
        "run_artifact_dir": run_artifact_dir,
        "schema": OUTER_PLAN_SCHEMA,
        "problems": problems,
    }


def command_outer_plan(args: argparse.Namespace) -> int:
    root = repo_root()
    data = create_outer_plan_data(root, args)
    if not data["ok"]:
        human = ["outer plan: problems found"]
        human.extend(f"- {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 1)

    out_dir = root / data["run_artifact_dir"]
    plan_path = out_dir / "plan.json"
    if plan_path.exists():
        data["ok"] = False
        data["problems"].append(f"refusing to overwrite existing plan artifact: {plan_path.relative_to(root)}")
        return emit(data, args.json, ["outer plan: refusing to overwrite existing plan artifact"], 1)
    out_dir.mkdir(parents=True, exist_ok=False)
    plan_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    data["artifact"] = str(plan_path.relative_to(root))
    human = [
        f"outer plan: {data['plan_id']}",
        f"- prompts: {len(data['prompts'])}",
        f"- driver: {data['driver']['id']}",
        f"- artifact: {data['artifact']}",
    ]
    return emit(data, args.json, human, 0)


def load_outer_plan(root: Path, plan_value: str) -> tuple[dict[str, Any] | None, str | None]:
    path = (root / plan_value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None, f"plan path escapes repository root: {plan_value}"
    if not path.is_file():
        return None, f"missing plan artifact: {plan_value}"
    data, problem = load_json_file(path)
    if problem:
        return None, problem
    if not isinstance(data, dict):
        return None, f"{plan_value}: top-level value must be an object"
    return data, None


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_relative_path(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))


def outer_plan_path(root: Path, plan_value: str) -> tuple[Path | None, str | None]:
    path = (root / plan_value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None, f"plan path escapes repository root: {plan_value}"
    if not path.is_file():
        return None, f"missing plan artifact: {plan_value}"
    return path, None


def outer_dry_run_report(root: Path, plan_value: str) -> dict[str, Any]:
    plan, problem = load_outer_plan(root, plan_value)
    if problem:
        return {"ok": False, "plan_id": None, "steps": [], "problems": [problem]}
    assert plan is not None

    problems: list[str] = []
    driver_map, driver_problems = load_assistant_driver_map(root)
    problems.extend(driver_problems)
    driver_id = plan.get("driver", {}).get("id") if isinstance(plan.get("driver"), dict) else None
    if not isinstance(driver_id, str) or driver_id not in driver_map:
        problems.append(f"missing driver record: {driver_id}")

    stop_conditions = plan.get("stop_conditions")
    if not isinstance(stop_conditions, list) or not stop_conditions:
        problems.append("plan has no stop conditions")
    required_ahl_checks = plan.get("required_ahl_checks")
    if not isinstance(required_ahl_checks, list) or not required_ahl_checks:
        problems.append("plan has no required AHL checks")

    steps: list[dict[str, Any]] = []
    prompt_items = plan.get("prompts")
    if not isinstance(prompt_items, list) or not prompt_items:
        problems.append("plan has no prompts")
        prompt_items = []

    for item in prompt_items:
        item_problems: list[str] = []
        prompt_id = item.get("prompt_id") if isinstance(item, dict) else None
        path_value = item.get("path") if isinstance(item, dict) else None
        validation_commands = item.get("validation_commands") if isinstance(item, dict) else None
        if not isinstance(prompt_id, str) or not PROMPT_ID_RE.fullmatch(prompt_id):
            item_problems.append(f"invalid prompt id: {prompt_id}")
        if not isinstance(path_value, str) or not path_value:
            item_problems.append("missing prompt path")
        else:
            ok, path_problem = relative_path_exists(root, path_value)
            if not ok and path_problem:
                item_problems.append(path_problem)
        if not isinstance(validation_commands, list) or not validation_commands:
            item_problems.append("missing validation commands")
        status = "fail" if item_problems else "pass"
        steps.append(
            {
                "prompt_id": prompt_id,
                "path": path_value,
                "status": status,
                "validation_commands": validation_commands if isinstance(validation_commands, list) else [],
                "problems": item_problems,
            }
        )
        problems.extend(f"{prompt_id or 'unknown'}: {step_problem}" for step_problem in item_problems)

    return {"ok": not problems, "plan_id": plan.get("plan_id"), "steps": steps, "problems": problems}


def validate_outer_run_plan(root: Path, plan: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    driver_map, driver_problems = load_assistant_driver_map(root)
    problems.extend(driver_problems)
    driver_id = plan.get("driver", {}).get("id") if isinstance(plan.get("driver"), dict) else None
    if not isinstance(driver_id, str) or driver_id not in driver_map:
        problems.append(f"missing driver record: {driver_id}")

    if plan.get("parallel") is True or plan.get("execution_mode") == "parallel":
        problems.append("parallel execution is not supported by outer run")

    prompt_items = plan.get("prompts")
    if not isinstance(prompt_items, list) or not prompt_items:
        problems.append("plan has no prompts")
        return problems

    previous_number: int | None = None
    for index, item in enumerate(prompt_items):
        if not isinstance(item, dict):
            problems.append(f"plan prompt {index + 1}: must be an object")
            continue
        prompt_id = item.get("prompt_id")
        path_value = item.get("path")
        if not isinstance(prompt_id, str) or not PROMPT_ID_RE.fullmatch(prompt_id):
            problems.append(f"plan prompt {index + 1}: invalid prompt id: {prompt_id}")
        else:
            number = prompt_id_to_number(prompt_id)
            if previous_number is not None and number != previous_number + 1:
                problems.append("plan prompts must be strictly sequential")
            previous_number = number
        if not isinstance(path_value, str) or not path_value:
            problems.append(f"{prompt_id or 'unknown'}: missing prompt path")
        else:
            ok, path_problem = relative_path_exists(root, path_value)
            if not ok and path_problem:
                problems.append(f"{prompt_id or 'unknown'}: {path_problem}")
        validation_commands = item.get("validation_commands")
        if not isinstance(validation_commands, list) or not validation_commands:
            problems.append(f"{prompt_id or 'unknown'}: missing validation commands")

    return problems


def build_outer_prompt_payload(plan: dict[str, Any], prompt_item: dict[str, Any]) -> str:
    prompt_id = prompt_item.get("prompt_id", "UNKNOWN")
    prompt_path = prompt_item.get("path", "")
    validation_commands = prompt_item.get("validation_commands")
    if not isinstance(validation_commands, list):
        validation_commands = []
    validation_block = "\n".join(f"- `{command}`" for command in validation_commands) or "- Use the prompt's own validation section."
    return (
        "# Fresh Prompt Execution Payload\n\n"
        f"Run exactly one prompt file: `{prompt_id}` at `{prompt_path}`.\n\n"
        "## First Read\n\n"
        "Read these local files before editing:\n\n"
        "- `AGENT.md`\n"
        "- `README.md`\n"
        "- `docs/guardrails.md`\n"
        f"- `{prompt_path}`\n"
        "- Any docs explicitly named by the active prompt\n\n"
        "Do not paste the whole repository into context. Read only the files needed for this prompt and any hot spots before editing them.\n\n"
        "## Execution Rules\n\n"
        "- Execute only the named prompt file.\n"
        "- Preserve unrelated modified or untracked files.\n"
        "- Do not commit, stage, push, tag, publish, or delete history unless the outer runner or authorized operator explicitly asks.\n"
        "- Do not store raw transcripts, conversation dumps, credentials, or provider secrets.\n"
        "- Keep changes scoped to the prompt's required deliverables and constraints.\n\n"
        "## Validation\n\n"
        "Run required or cheap relevant validation before claiming completion. Expected commands from the plan:\n\n"
        f"{validation_block}\n\n"
        "## Endcap\n\n"
        "- Audit every required deliverable against the prompt.\n"
        "- Inspect the immediate next prompt for readiness.\n"
        "- Create `tmp/HANDOFF.md` only if a real blocker or non-trivial warning remains.\n"
        "- Summarize changed files, validation evidence, residual risks, and next-prompt readiness.\n"
    )


def driver_supports_setting(driver: dict[str, Any], field: str) -> bool:
    value = driver.get(field)
    if isinstance(value, dict):
        status = str(value.get("status", "")).lower()
        return status in {"supported", "manual", "verified"}
    text = str(value or "").lower()
    if "unknown" in text or "requires verification" in text:
        return False
    return any(word in text for word in ("supported", "manual", "verified"))


def assistant_driver_command(driver: dict[str, Any], plan: dict[str, Any], extra_args: list[str]) -> tuple[list[str] | None, list[str]]:
    warnings: list[str] = []
    driver_id = driver.get("id")
    if driver_id == "manual" or driver.get("driver_kind") == "manual":
        return None, warnings
    if driver.get("manual_confirmation_required") or driver.get("live_run_status") == "manual-confirmation-required":
        return None, [f"{driver_id}: live invocation requires manual confirmation because the safe command shape is unverified"]
    if driver_id not in {"codex", "gemini"}:
        return None, [f"live invocation is not implemented for driver: {driver_id}"]
    executable = driver.get("executable_name")
    if not isinstance(executable, str) or not executable:
        return None, [f"{driver_id}: missing executable_name"]
    command = [executable]
    if plan.get("model"):
        if driver_supports_setting(driver, "model_selection_support"):
            command.extend(["--model", str(plan["model"])])
        else:
            warnings.append("model value recorded in plan but not passed because the driver contract does not verify model selection")
    if plan.get("reasoning"):
        if driver_supports_setting(driver, "reasoning_selection_support"):
            command.extend(["--reasoning", str(plan["reasoning"])])
        else:
            warnings.append("reasoning value recorded in plan but not passed because the driver contract does not verify reasoning selection")
    command.extend(extra_args)
    return command, warnings


def run_assistant_driver(command: list[str], payload: str, root: Path, timeout_seconds: int) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            cwd=root,
            input=payload,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "status": "driver-failed", "returncode": None, "failure_reason": "timeout"}
    except OSError as exc:
        return {"ok": False, "status": "driver-failed", "returncode": None, "failure_reason": str(exc)}
    if result.returncode != 0:
        return {"ok": False, "status": "driver-failed", "returncode": result.returncode, "failure_reason": result.stderr.strip() or "driver exited non-zero"}
    return {"ok": True, "status": "completed", "returncode": result.returncode, "failure_reason": None}


def write_outer_step_summary(root: Path, run_dir: Path, step: dict[str, Any]) -> str:
    summary_dir = run_dir / "step-summaries"
    summary_dir.mkdir(parents=True, exist_ok=True)
    path = summary_dir / f"{step['prompt_id']}.md"
    lines = [
        "# Outer Run Step Summary",
        "",
        f"- Prompt id: {step['prompt_id']}",
        f"- Status: {step['status']}",
        f"- Mode: {step['mode']}",
        f"- Driver status: {step['driver']['status']}",
        f"- Gate status: {step.get('gate', {}).get('status', 'not-run')}",
        f"- Payload: {step['payload_artifact']}",
        "",
        "## Notes",
        "",
        step.get("notes") or "No final assistant summary was captured.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return repo_relative_path(root, path)


def ledger_step_rollup(ledger: dict[str, Any]) -> dict[str, Any]:
    steps = ledger.get("steps") if isinstance(ledger.get("steps"), list) else []
    completed: list[str] = []
    failed: list[str] = []
    skipped: list[str] = []
    pending: list[str] = []
    all_prompt_ids: list[str] = []
    for step in steps:
        if not isinstance(step, dict):
            continue
        prompt_id = step.get("prompt_id")
        if not isinstance(prompt_id, str):
            continue
        all_prompt_ids.append(prompt_id)
        status = str(step.get("status", "pending"))
        if status in {"completed", "dry-run"}:
            completed.append(prompt_id)
        elif status == "skipped":
            skipped.append(prompt_id)
        elif status in OUTER_STEP_FAILED_STATUSES:
            failed.append(prompt_id)
        else:
            pending.append(prompt_id)
    return {
        "total": len(all_prompt_ids),
        "completed": completed,
        "failed": failed,
        "skipped": skipped,
        "pending": pending,
    }


def next_prompt_from_ledger(ledger: dict[str, Any], rerun: bool = False) -> str | None:
    pointer = ledger.get("resume_pointer")
    if not rerun and isinstance(pointer, dict):
        prompt_id = pointer.get("next_prompt")
        if isinstance(prompt_id, str) and prompt_id:
            return prompt_id
    steps = ledger.get("steps") if isinstance(ledger.get("steps"), list) else []
    for step in steps:
        if not isinstance(step, dict):
            continue
        prompt_id = step.get("prompt_id")
        if not isinstance(prompt_id, str):
            continue
        status = str(step.get("status", "pending"))
        if rerun or status not in OUTER_STEP_COMPLETED_STATUSES:
            return prompt_id
    return None


def ledger_recovery_recommendation(status: str, next_prompt: str | None) -> str:
    if status == "completed":
        return "Run is complete; do not resume unless an operator explicitly reruns a prompt."
    if status in {"blocked", "failed-validation", "unsafe-git-state", "unexpected-plan-mutation"}:
        return "Repair the recorded blocker before resuming."
    if next_prompt:
        return f"Resume from {next_prompt} after confirming the worktree is clean and the ledger still matches the plan."
    return "Review the ledger manually before resuming."


def outer_run_ledger(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    plan_path, plan_path_problem = outer_plan_path(root, args.plan)
    if plan_path_problem:
        return {"ok": False, "status": "blocked", "run_id": None, "plan_id": None, "mode": "live" if args.execute else "dry-run", "driver": None, "steps": [], "problems": [plan_path_problem]}
    assert plan_path is not None
    plan, plan_problem = load_outer_plan(root, args.plan)
    if plan_problem:
        return {"ok": False, "status": "blocked", "run_id": None, "plan_id": None, "mode": "live" if args.execute else "dry-run", "driver": None, "steps": [], "problems": [plan_problem]}
    assert plan is not None

    problems = validate_outer_run_plan(root, plan)
    if args.max_prompts is not None and args.max_prompts < 1:
        problems.append("--max-prompts must be greater than zero")
    if args.timeout_seconds < 1:
        problems.append("--timeout-seconds must be greater than zero")
    driver_map, driver_problems = load_assistant_driver_map(root)
    problems.extend(driver_problems)
    driver_id = plan.get("driver", {}).get("id") if isinstance(plan.get("driver"), dict) else None
    driver = driver_map.get(driver_id) if isinstance(driver_id, str) else None
    mode = "live" if args.execute else "dry-run"
    run_id = args.run_id or f"{plan.get('plan_id', 'outer-run')}-run-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}".lower()
    plan_hash = file_sha256(plan_path)
    run_dir_value = plan.get("run_artifact_dir") if isinstance(plan.get("run_artifact_dir"), str) else f"runs/outer-loop/{run_id}"
    run_dir = root / run_dir_value
    ledger_path = run_dir / "run-ledger.json"

    ledger: dict[str, Any] = {
        "ok": False,
        "schema": OUTER_RUN_LEDGER_SCHEMA,
        "status": "blocked" if problems else "running",
        "run_id": run_id,
        "plan_id": plan.get("plan_id"),
        "mode": mode,
        "execute": bool(args.execute),
        "dry_run": not args.execute,
        "started_at": utc_timestamp(),
        "ended_at": None,
        "plan_artifact": repo_relative_path(root, plan_path),
        "plan_sha256": plan_hash,
        "driver": {
            "id": driver_id,
            "driver_kind": driver.get("driver_kind") if driver else None,
            "display_name": driver.get("display_name") if driver else None,
        },
        "model": plan.get("model"),
        "reasoning": plan.get("reasoning"),
        "permission_posture": plan.get("permission_posture"),
        "command_metadata": {
            "command": "outer run",
            "driver_args": list(args.driver_arg or []),
            "execute": bool(args.execute),
            "dry_run": not args.execute,
        },
        "validation_results": [],
        "gate_results": [],
        "commit_plan": None,
        "commit_hashes": [],
        "resume_pointer": {"next_prompt": None, "completed_prompts": [], "notes": "Run has not processed any prompt steps yet."},
        "stop_reason": None,
        "recovery_recommendation": None,
        "max_prompts": args.max_prompts,
        "timeout_seconds": args.timeout_seconds,
        "transcript_capture_policy": plan.get("transcript_capture_policy", dict(OUTER_DEFAULT_TRANSCRIPT_POLICY)),
        "steps": [],
        "problems": list(problems),
    }
    if problems:
        ledger["ended_at"] = utc_timestamp()
        return ledger

    run_dir.mkdir(parents=True, exist_ok=True)
    prompt_items = plan.get("prompts", [])
    if args.max_prompts is not None:
        prompt_items = prompt_items[: args.max_prompts]

    payload_dir = run_dir / "payloads"
    payload_dir.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(prompt_items, start=1):
        assert isinstance(item, dict)
        prompt_id = str(item["prompt_id"])
        payload = build_outer_prompt_payload(plan, item)
        payload_path = payload_dir / f"{prompt_id}.md"
        payload_path.write_text(payload, encoding="utf-8")
        step: dict[str, Any] = {
            "index": index,
            "prompt_id": prompt_id,
            "prompt_file": item.get("path"),
            "mode": mode,
            "status": "dry-run" if not args.execute else "running",
            "payload_artifact": repo_relative_path(root, payload_path),
            "validation_commands": item.get("validation_commands", []),
            "driver": {"status": "not-invoked" if not args.execute else "pending", "command": None, "returncode": None, "failure_reason": None},
            "gate": {"status": "not-run"},
            "notes": None,
            "problems": [],
        }

        if args.execute:
            assert driver is not None
            command, command_warnings = assistant_driver_command(driver, plan, args.driver_arg or [])
            step["driver"]["warnings"] = command_warnings
            if command_warnings and command is None:
                step["driver"].update({"status": "driver-failed", "failure_reason": "; ".join(command_warnings)})
                step["status"] = "driver-failed"
                step["problems"].extend(command_warnings)
            elif command is None:
                step["driver"]["status"] = "manual-action-required"
                step["status"] = "manual-action-required"
                step["notes"] = "Manual driver selected; operator must start a fresh assistant session and use the payload artifact."
            else:
                step["driver"]["command"] = command
                driver_result = run_assistant_driver(command, payload, root, args.timeout_seconds)
                step["driver"].update(driver_result)
                step["status"] = "driver-completed" if driver_result["ok"] else "driver-failed"
                if not driver_result["ok"]:
                    step["problems"].append(str(driver_result["failure_reason"]))
        else:
            step["notes"] = "Dry-run only; no assistant CLI was invoked."

        if file_sha256(plan_path) != plan_hash:
            step["status"] = "unexpected-plan-mutation"
            step["problems"].append("plan artifact changed during run")
            ledger["steps"].append(step)
            ledger["problems"].append("unexpected plan mutation")
            ledger["status"] = "unexpected-plan-mutation"
            break

        if step["status"] == "driver-failed":
            ledger["steps"].append(step)
            ledger["problems"].extend(step["problems"])
            ledger["status"] = "driver-failed"
            break

        gate_args = argparse.Namespace(prompt=prompt_id, plan=args.plan, audit_artifact=None)
        gate = outer_gate_report(root, gate_args)
        step["gate"] = {"status": gate["status"], "decision": gate["decision"], "ok": gate["ok"], "problems": gate["problems"], "warnings": gate["warnings"]}
        ledger["gate_results"].append({"prompt_id": prompt_id, "status": gate["status"], "decision": gate["decision"], "ok": gate["ok"]})
        ledger["validation_results"].extend({"prompt_id": prompt_id, **outcome} for outcome in gate.get("validation_outcomes", []))
        if file_sha256(plan_path) != plan_hash:
            step["status"] = "unexpected-plan-mutation"
            step["problems"].append("plan artifact changed during gate evaluation")
            ledger["steps"].append(step)
            ledger["problems"].append("unexpected plan mutation")
            ledger["status"] = "unexpected-plan-mutation"
            break
        if gate["status"] in OUTER_RUN_STOP_GATE_STATUSES:
            step["status"] = gate["status"]
            step["problems"].extend(gate["problems"])
            ledger["problems"].extend(f"{prompt_id}: {problem}" for problem in gate["problems"])
            ledger["status"] = gate["status"]
            step["summary_artifact"] = write_outer_step_summary(root, run_dir, step)
            ledger["steps"].append(step)
            break

        if step["status"] in {"running", "dry-run", "driver-completed"}:
            step["status"] = "completed" if args.execute else "dry-run"
        step["summary_artifact"] = write_outer_step_summary(root, run_dir, step)
        ledger["steps"].append(step)

    if ledger["status"] == "running":
        ledger["status"] = "completed"
    ledger["ended_at"] = utc_timestamp()
    ledger["ok"] = ledger["status"] in {"completed"}
    rollup = ledger_step_rollup(ledger)
    next_prompt = next_prompt_from_ledger(ledger)
    ledger["resume_pointer"] = {
        "next_prompt": next_prompt,
        "completed_prompts": rollup["completed"],
        "failed_prompts": rollup["failed"],
        "skipped_prompts": rollup["skipped"],
        "pending_prompts": rollup["pending"],
        "rerun_required": False,
    }
    ledger["stop_reason"] = None if ledger["status"] == "completed" else ledger["status"]
    ledger["recovery_recommendation"] = ledger_recovery_recommendation(str(ledger["status"]), next_prompt)
    ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ledger["artifact"] = repo_relative_path(root, ledger_path)
    return ledger


def git_status_report(root: Path) -> dict[str, Any]:
    result, problem = run_git(root, ["status", "--short", "--untracked-files=all"])
    if problem:
        return {
            "available": False,
            "ok": False,
            "unsafe": True,
            "lines": [],
            "paths": [],
            "problems": [problem],
        }
    if result is None or result.returncode != 0:
        stderr = result.stderr.strip() if result is not None else ""
        return {
            "available": True,
            "ok": False,
            "unsafe": True,
            "lines": [],
            "paths": [],
            "problems": [stderr or "could not read git status"],
        }

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    conflict_statuses = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}
    unsafe_lines = [line for line in lines if line[:2] in conflict_statuses]
    problems = [f"unmerged git status entry: {line}" for line in unsafe_lines]
    return {
        "available": True,
        "ok": not unsafe_lines,
        "unsafe": bool(unsafe_lines),
        "lines": lines,
        "paths": changed_paths_from_status(lines),
        "problems": problems,
    }


def run_outer_gate_ahl_check(root: Path, command: str) -> dict[str, Any]:
    if command == "python3 scripts/ahl.py promptset lint":
        data = promptset_lint_data(root)
        return {"command": command, "status": "passed" if data["ok"] else "failed", "ok": data["ok"], "problems": data["problems"]}
    if command == "python3 scripts/ahl.py doctor":
        script = root / "scripts" / "ahl.py"
        if not script.is_file():
            return {"command": command, "status": "unavailable", "ok": None, "problems": ["scripts/ahl.py is unavailable"]}
        try:
            result = subprocess.run(
                [sys.executable, str(script), "doctor", "--json"],
                cwd=root,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except OSError as exc:
            return {"command": command, "status": "unavailable", "ok": None, "problems": [f"could not run doctor: {exc}"]}
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            data = {"ok": False, "problems": [result.stderr.strip() or "doctor did not emit JSON"]}
        problems = data.get("problems", [])
        if not isinstance(problems, list):
            problems = []
        return {"command": command, "status": "passed" if result.returncode == 0 else "failed", "ok": result.returncode == 0, "problems": problems}
    return {"command": command, "status": "skipped", "ok": None, "problems": ["not in outer gate AHL check allowlist"]}


def prompt_item_from_plan(plan: dict[str, Any], prompt_id: str) -> tuple[dict[str, Any] | None, bool]:
    prompt_items = plan.get("prompts")
    if not isinstance(prompt_items, list):
        return None, False
    matching_index: int | None = None
    for index, item in enumerate(prompt_items):
        if isinstance(item, dict) and item.get("prompt_id") == prompt_id:
            matching_index = index
            break
    if matching_index is None:
        return None, False
    return prompt_items[matching_index], matching_index == len(prompt_items) - 1


def completion_audit_from_artifact(root: Path, artifact_value: str | None) -> dict[str, Any]:
    if not artifact_value:
        return {
            "status": "missing",
            "artifact": None,
            "semantic_completion_claimed": False,
            "notes": "No explicit completion audit artifact was supplied; structural gate cannot claim semantic completion.",
        }
    path = (root / artifact_value).resolve()
    try:
        rel = path.relative_to(root.resolve())
    except ValueError:
        return {
            "status": "blocked",
            "artifact": artifact_value,
            "semantic_completion_claimed": False,
            "notes": "Completion audit artifact path escapes the repository.",
        }
    if not path.is_file():
        return {
            "status": "missing",
            "artifact": str(rel),
            "semantic_completion_claimed": False,
            "notes": "Completion audit artifact was supplied but does not exist.",
        }
    return {
        "status": "present",
        "artifact": str(rel),
        "semantic_completion_claimed": False,
        "notes": "Audit artifact exists; reviewers still own semantic judgment.",
    }


def outer_gate_report(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    prompt_id = normalize_prompt_id(args.prompt)
    prompt_number = prompt_id_to_number(prompt_id)
    prompt_path = root / ".prompts" / f"{prompt_id}.txt"
    plan: dict[str, Any] | None = None
    plan_problem: str | None = None
    plan_prompt: dict[str, Any] | None = None
    final_prompt_in_plan = False
    problems: list[str] = []
    warnings: list[str] = []

    if args.plan:
        plan, plan_problem = load_outer_plan(root, args.plan)
        if plan_problem:
            problems.append(plan_problem)
        elif plan is not None:
            plan_prompt, final_prompt_in_plan = prompt_item_from_plan(plan, prompt_id)
            if plan_prompt is None:
                problems.append(f"prompt {prompt_id} is not present in supplied plan")

    git = git_status_report(root)
    problems.extend(git["problems"])

    prompt_exists = prompt_path.is_file()
    if not prompt_exists:
        problems.append(f"missing prompt file: .prompts/{prompt_id}.txt")

    next_prompt_id = prompt_number_to_id(prompt_number + 1)
    next_prompt_path = root / ".prompts" / f"{next_prompt_id}.txt"
    next_required = not final_prompt_in_plan
    next_exists = next_prompt_path.is_file()
    next_blockers: list[str] = []
    if next_required and not next_exists:
        next_blockers.append(f"missing next prompt file: .prompts/{next_prompt_id}.txt")
        problems.extend(next_blockers)

    if plan_prompt and isinstance(plan_prompt.get("validation_commands"), list):
        validation_commands = [item for item in plan_prompt["validation_commands"] if isinstance(item, str)]
        validation_source = "plan"
    else:
        validation_commands = validation_commands_for_prompt(prompt_path)
        validation_source = "prompt" if prompt_exists else "unavailable"
    validation_outcomes = [
        {
            "command": command,
            "status": "skipped",
            "reason": "record-only mode; outer gate does not execute arbitrary prompt validation commands",
        }
        for command in validation_commands
    ]
    if not validation_commands:
        warnings.append("no validation commands were available to record")

    if plan and isinstance(plan.get("required_ahl_checks"), list):
        requested_ahl_checks = [item for item in plan["required_ahl_checks"] if isinstance(item, str)]
    else:
        requested_ahl_checks = list(OUTER_REQUIRED_AHL_CHECKS)
    ahl_checks = [run_outer_gate_ahl_check(root, command) for command in requested_ahl_checks]
    failed_ahl_checks = [item for item in ahl_checks if item["status"] == "failed"]
    if failed_ahl_checks:
        problems.extend(f"AHL check failed: {item['command']}" for item in failed_ahl_checks)
    skipped_or_unavailable = [item for item in ahl_checks if item["status"] in {"skipped", "unavailable"}]
    if skipped_or_unavailable:
        warnings.extend(f"AHL check {item['status']}: {item['command']}" for item in skipped_or_unavailable)

    completion_audit = completion_audit_from_artifact(root, args.audit_artifact)
    if completion_audit["status"] == "blocked":
        problems.append(completion_audit["notes"])
    elif completion_audit["status"] == "missing":
        warnings.append(completion_audit["notes"])

    handoff_path = root / "tmp" / "HANDOFF.md"
    commit_policy = plan.get("commit_policy") if isinstance(plan, dict) else None
    if commit_policy not in ("none", "plan-only", "explicit"):
        commit_policy = "none"

    if git["unsafe"]:
        status = "unsafe-git-state"
    elif not prompt_exists or next_blockers or plan_problem or (plan is not None and plan_prompt is None):
        status = "blocked"
    elif failed_ahl_checks:
        status = "failed-validation"
    elif completion_audit["status"] != "present":
        status = "needs-human-review"
    elif warnings:
        status = "pass-with-warnings"
    else:
        status = "pass"

    decision_by_status = {
        "pass": "continue",
        "pass-with-warnings": "continue-with-review",
        "blocked": "stop",
        "failed-validation": "stop",
        "needs-human-review": "stop-for-human-review",
        "driver-failed": "stop",
        "unsafe-git-state": "stop",
    }
    return {
        "ok": status in {"pass", "pass-with-warnings", "needs-human-review"},
        "schema": OUTER_GATE_REPORT_SCHEMA,
        "generated_at": utc_timestamp(),
        "status": status,
        "prompt_id": prompt_id,
        "prompt_file": f".prompts/{prompt_id}.txt",
        "prompt_file_exists": prompt_exists,
        "plan": {
            "supplied": bool(args.plan),
            "path": args.plan,
            "plan_id": plan.get("plan_id") if isinstance(plan, dict) else None,
            "prompt_in_plan": plan_prompt is not None if plan is not None else None,
            "final_prompt_in_plan": final_prompt_in_plan,
        },
        "git": git,
        "changed_files": git["lines"],
        "validation_commands": {"source": validation_source, "commands": validation_commands},
        "validation_outcomes": validation_outcomes,
        "ahl_checks": ahl_checks,
        "completion_audit": completion_audit,
        "next_prompt_readiness": {
            "status": "not-required" if not next_required else ("ready" if next_exists else "blocked"),
            "next_prompt": next_prompt_id,
            "path": f".prompts/{next_prompt_id}.txt",
            "required": next_required,
            "blockers": next_blockers,
        },
        "handoff": {
            "status": "present" if handoff_path.is_file() else "absent",
            "path": "tmp/HANDOFF.md",
        },
        "commit_plan": {
            "status": "planned" if commit_policy in {"plan-only", "explicit"} else "none",
            "policy": commit_policy,
            "notes": "Gate records commit intent only; it does not stage or commit.",
        },
        "decision": decision_by_status[status],
        "warnings": warnings,
        "problems": problems,
    }


def resolve_outer_run_ledger_path(root: Path, run_value: str) -> tuple[Path | None, str | None]:
    candidates: list[Path] = []
    supplied = Path(run_value)
    if supplied.suffix == ".json" or supplied.parts:
        candidates.append(root / supplied)
    candidates.append(root / "runs" / "outer-loop" / run_value / "run-ledger.json")
    candidates.append(root / "runs" / "outer-loop" / f"{run_value}.json")
    seen: set[Path] = set()
    for candidate in candidates:
        path = candidate.resolve()
        if path in seen:
            continue
        seen.add(path)
        try:
            path.relative_to(root.resolve())
        except ValueError:
            return None, f"run ledger path escapes repository root: {run_value}"
        if path.is_file():
            return path, None
    return None, f"missing run ledger artifact for run: {run_value}"


def load_outer_run_ledger(root: Path, run_value: str) -> tuple[dict[str, Any] | None, Path | None, str | None]:
    path, problem = resolve_outer_run_ledger_path(root, run_value)
    if problem:
        return None, path, problem
    assert path is not None
    data, load_problem = load_json_file(path)
    if load_problem:
        return None, path, load_problem
    if not isinstance(data, dict):
        return None, path, f"{repo_relative_path(root, path)}: run ledger must be a JSON object"
    required = ("run_id", "plan_id", "status", "steps")
    missing = [field for field in required if field not in data]
    if missing:
        return None, path, f"{repo_relative_path(root, path)}: malformed run ledger missing fields: {', '.join(missing)}"
    if not isinstance(data.get("steps"), list):
        return None, path, f"{repo_relative_path(root, path)}: malformed run ledger steps must be a list"
    return data, path, None


def outer_status_report(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    ledger, path, problem = load_outer_run_ledger(root, args.run)
    if problem:
        return {
            "ok": False,
            "status": "malformed" if path is not None else "missing",
            "run_id": args.run,
            "plan_id": None,
            "artifact": repo_relative_path(root, path) if path else None,
            "steps": {"total": 0, "completed": [], "failed": [], "skipped": [], "pending": []},
            "next_prompt": None,
            "resume_safe": False,
            "recovery_recommendation": "Fix or recreate the run ledger before using resume commands.",
            "problems": [problem],
        }
    assert ledger is not None and path is not None
    rollup = ledger_step_rollup(ledger)
    next_prompt = next_prompt_from_ledger(ledger)
    status = str(ledger.get("status", "unknown"))
    resume_safe = status in OUTER_RESUME_SAFE_STATUSES or (bool(next_prompt) and not rollup["failed"] and status not in {"completed"})
    return {
        "ok": True,
        "status": status,
        "run_id": ledger.get("run_id"),
        "plan_id": ledger.get("plan_id"),
        "artifact": repo_relative_path(root, path),
        "steps": rollup,
        "next_prompt": next_prompt,
        "resume_safe": resume_safe,
        "stop_reason": ledger.get("stop_reason"),
        "recovery_recommendation": ledger.get("recovery_recommendation") or ledger_recovery_recommendation(status, next_prompt),
        "problems": [],
    }


def outer_resume_plan(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    status = outer_status_report(root, argparse.Namespace(run=args.run))
    problems = list(status["problems"])
    git = git_status_report(root)
    if git["unsafe"] or git["lines"]:
        problems.append("worktree is not clean; refusing resume")
    next_prompt = status["next_prompt"]
    if args.rerun:
        ledger, _path, problem = load_outer_run_ledger(root, args.run)
        if problem:
            problems.append(problem)
        elif ledger is not None:
            next_prompt = next_prompt_from_ledger(ledger, rerun=True)
    if not next_prompt:
        problems.append("no pending prompt step is available to resume")
    if status["steps"]["failed"] and not args.rerun:
        problems.append("failed prompt steps require repair or explicit --rerun")
    ok = not problems
    return {
        "ok": ok,
        "status": "ready" if ok else "refused",
        "run_id": status["run_id"],
        "plan_id": status["plan_id"],
        "dry_run": bool(args.dry_run),
        "execute": bool(getattr(args, "execute", False)),
        "rerun": bool(args.rerun),
        "next_prompt": next_prompt,
        "completed_prompts": status["steps"]["completed"],
        "skipped_prompts": status["steps"]["skipped"],
        "failed_prompts": status["steps"]["failed"],
        "pending_prompts": status["steps"]["pending"],
        "git": git,
        "problems": problems,
        "notes": "Dry-run resume planning only; no assistant CLI is invoked." if args.dry_run else "Resume execution still requires an explicit runner execution path.",
    }


def fill_recovery_template(template: str, data: dict[str, Any]) -> str:
    replacements = {
        "{{RUN_ID}}": str(data.get("run_id") or "unknown"),
        "{{PLAN_ID}}": str(data.get("plan_id") or "unknown"),
        "{{STATUS}}": str(data.get("status") or "unknown"),
        "{{NEXT_PROMPT}}": str(data.get("next_prompt") or "none"),
        "{{STOP_REASON}}": str(data.get("stop_reason") or "not recorded"),
        "{{RECOVERY_RECOMMENDATION}}": str(data.get("recovery_recommendation") or "Review the run ledger before resuming."),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


def outer_recovery_handoff(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    status = outer_status_report(root, argparse.Namespace(run=args.run))
    problems = list(status["problems"])
    template_path = root / "templates" / "outer-loop" / "recovery-handoff.md"
    if not template_path.is_file():
        problems.append("missing recovery handoff template: templates/outer-loop/recovery-handoff.md")
    run_id = str(status.get("run_id") or args.run)
    out_path = root / "runs" / "outer-loop" / run_id / "recovery-handoff.md"
    if out_path.exists() and not args.force:
        problems.append(f"recovery handoff already exists: {repo_relative_path(root, out_path)}")
    if problems:
        return {"ok": False, "created": False, "artifact": repo_relative_path(root, out_path), "run_id": status.get("run_id"), "problems": problems}
    template = template_path.read_text(encoding="utf-8")
    content = fill_recovery_template(template, status)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return {"ok": True, "created": True, "artifact": repo_relative_path(root, out_path), "run_id": status.get("run_id"), "problems": []}


def command_outer(args: argparse.Namespace) -> int:
    if args.action == "plan":
        return command_outer_plan(args)
    if args.action == "run":
        root = repo_root()
        data = outer_run_ledger(root, args)
        human = [
            f"outer run: {data['status']}",
            f"- plan: {data['plan_id'] or 'unknown'}",
            f"- mode: {data['mode']}",
            f"- steps: {len(data['steps'])}",
        ]
        if data.get("artifact"):
            human.append(f"- ledger: {data['artifact']}")
        human.extend(f"- problem: {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)
    if args.action == "gate":
        root = repo_root()
        data = outer_gate_report(root, args)
        human = [
            f"outer gate: {data['status']}",
            f"- prompt: {data['prompt_id']}",
            f"- decision: {data['decision']}",
            f"- changed files: {len(data['changed_files'])}",
        ]
        human.extend(f"- warning: {warning}" for warning in data["warnings"])
        human.extend(f"- problem: {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)
    if args.action == "status":
        root = repo_root()
        data = outer_status_report(root, args)
        human = [f"outer status: {data['status']}", f"- run: {data['run_id'] or args.run}", f"- next prompt: {data['next_prompt'] or 'none'}"]
        human.extend(f"- problem: {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)
    if args.action == "resume":
        root = repo_root()
        data = outer_resume_plan(root, args)
        human = [f"outer resume: {data['status']}", f"- run: {data['run_id'] or args.run}", f"- next prompt: {data['next_prompt'] or 'none'}"]
        human.extend(f"- problem: {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)
    if args.action == "recovery-handoff":
        root = repo_root()
        data = outer_recovery_handoff(root, args)
        human = ["outer recovery handoff: created" if data["ok"] else "outer recovery handoff: refused", f"- artifact: {data['artifact']}"]
        human.extend(f"- problem: {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)
    root = repo_root()
    data = outer_dry_run_report(root, args.plan)
    human = ["outer dry-run: ok" if data["ok"] else "outer dry-run: problems found"]
    human.append(f"- plan: {data['plan_id'] or 'unknown'}")
    for step in data["steps"]:
        human.append(f"- {step['prompt_id']}: {step['status']}")
    human.extend(f"- {problem}" for problem in data["problems"])
    return emit(data, args.json, human, 0 if data["ok"] else 1)


PATH_TOKEN_RE = re.compile(r"(?:(?:^|[`\s(])((?:\.?[A-Za-z0-9_./-]+/)+[A-Za-z0-9_.-]+|[A-Za-z0-9_.-]+\.(?:py|md|json)))")


def parse_git_status_line(line: str) -> dict[str, Any]:
    index_status = line[0] if len(line) > 0 else " "
    worktree_status = line[1] if len(line) > 1 else " "
    raw_path = line[3:] if len(line) > 3 else line.strip()
    paths = [part.strip() for part in raw_path.split(" -> ")] if " -> " in raw_path else [raw_path.strip()]
    path = paths[-1] if paths else raw_path.strip()
    if line.startswith("??"):
        category = "untracked"
    elif index_status != " " and worktree_status == " ":
        category = "staged"
    elif "D" in (index_status, worktree_status):
        category = "deleted"
    else:
        category = "modified"
    return {
        "line": line,
        "path": path,
        "paths": paths,
        "index_status": index_status,
        "worktree_status": worktree_status,
        "category": category,
    }


def extract_repo_paths_from_prompt(text: str) -> list[str]:
    found: set[str] = set()
    for match in PATH_TOKEN_RE.finditer(text):
        value = match.group(1).strip("`.,)")
        if value.startswith(("http://", "https://")) or value.startswith("../"):
            continue
        if value.startswith("/"):
            continue
        if value and "." not in Path(value).parts:
            found.add(value)
    return sorted(found)


def prompt_section_text(text: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.I | re.M)
    match = pattern.search(text)
    if not match:
        return ""
    next_heading = re.search(r"^##\s+", text[match.end() :], re.M)
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.end() : end]


def changed_file_matches_expected(path: str, expected_paths: list[str]) -> bool:
    if not expected_paths:
        return True
    for expected in expected_paths:
        if path == expected or path.startswith(expected.rstrip("/") + "/"):
            return True
    return False


def prompt_commit_subject(prompt_ids: list[str], summary: str | None = None) -> str:
    prefix = f"[{prompt_ids[0]}]" if len(prompt_ids) == 1 else f"[{prompt_ids[0]}-{prompt_ids[-1]}]"
    return f"{prefix} {summary or 'Package prompt changes'}"


def commit_plan_output_path(root: Path, prompt_ids: list[str], run_value: str | None) -> Path:
    if run_value:
        run_path = (root / run_value).resolve()
        if run_path.name == "ledger.json" or run_path.name == "run-ledger.json":
            return run_path.parent / "commit-plan.json"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    label = "-".join(prompt_ids) if prompt_ids else "working-tree"
    return root / "runs" / "outer-loop" / "commit-plans" / f"{label}-{stamp}.json"


def commit_prompt_context(root: Path, prompt_id: str) -> dict[str, Any]:
    path = root / ".prompts" / f"{prompt_id}.txt"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    deliverables = prompt_section_text(text, "Required Deliverables")
    expected_paths = extract_repo_paths_from_prompt(deliverables) or extract_repo_paths_from_prompt(text)
    return {
        "prompt_id": prompt_id,
        "prompt_file": f".prompts/{prompt_id}.txt",
        "prompt_file_exists": path.is_file(),
        "expected_paths": expected_paths,
    }


def validation_from_ledger(ledger: dict[str, Any] | None, prompt_id: str) -> list[dict[str, Any]]:
    if not isinstance(ledger, dict):
        return []
    evidence: list[dict[str, Any]] = []
    for step in ledger.get("steps", []):
        if not isinstance(step, dict) or step.get("prompt_id") != prompt_id:
            continue
        for command in step.get("validation_commands", []):
            if isinstance(command, str):
                evidence.append({"command": command, "status": "recorded"})
        gate = step.get("gate")
        if isinstance(gate, dict):
            evidence.append({"command": "outer gate", "status": str(gate.get("status", "recorded"))})
    return evidence


def load_commit_ledger(root: Path, run_value: str | None) -> tuple[dict[str, Any] | None, str | None]:
    if not run_value:
        return None, None
    path = (root / run_value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None, f"run ledger path escapes repository root: {run_value}"
    if not path.is_file():
        return None, f"missing run ledger artifact: {run_value}"
    data, problem = load_json_file(path)
    if problem:
        return None, problem
    if not isinstance(data, dict):
        return None, f"{run_value}: top-level value must be an object"
    return data, None


def prompt_ids_from_commit_request(args: argparse.Namespace, ledger: dict[str, Any] | None) -> list[str]:
    if args.prompt:
        return [normalize_prompt_id(args.prompt)]
    prompt_ids: list[str] = []
    if isinstance(ledger, dict):
        for step in ledger.get("steps", []):
            if isinstance(step, dict) and isinstance(step.get("prompt_id"), str):
                prompt_id = normalize_prompt_id(step["prompt_id"])
                if prompt_id not in prompt_ids:
                    prompt_ids.append(prompt_id)
    return prompt_ids


def create_commit_plan(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    ledger, ledger_problem = load_commit_ledger(root, args.run)
    prompt_ids = prompt_ids_from_commit_request(args, ledger)
    problems: list[str] = []
    if ledger_problem:
        problems.append(ledger_problem)
    if not prompt_ids:
        problems.append("commit plan needs a prompt id or a run ledger with steps")

    git = git_status_report(root)
    problems.extend(git["problems"])
    entries = [parse_git_status_line(line) for line in git["lines"]]
    prompt_contexts = [commit_prompt_context(root, prompt_id) for prompt_id in prompt_ids]
    expected_paths: list[str] = []
    for context in prompt_contexts:
        expected_paths.extend(context["expected_paths"])
        if not context["prompt_file_exists"]:
            problems.append(f"missing prompt file: {context['prompt_file']}")
    expected_paths = sorted(set(expected_paths))

    candidate_entries = [entry for entry in entries if changed_file_matches_expected(entry["path"], expected_paths)]
    unrelated_entries = [entry for entry in entries if entry not in candidate_entries]
    changed_files = [
        {
            "path": entry["path"],
            "status": entry["category"],
            "git_status": entry["line"][:2],
            "status_line": entry["line"],
        }
        for entry in candidate_entries
    ]
    validation_evidence: list[dict[str, Any]] = []
    for prompt_id in prompt_ids:
        validation_evidence.extend(validation_from_ledger(ledger, prompt_id))
    if not validation_evidence:
        validation_evidence.append({"command": "not recorded", "status": "skipped", "notes": "No run ledger validation evidence was supplied."})

    validation_status = "passed"
    if isinstance(ledger, dict) and ledger.get("status") in {"blocked", "failed-validation", "driver-failed", "unsafe-git-state"}:
        validation_status = str(ledger.get("status"))
    elif not isinstance(ledger, dict):
        validation_status = "unknown"

    groups = []
    if prompt_ids:
        groups.append(
            {
                "group_id": "commit-1",
                "prompt_ids": prompt_ids,
                "subject": prompt_commit_subject(prompt_ids),
                "summary": "Package prompt-scoped changes for review.",
                "changed_files": changed_files,
                "validation_status": validation_status,
                "validation_evidence": validation_evidence,
                "follow_up_notes": [],
                "allow_failed_required": validation_status in {"blocked", "failed", "failed-validation", "driver-failed", "unsafe-git-state"},
            }
        )

    plan_id = f"commit-plan-{'-'.join(prompt_ids) if prompt_ids else 'unknown'}"
    artifact_path = Path(args.out) if args.out else commit_plan_output_path(root, prompt_ids, args.run)
    if not artifact_path.is_absolute():
        artifact_path = root / artifact_path
    try:
        artifact_rel = repo_relative_path(root, artifact_path)
    except ValueError:
        artifact_rel = str(artifact_path)
        problems.append(f"commit plan artifact path escapes repository root: {args.out}")

    data = {
        "ok": not problems,
        "schema": COMMIT_PLAN_SCHEMA,
        "plan_id": plan_id,
        "created_at": utc_timestamp(),
        "mode": "plan-only",
        "source": {"prompt": args.prompt, "run": args.run},
        "prompt_ids": prompt_ids,
        "prompt_context": prompt_contexts,
        "grouping_policy": {
            "default": "one commit per prompt id",
            "explicit_file_lists": True,
            "unrelated_changes_excluded": True,
        },
        "git": {
            "available": git["available"],
            "unsafe": git["unsafe"],
            "status_lines": git["lines"],
            "modified": [entry["path"] for entry in entries if entry["category"] == "modified"],
            "untracked": [entry["path"] for entry in entries if entry["category"] == "untracked"],
            "deleted": [entry["path"] for entry in entries if entry["category"] == "deleted"],
            "staged": [entry["path"] for entry in entries if entry["category"] == "staged"],
        },
        "groups": groups,
        "unrelated_changes": [{"path": entry["path"], "status_line": entry["line"]} for entry in unrelated_entries],
        "warnings": [],
        "problems": problems,
        "artifact": artifact_rel,
    }
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return data


def load_commit_plan(root: Path, plan_value: str) -> tuple[dict[str, Any] | None, str | None]:
    path = (root / plan_value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None, f"commit plan path escapes repository root: {plan_value}"
    if not path.is_file():
        return None, f"missing commit plan artifact: {plan_value}"
    data, problem = load_json_file(path)
    if problem:
        return None, problem
    if not isinstance(data, dict):
        return None, f"{plan_value}: top-level value must be an object"
    return data, None


def staged_paths(root: Path) -> tuple[list[str], list[str]]:
    result, problem = run_git(root, ["diff", "--cached", "--name-only"])
    if problem:
        return [], [problem]
    if result is None or result.returncode != 0:
        return [], [result.stderr.strip() if result else "could not inspect staged files"]
    return [line for line in result.stdout.splitlines() if line.strip()], []


def render_commit_message(group: dict[str, Any]) -> str:
    lines = [
        str(group.get("subject") or prompt_commit_subject([str(item) for item in group.get("prompt_ids", [])])),
        "",
        str(group.get("summary") or "Package prompt-scoped changes."),
        "",
        "Validation:",
    ]
    evidence = group.get("validation_evidence") if isinstance(group.get("validation_evidence"), list) else []
    if evidence:
        for item in evidence:
            if isinstance(item, dict):
                command = item.get("command", "unknown")
                status = item.get("status", "recorded")
                lines.append(f"- {command}: {status}")
    else:
        lines.append("- not recorded")
    lines.append("")
    lines.append("Changed areas:")
    for item in group.get("changed_files", []):
        if isinstance(item, dict):
            lines.append(f"- {item.get('path')}")
    follow_ups = group.get("follow_up_notes") if isinstance(group.get("follow_up_notes"), list) else []
    if follow_ups:
        lines.append("")
        lines.append("Follow-up notes:")
        lines.extend(f"- {note}" for note in follow_ups)
    return "\n".join(lines).rstrip() + "\n"


def commit_check_selector(args: argparse.Namespace) -> dict[str, Any]:
    prompt_id = normalize_prompt_id(args.prompt) if args.prompt else None
    if args.range:
        mode = "range"
        description = args.range
        rev_args = [args.range]
        truncated = False
    else:
        count = args.last if args.last is not None else COMMIT_CHECK_DEFAULT_LIMIT
        mode = "last" if args.last is not None else ("prompt-default" if prompt_id else "default")
        description = f"last {count}"
        rev_args = [f"--max-count={count}", "HEAD"]
        truncated = args.last is None and prompt_id is not None
    return {
        "mode": mode,
        "description": description,
        "rev_args": rev_args,
        "prompt_id": prompt_id,
        "truncated": truncated,
    }


def git_commit_hashes(root: Path, selector: dict[str, Any]) -> tuple[list[str], list[str]]:
    result, problem = run_git(root, ["rev-list", "--reverse", *selector["rev_args"]])
    if problem:
        return [], [problem]
    if result is None:
        return [], ["git rev-list did not return a result"]
    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "does not have any commits yet" in stderr or "unknown revision" in stderr:
            return [], [stderr or "empty or invalid commit range"]
        return [], [stderr or "could not inspect commit range"]
    return [line.strip() for line in result.stdout.splitlines() if line.strip()], []


def git_commit_record(root: Path, commit_hash: str) -> tuple[dict[str, Any] | None, str | None]:
    message_result, message_problem = run_git(root, ["log", "-1", "--format=%B", commit_hash])
    if message_problem:
        return None, message_problem
    if message_result is None or message_result.returncode != 0:
        return None, message_result.stderr.strip() if message_result else "could not read commit message"

    meta_result, meta_problem = run_git(root, ["show", "--quiet", "--format=%h%x00%H%x00%P", commit_hash])
    if meta_problem:
        return None, meta_problem
    if meta_result is None or meta_result.returncode != 0:
        return None, meta_result.stderr.strip() if meta_result else "could not read commit metadata"
    meta_parts = meta_result.stdout.rstrip("\n").split("\x00")
    if len(meta_parts) < 3:
        return None, "could not parse commit metadata"

    files_result, files_problem = run_git(root, ["diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit_hash])
    if files_problem:
        return None, files_problem
    if files_result is None or files_result.returncode != 0:
        return None, files_result.stderr.strip() if files_result else "could not read changed files"

    raw_message = message_result.stdout.rstrip("\n")
    lines = raw_message.splitlines()
    subject = lines[0] if lines else ""
    return {
        "hash": meta_parts[1],
        "short_hash": meta_parts[0],
        "parents": [item for item in meta_parts[2].split() if item],
        "subject": subject,
        "message": raw_message,
        "message_lines": lines,
        "changed_files": [line for line in files_result.stdout.splitlines() if line.strip()],
    }, None


def generated_boilerplate_lines(lines: list[str]) -> list[str]:
    needles = (
        "generated by",
        "generated with",
        "auto-generated by",
        "automatically generated",
        "claude code",
        "codex",
    )
    matches: list[str] = []
    for line in lines:
        lowered = line.lower()
        if any(needle in lowered for needle in needles):
            matches.append(line)
    return matches


def inspect_commit_message(record: dict[str, Any], expected_prompt: str | None) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    subject = record["subject"]
    lines = record["message_lines"]
    if expected_prompt:
        expected_prefix = f"[{expected_prompt}]"
        if not subject.startswith(expected_prefix):
            issues.append(
                {
                    "code": "missing_prompt_prefix",
                    "severity": "error",
                    "message": f"subject must start with {expected_prefix}",
                    "guidance": "amend this commit or use an interactive rebase to rewrite the subject.",
                }
            )
    elif not PROMPT_COMMIT_SUBJECT_RE.search(subject):
        issues.append(
            {
                "code": "missing_prompt_prefix",
                "severity": "error",
                "message": "subject must start with a prompt prefix such as [PROMPT_84]",
                "guidance": "amend this commit or use an interactive rebase to add the prompt prefix.",
            }
        )
    if len(subject) > COMMIT_SUBJECT_LIMIT:
        issues.append(
            {
                "code": "overlong_subject",
                "severity": "warning",
                "message": f"subject is {len(subject)} characters; keep it at or below {COMMIT_SUBJECT_LIMIT}",
                "guidance": "shorten the subject during amend or rebase if this hurts reviewability.",
            }
        )
    if len(lines) > 1 and lines[1] != "":
        issues.append(
            {
                "code": "missing_blank_line",
                "severity": "error",
                "message": "message body must be separated from the subject by a blank line",
                "guidance": "rewrite with a short subject, blank line, then body.",
            }
        )
    if "\\n" in record["message"]:
        issues.append(
            {
                "code": "literal_newline_sequence",
                "severity": "error",
                "message": "commit message contains a literal \\n sequence",
                "guidance": "rewrite the message with a heredoc or message file so real newlines are used.",
            }
        )
    for index, line in enumerate(lines[2:], start=3):
        stripped = line.strip()
        if stripped and len(line) > COMMIT_BODY_LINE_LIMIT:
            issues.append(
                {
                    "code": "unwrapped_body_line",
                    "severity": "warning",
                    "message": f"line {index} is {len(line)} characters; wrap body lines at {COMMIT_BODY_LINE_LIMIT}",
                    "guidance": "wrap body text during amend or rebase if the line is prose rather than a path or command.",
                }
            )
            break
    if any(line.lower().startswith("co-authored-by:") for line in lines):
        issues.append(
            {
                "code": "co_author_trailer",
                "severity": "error",
                "message": "commit message contains a co-author trailer",
                "guidance": "remove the trailer with amend or interactive rebase if it was accidental.",
            }
        )
    boilerplate = generated_boilerplate_lines(lines)
    if boilerplate:
        issues.append(
            {
                "code": "generated_boilerplate",
                "severity": "warning",
                "message": "commit message appears to contain generated assistant boilerplate",
                "guidance": "rewrite the message to describe the human-reviewed change.",
            }
        )
    if len(record["parents"]) > 1:
        issues.append(
            {
                "code": "merge_commit",
                "severity": "warning",
                "message": "merge commit detected; grouping evidence may need manual review",
                "guidance": "inspect the merge manually before deciding whether history cleanup is warranted.",
            }
        )
    return issues


def group_summary_for_commits(commits: list[dict[str, Any]]) -> dict[str, Any]:
    prompt_counts: dict[str, int] = {}
    top_dirs: dict[str, int] = {}
    all_files: set[str] = set()
    for commit in commits:
        for match in PROMPT_COMMIT_RE.findall(commit["subject"]):
            prompt_id = f"PROMPT_{match}"
            prompt_counts[prompt_id] = prompt_counts.get(prompt_id, 0) + 1
        for path in commit["changed_files"]:
            all_files.add(path)
            top = path.split("/", 1)[0] if "/" in path else "."
            top_dirs[top] = top_dirs.get(top, 0) + 1
    return {
        "commit_count": len(commits),
        "prompt_counts": dict(sorted(prompt_counts.items())),
        "changed_file_count": len(all_files),
        "changed_top_dirs": sorted(top_dirs),
        "plausibly_grouped_by_prompt": len(prompt_counts) <= 1 or len(commits) == len(prompt_counts),
    }


def commit_check_data(args: argparse.Namespace) -> dict[str, Any]:
    locate = project_locate_data(args.project)
    problems = list(locate["problems"])
    warnings = list(locate["warnings"])
    project = dict(locate["project"])
    project_root = Path(project["root"])
    selector = commit_check_selector(args)
    if args.last is not None and args.last < 1:
        problems.append("--last must be a positive integer")
    if selector["truncated"]:
        warnings.append(
            f"{selector['prompt_id']} selection searched the most recent {COMMIT_CHECK_DEFAULT_LIMIT} commits; use --last or --range if older commits may belong to this prompt"
        )
    if not project["git"]["inside_work_tree"]:
        problems.append("target project is not inside a git work tree")

    selected_hashes: list[str] = []
    selected_commits: list[dict[str, Any]] = []
    unmatched_commit_count = 0
    if not problems:
        selected_hashes, hash_problems = git_commit_hashes(project_root, selector)
        problems.extend(hash_problems)
    prompt_id = selector["prompt_id"]
    inspect_selected_against_prompt = prompt_id is not None and (args.last is not None or args.range is not None)
    if not problems:
        for commit_hash in selected_hashes:
            record, record_problem = git_commit_record(project_root, commit_hash)
            if record_problem:
                problems.append(record_problem)
                continue
            assert record is not None
            if prompt_id and not record["subject"].startswith(f"[{prompt_id}]"):
                unmatched_commit_count += 1
                if not inspect_selected_against_prompt:
                    continue
            record["issues"] = inspect_commit_message(record, prompt_id)
            selected_commits.append(record)
        if not selected_commits:
            if prompt_id:
                problems.append(f"no commits matched requested prompt {prompt_id}")
            else:
                warnings.append("no commits matched the requested selector")

    issue_count = sum(len(commit.get("issues", [])) for commit in selected_commits)
    guidance: list[str] = []
    if issue_count:
        if len(selected_commits) == 1:
            guidance.append("suggested command: git commit --amend")
        else:
            guidance.append(f"suggested command: git rebase -i {selected_commits[0]['hash']}^")
    summary = group_summary_for_commits(selected_commits)
    if selected_commits and not summary["plausibly_grouped_by_prompt"]:
        warnings.append("commit range includes multiple prompt prefixes; verify grouping before publishing")

    commits = [
        {
            "hash": commit["hash"],
            "short_hash": commit["short_hash"],
            "subject": commit["subject"],
            "parents": commit["parents"],
            "changed_files": commit["changed_files"],
            "issues": commit["issues"],
        }
        for commit in selected_commits
    ]
    return {
        "ok": not problems and issue_count == 0,
        "read_only": True,
        "project": {
            "requested": project["requested"],
            "root": project["root"],
            "source": project["source"],
        },
        "selector": {
            "mode": selector["mode"],
            "description": selector["description"],
            "prompt": prompt_id,
            "searched_commit_count": len(selected_hashes),
            "matched_commit_count": len(selected_commits),
            "unmatched_commit_count": unmatched_commit_count,
            "truncated": selector["truncated"],
        },
        "summary": summary,
        "commits": commits,
        "guidance": guidance,
        "warnings": warnings,
        "problems": problems,
    }


def execute_commit_plan(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    plan, problem = load_commit_plan(root, args.plan)
    problems: list[str] = []
    commits: list[dict[str, Any]] = []
    if problem:
        return {"ok": False, "status": "blocked", "plan": args.plan, "dry_run": args.dry_run, "commits": [], "problems": [problem]}
    assert plan is not None
    if not args.operator_approved and not args.dry_run:
        problems.append("commit execution requires --operator-approved")

    groups = plan.get("groups")
    if not isinstance(groups, list) or not groups:
        problems.append("commit plan has no groups")
        groups = []

    plan_paths: set[str] = set()
    for group in groups:
        if not isinstance(group, dict):
            problems.append("commit group must be an object")
            continue
        validation_status = group.get("validation_status")
        if validation_status in {"blocked", "failed", "failed-validation", "driver-failed", "unsafe-git-state"} and not args.allow_failed:
            problems.append(f"{group.get('group_id', 'commit group')}: validation status is {validation_status}; use --allow-failed to override")
        files = group.get("changed_files")
        if not isinstance(files, list) or not files:
            problems.append(f"{group.get('group_id', 'commit group')}: no changed files listed")
            continue
        for file_item in files:
            if not isinstance(file_item, dict) or not isinstance(file_item.get("path"), str):
                problems.append(f"{group.get('group_id', 'commit group')}: changed file entry is invalid")
                continue
            rel = file_item["path"]
            target = (root / rel).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                problems.append(f"{group.get('group_id', 'commit group')}: file escapes repository root: {rel}")
                continue
            if not target.exists():
                problems.append(f"{group.get('group_id', 'commit group')}: listed file is missing: {rel}")
            plan_paths.add(rel)

    staged, staged_problems = staged_paths(root)
    problems.extend(staged_problems)
    unexpected_staged = sorted(path for path in staged if path not in plan_paths)
    if unexpected_staged:
        problems.append("refusing to commit unrelated staged files: " + ", ".join(unexpected_staged))
    if problems:
        return {"ok": False, "status": "blocked", "plan": args.plan, "dry_run": args.dry_run, "commits": commits, "problems": problems}

    message_dir = root / "tmp" / "commit-messages"
    message_dir.mkdir(parents=True, exist_ok=True)
    for index, group in enumerate(groups, start=1):
        assert isinstance(group, dict)
        file_paths = [item["path"] for item in group["changed_files"] if isinstance(item, dict) and isinstance(item.get("path"), str)]
        message = render_commit_message(group)
        message_path = message_dir / f"{plan.get('plan_id', 'commit-plan')}-{index}.txt"
        message_path.write_text(message, encoding="utf-8")
        command_record = {"group_id": group.get("group_id"), "files": file_paths, "message_file": repo_relative_path(root, message_path), "hash": None}
        if args.dry_run:
            command_record["status"] = "dry-run"
            commits.append(command_record)
            continue
        add_result, add_problem = run_git(root, ["add", "--", *file_paths])
        if add_problem or add_result is None or add_result.returncode != 0:
            problems.append(add_problem or add_result.stderr.strip() or "git add failed")
            break
        commit_result, commit_problem = run_git(root, ["commit", "-F", str(message_path)])
        if commit_problem or commit_result is None or commit_result.returncode != 0:
            problems.append(commit_problem or commit_result.stderr.strip() or "git commit failed")
            break
        hash_result, hash_problem = run_git(root, ["rev-parse", "--short", "HEAD"])
        commit_hash = None
        if not hash_problem and hash_result is not None and hash_result.returncode == 0:
            commit_hash = hash_result.stdout.strip()
        command_record["status"] = "committed"
        command_record["hash"] = commit_hash
        commits.append(command_record)

    return {"ok": not problems, "status": "committed" if not args.dry_run and not problems else ("dry-run" if args.dry_run and not problems else "blocked"), "plan": args.plan, "dry_run": args.dry_run, "commits": commits, "problems": problems}


def command_commit(args: argparse.Namespace) -> int:
    if args.action == "check":
        data = commit_check_data(args)
        human = [
            "commit check: ok" if data["ok"] else "commit check: issues found",
            f"- project root: {data['project']['root']}",
            f"- selector: {data['selector']['description']}",
            f"- commits: {data['summary']['commit_count']}",
            f"- issues: {sum(len(commit['issues']) for commit in data['commits'])}",
        ]
        for commit in data["commits"]:
            human.append(f"- {commit['short_hash']} {commit['subject']}")
            for issue in commit["issues"]:
                human.append(f"  - {issue['severity']}: {issue['message']}")
        human.extend(f"- guidance: {item}" for item in data["guidance"])
        human.extend(f"- warning: {warning}" for warning in data["warnings"])
        human.extend(f"- problem: {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)

    root = repo_root()
    if args.action == "plan":
        data = create_commit_plan(root, args)
        human = [
            "commit plan: ok" if data["ok"] else "commit plan: problems found",
            f"- prompts: {', '.join(data['prompt_ids']) if data['prompt_ids'] else 'none'}",
            f"- groups: {len(data['groups'])}",
            f"- artifact: {data['artifact']}",
        ]
        human.extend(f"- problem: {problem}" for problem in data["problems"])
        return emit(data, args.json, human, 0 if data["ok"] else 1)
    data = execute_commit_plan(root, args)
    human = [
        f"commit execute: {data['status']}",
        f"- commits: {len(data['commits'])}",
    ]
    human.extend(f"- problem: {problem}" for problem in data["problems"])
    return emit(data, args.json, human, 0 if data["ok"] else 1)


def portable_rehearsal_command(label: str, command: str, ok: bool, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"label": label, "command": command, "status": "pass" if ok else "fail", "ok": ok, "details": details or {}}


def portable_rehearsal_missing_fixture(path: Path, label: str) -> dict[str, Any] | None:
    if path.exists():
        return None
    return portable_rehearsal_command(label, f"check fixture path {path}", False, {"problem": f"missing fixture path: {path}"})


def create_portable_rehearsal_git_repo() -> tuple[str | None, dict[str, Any]]:
    if not shutil.which("git"):
        return None, {"status": "skip", "reason": "git is not available"}

    tempdir = tempfile.TemporaryDirectory(prefix="ahl-portable-rehearsal-")
    repo = Path(tempdir.name)
    commands: list[dict[str, Any]] = []

    def run(args: list[str]) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(args, cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        commands.append({"command": " ".join(args), "returncode": result.returncode})
        return result

    run(["git", "init"])
    run(["git", "config", "user.email", "ahl-rehearsal@example.test"])
    run(["git", "config", "user.name", "AHL Rehearsal"])
    (repo / "good.txt").write_text("good\n", encoding="utf-8")
    run(["git", "add", "good.txt"])
    good_commit = run(["git", "commit", "-m", "[PROMPT_01] Add portable rehearsal fixture", "-m", "Record deterministic rehearsal data."])
    (repo / "bad.txt").write_text("bad\n", encoding="utf-8")
    run(["git", "add", "bad.txt"])
    bad_commit = run(["git", "commit", "-m", "Add unprefixed rehearsal fixture"])
    ok = all(item["returncode"] == 0 for item in commands) and good_commit.returncode == 0 and bad_commit.returncode == 0
    if not ok:
        tempdir.cleanup()
        return None, {"status": "fail", "commands": commands, "reason": "temporary git repo setup failed"}
    return str(repo), {"status": "pass", "commands": commands, "cleanup": tempdir}


def portable_rehearsal_data(args: argparse.Namespace) -> dict[str, Any]:
    ahl_home = script_ahl_home()
    basic = Path(args.basic_project or ahl_home / "fixtures" / "portable-operator" / "projects" / "basic")
    gapped = Path(args.gapped_project or ahl_home / "fixtures" / "portable-operator" / "projects" / "gapped")
    if not basic.is_absolute():
        basic = ahl_home / basic
    if not gapped.is_absolute():
        gapped = ahl_home / gapped

    commands: list[dict[str, Any]] = []
    for fixture_path, label in ((basic, "basic fixture exists"), (gapped, "gapped fixture exists")):
        missing = portable_rehearsal_missing_fixture(fixture_path, label)
        if missing:
            commands.append(missing)

    if not commands:
        locate = project_locate_data(str(basic))
        commands.append(portable_rehearsal_command("AHL home and project root discovery", f"python3 scripts/ahl.py project locate --project {basic} --json", locate["ok"] and Path(locate["ahl_home"]["path"]).resolve() == ahl_home.resolve() and Path(locate["project"]["root"]).resolve() == basic.resolve(), {"ahl_home": locate["ahl_home"]["path"], "project_root": locate["project"]["root"], "warnings": locate["warnings"], "problems": locate["problems"]}))

        basic_status = project_status_data(str(basic))
        commands.append(portable_rehearsal_command("project status basic fixture", f"python3 scripts/ahl.py project status --project {basic} --json", basic_status["ok"] and basic_status["project"]["promptset"]["state"] == "valid-sequential", {"promptset_state": basic_status["project"]["promptset"]["state"], "prompt_files": basic_status["project"]["promptset"]["filenames"], "likely_next_prompt": basic_status["project"]["next_prompt"]["likely_next_prompt"], "problems": basic_status["problems"]}))

        gapped_status = project_status_data(str(gapped))
        commands.append(portable_rehearsal_command("project status gapped fixture", f"python3 scripts/ahl.py project status --project {gapped} --json", gapped_status["ok"] and gapped_status["project"]["promptset"]["state"] == "gaps" and 2 in gapped_status["project"]["promptset"]["gaps"], {"promptset_state": gapped_status["project"]["promptset"]["state"], "gaps": gapped_status["project"]["promptset"]["gaps"], "problems": gapped_status["problems"]}))

        snippets = lifecycle_snippets_data("PROMPT_01", project_value=str(basic))
        commands.append(portable_rehearsal_command("lifecycle snippets fixture prompt", f"python3 scripts/ahl.py lifecycle snippets PROMPT_01 --project {basic} --json", snippets["ok"] and snippets["snippets"]["run"] == "Load AGENT.md, then run .prompts/PROMPT_01.txt", {"bootstrap_doc": snippets["configuration"]["bootstrap_doc"], "context_mentioned": snippets["configuration"]["context_mentioned"], "snippet_keys": sorted(snippets["snippets"]), "problems": snippets["problems"]}))

        context = lifecycle_context_check_data("PROMPT_01", project_value=str(basic))
        commands.append(portable_rehearsal_command("context-update check fixture prompt", f"python3 scripts/ahl.py lifecycle context-check PROMPT_01 --project {basic} --json", context["ok"] and context["read_only"] and not context["changed_paths"], {"read_only": context["read_only"], "changed_paths": context["changed_paths"], "conclusion": context["conclusion"], "warnings": context["warnings"], "problems": context["problems"]}))

        run_range = lifecycle_run_range_data("1", "2", project_value=str(basic), plan_id_value="portable-rehearsal-basic")
        commands.append(portable_rehearsal_command("run-range dry-run basic fixture", f"python3 scripts/ahl.py lifecycle run-range 1 2 --project {basic} --dry-run --json", run_range["ok"] and run_range["dry_run"] and run_range["prompt_ids"] == ["PROMPT_01", "PROMPT_02"], {"plan_id": run_range["plan_id"], "prompt_ids": run_range["prompt_ids"], "mode": run_range["mode"], "problems": run_range["problems"]}))

        gapped_range = lifecycle_run_range_data("1", "3", project_value=str(gapped), plan_id_value="portable-rehearsal-gapped")
        commands.append(portable_rehearsal_command("run-range gapped fixture failure is clear", f"python3 scripts/ahl.py lifecycle run-range 1 3 --project {gapped} --dry-run --json", not gapped_range["ok"] and "PROMPT_02" in gapped_range["missing_prompt_ids"], {"missing_prompt_ids": gapped_range["missing_prompt_ids"], "stop_reason": gapped_range["stop_reason"], "problems": gapped_range["problems"]}))

        temp_repo, git_setup = create_portable_rehearsal_git_repo()
        if temp_repo is None:
            commands.append({"label": "commit-check temporary git fixture", "command": "python3 scripts/ahl.py commit check --project <tempdir> --last 2 --json", "status": git_setup["status"], "ok": git_setup["status"] == "skip", "details": {k: v for k, v in git_setup.items() if k != "cleanup"}})
        else:
            cleanup = git_setup.pop("cleanup")
            try:
                commit_check = commit_check_data(argparse.Namespace(project=temp_repo, prompt=None, last=2, range=None))
                issue_codes = [issue["code"] for commit in commit_check["commits"] for issue in commit["issues"]]
                commands.append(portable_rehearsal_command("commit-check temporary git fixture", "python3 scripts/ahl.py commit check --project <tempdir> --last 2 --json", not commit_check["ok"] and "missing_prompt_prefix" in issue_codes and commit_check["summary"]["commit_count"] == 2, {"temp_repo_created": True, "temp_repo_cleaned_up": False, "commit_count": commit_check["summary"]["commit_count"], "issue_codes": issue_codes, "setup": git_setup, "problems": commit_check["problems"]}))
            finally:
                cleanup.cleanup()
            commands[-1]["details"]["temp_repo_cleaned_up"] = not Path(temp_repo).exists()

    failed = [item for item in commands if item["status"] == "fail"]
    skipped = [item for item in commands if item["status"] == "skip"]
    return {
        "ok": not failed,
        "schema": PORTABLE_REHEARSAL_REPORT_SCHEMA,
        "generated_at": utc_timestamp(),
        "mode": "offline-rehearsal",
        "read_only": True,
        "assistant_invocation": "disabled",
        "ahl_home": str(ahl_home),
        "fixture_projects": {"basic": str(basic), "gapped": str(gapped)},
        "commands": commands,
        "summary": {"passed": sum(1 for item in commands if item["status"] == "pass"), "failed": len(failed), "skipped": len(skipped), "total": len(commands)},
        "known_limitations": [
            "Rehearsal proves helper composition against fixtures; it does not call assistant CLIs or perform real prompt implementation.",
            "Context-update check is advisory and read-only; human review decides whether durable context edits are justified.",
            "Commit-check coverage uses isolated temporary git history, not the AHL repository history.",
        ],
        "residual_manual_steps": ["A human operator still starts each assistant session, reviews implementation, approves commits, and decides context updates."],
        "capstone_ready": not failed,
        "problems": [item["details"].get("problem", item["label"]) for item in failed],
    }


def command_portable(args: argparse.Namespace) -> int:
    data = portable_rehearsal_data(args)
    human = [
        "portable rehearsal: ok" if data["ok"] else "portable rehearsal: problems found",
        f"- commands: {data['summary']['passed']} passed, {data['summary']['failed']} failed, {data['summary']['skipped']} skipped",
        f"- capstone ready: {data['capstone_ready']}",
    ]
    for item in data["commands"]:
        human.append(f"- {item['status']}: {item['label']}")
    human.extend(f"- problem: {problem}" for problem in data["problems"])
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


def domain_pack_manifest_paths(root: Path) -> list[Path]:
    base = root / "domain-packs"
    if not base.is_dir():
        return []
    return sorted(base.glob("*/pack.json"))


def validate_domain_pack_path(pack_dir: Path, root: Path, value: Any) -> tuple[bool, str | None]:
    if not isinstance(value, str) or not value:
        return False, "path value must be a non-empty string"
    candidate = (pack_dir / value).resolve()
    try:
        candidate.relative_to(pack_dir.resolve())
    except ValueError:
        return False, f"path escapes pack directory: {value}"
    if not candidate.exists():
        return False, f"referenced path does not exist: {pack_dir.relative_to(root)}/{value}"
    return True, None


def domain_pack_check_one(root: Path, manifest: Path) -> dict[str, Any]:
    pack_dir = manifest.parent
    rel_manifest = str(manifest.relative_to(root))
    rel_dir = str(pack_dir.relative_to(root))
    problems: list[str] = []
    checked_files: list[str] = []

    data, problem = load_json_file(manifest)
    if problem:
        return {
            "id": pack_dir.name,
            "path": rel_dir,
            "manifest": rel_manifest,
            "status": "fail",
            "checked_files": checked_files,
            "problems": [problem],
        }
    if not isinstance(data, dict):
        return {
            "id": pack_dir.name,
            "path": rel_dir,
            "manifest": rel_manifest,
            "status": "fail",
            "checked_files": checked_files,
            "problems": ["manifest top-level value must be an object"],
        }

    missing = [field for field in DOMAIN_PACK_REQUIRED_FIELDS if field not in data]
    if missing:
        problems.append("missing required fields: " + ", ".join(missing))

    pack_id = data.get("id")
    if not isinstance(pack_id, str) or not DOMAIN_PACK_ID_RE.fullmatch(pack_id):
        problems.append("id must be _template or a lowercase slug")
    elif pack_id != pack_dir.name:
        problems.append(f"id must match pack directory name: {pack_dir.name}")

    if not isinstance(data.get("schema_version"), int) or data.get("schema_version", 0) < 1:
        problems.append("schema_version must be an integer >= 1")
    for field in ("name", "purpose", "entrypoint"):
        if not isinstance(data.get(field), str) or not data.get(field):
            problems.append(f"{field} must be a non-empty string")

    status = data.get("status")
    if not isinstance(status, str) or status not in DOMAIN_PACK_STATUSES:
        problems.append("status must be one of: " + ", ".join(DOMAIN_PACK_STATUSES))
    if data.get("optional") is not True:
        problems.append("optional must be true")
    if data.get("core_doctrine_changes") is not False:
        problems.append("core_doctrine_changes must be false")

    entrypoint = data.get("entrypoint")
    if isinstance(entrypoint, str):
        ok, path_problem = validate_domain_pack_path(pack_dir, root, entrypoint)
        checked_files.append(f"{rel_dir}/{entrypoint}")
        if not ok and path_problem:
            problems.append(f"entrypoint: {path_problem}")

    files = data.get("files")
    if not isinstance(files, list) or not files:
        problems.append("files must be a non-empty list")
    else:
        seen: set[str] = set()
        for item in files:
            if not isinstance(item, str) or not item:
                problems.append("files entries must be non-empty strings")
                continue
            if item in seen:
                problems.append(f"duplicate file reference: {item}")
            seen.add(item)
            checked_files.append(f"{rel_dir}/{item}")
            ok, path_problem = validate_domain_pack_path(pack_dir, root, item)
            if not ok and path_problem:
                problems.append(f"files: {path_problem}")
        if isinstance(entrypoint, str) and entrypoint not in seen:
            problems.append("entrypoint must also be listed in files")

    return {
        "id": pack_id if isinstance(pack_id, str) else pack_dir.name,
        "path": rel_dir,
        "manifest": rel_manifest,
        "status": "fail" if problems else "pass",
        "checked_files": sorted(set(checked_files)),
        "problems": problems,
    }


def domain_pack_check_data(root: Path) -> dict[str, Any]:
    base = root / "domain-packs"
    checks: list[dict[str, Any]] = []
    problems: list[str] = []

    checks.append({"name": "domain pack directory", "path": "domain-packs", "ok": base.is_dir()})
    if not base.is_dir():
        problems.append("missing domain pack directory: domain-packs")
        return {"ok": False, "checks": checks, "problems": problems, "packs": []}

    manifests = domain_pack_manifest_paths(root)
    checks.append({"name": "domain pack manifests", "path": "domain-packs/*/pack.json", "ok": bool(manifests), "count": len(manifests)})
    if not manifests:
        problems.append("no domain pack manifests found")

    packs = [domain_pack_check_one(root, manifest) for manifest in manifests]
    for pack in packs:
        problems.extend(f"{pack['manifest']}: {problem}" for problem in pack["problems"])

    return {"ok": not problems, "checks": checks, "problems": problems, "packs": packs}


def command_domain_pack(args: argparse.Namespace) -> int:
    data = domain_pack_check_data(repo_root())
    human = ["domain-pack check: ok" if data["ok"] else "domain-pack check: problems found"]
    human.append(f"- packs checked: {len(data['packs'])}")
    for pack in data["packs"]:
        human.append(f"- {pack['id']}: {pack['status']}")
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

    driver = subparsers.add_parser("driver", help="List, validate, or safely probe assistant driver records.")
    driver.add_argument("action", choices=("list", "check", "probe"))
    driver.add_argument("driver_id", nargs="?", help="Driver id for `driver probe`.")
    driver.add_argument("--help-only", action="store_true", help="Run only the driver's configured help command.")
    driver.add_argument("--json", action="store_true")
    driver.set_defaults(func=command_driver)

    project = subparsers.add_parser("project", help="Locate AHL home and the target project root.")
    project_subparsers = project.add_subparsers(dest="action", required=True)
    project_locate = project_subparsers.add_parser("locate", help="Report AHL home and target project discovery.")
    project_locate.add_argument("--project", help="Target project path; defaults to the current working directory.")
    project_locate.add_argument("--json", action="store_true")
    project_locate.set_defaults(func=command_project)
    project_status = project_subparsers.add_parser("status", help="Report target project promptset and git status.")
    project_status.add_argument("--project", help="Target project path; defaults to the current working directory.")
    project_status.add_argument("--json", action="store_true")
    project_status.set_defaults(func=command_project)

    lifecycle = subparsers.add_parser("lifecycle", help="Print portable lifecycle operator snippets.")
    lifecycle_subparsers = lifecycle.add_subparsers(dest="action", required=True)
    lifecycle_snippets = lifecycle_subparsers.add_parser("snippets", help="Print reusable one-prompt lifecycle snippets.")
    lifecycle_snippets.add_argument("prompt", help="Prompt number, id, or filename, such as 45, PROMPT_45, or PROMPT_45.txt.")
    lifecycle_snippets.add_argument("--project", help="Target project path; defaults to the current working directory.")
    lifecycle_snippets.add_argument(
        "--bootstrap",
        default="auto",
        help="Bootstrap doc selection: auto, AGENT.md, CLAUDE.md, or none.",
    )
    lifecycle_snippets.add_argument("--context", action="store_true", help="Mention .context/ even when it is not detected.")
    lifecycle_snippets.add_argument("--no-context", action="store_true", help="Omit .context/ from the context-update snippet.")
    lifecycle_snippets.add_argument("--include-repair", action="store_true", help="Include the optional repair snippet.")
    lifecycle_snippets.add_argument("--json", action="store_true")
    lifecycle_snippets.set_defaults(func=command_lifecycle)
    lifecycle_context_check = lifecycle_subparsers.add_parser(
        "context-check",
        help="Read git status and suggest context-update review questions.",
    )
    lifecycle_context_check.add_argument(
        "prompt",
        help="Prompt number, id, or filename, such as 45, PROMPT_45, or PROMPT_45.txt.",
    )
    lifecycle_context_check.add_argument("--project", help="Target project path; defaults to the current working directory.")
    lifecycle_context_check.add_argument("--json", action="store_true")
    lifecycle_context_check.set_defaults(func=command_lifecycle)
    lifecycle_run_range = lifecycle_subparsers.add_parser(
        "run-range",
        help="Dry-run a one-prompt-at-a-time lifecycle plan for a prompt range.",
    )
    lifecycle_run_range.add_argument("start_prompt", help="First prompt number, id, or filename.")
    lifecycle_run_range.add_argument("end_prompt", help="Last prompt number, id, or filename.")
    lifecycle_run_range.add_argument("--project", help="Target project path; defaults to the current working directory.")
    lifecycle_run_range.add_argument(
        "--bootstrap",
        default="auto",
        help="Bootstrap doc selection for generated run snippets: auto, AGENT.md, CLAUDE.md, or none.",
    )
    lifecycle_run_range.add_argument("--dry-run", action="store_true", default=True, help="Default read-only mode; included for explicit operator clarity.")
    lifecycle_run_range.add_argument("--artifact", help="Explicit JSON artifact path to write; relative paths are under AHL home.")
    lifecycle_run_range.add_argument("--plan-id", help="Deterministic plan id for tests or operator-selected artifacts.")
    lifecycle_run_range.add_argument("--force", action="store_true", help="Overwrite an existing explicit artifact.")
    lifecycle_run_range.add_argument("--json", action="store_true")
    lifecycle_run_range.set_defaults(func=command_lifecycle)

    outer = subparsers.add_parser("outer", help="Plan, dry-run, and gate sequential outer-loop batches.")
    outer_subparsers = outer.add_subparsers(dest="action", required=True)
    outer_plan = outer_subparsers.add_parser("plan", help="Create an inspectable sequential batch plan artifact.")
    range_group = outer_plan.add_mutually_exclusive_group(required=True)
    range_group.add_argument("--from", dest="from_prompt", help="First prompt id, such as PROMPT_33.")
    range_group.add_argument("--next", type=int, help="Plan the next N prompt files from the promptset.")
    outer_plan.add_argument("--count", type=int, help="Number of prompts when using --from.")
    outer_plan.add_argument("--driver", required=True, help="Assistant driver id from registry/assistant-drivers.json.")
    outer_plan.add_argument("--model", help="Model name to record in the plan.")
    outer_plan.add_argument("--reasoning", help="Reasoning or thinking setting to record in the plan.")
    outer_plan.add_argument(
        "--permission-posture",
        choices=("read-only", "workspace-write", "manual-required"),
        default=OUTER_DEFAULT_PERMISSION_POSTURE,
    )
    outer_plan.add_argument(
        "--commit-policy",
        choices=("none", "plan-only", "explicit"),
        default=OUTER_DEFAULT_COMMIT_POLICY,
    )
    outer_plan.add_argument("--plan-id", help="Deterministic plan id for tests or operator-chosen artifacts.")
    outer_plan.add_argument("--json", action="store_true")
    outer_plan.set_defaults(func=command_outer)

    outer_dry_run = outer_subparsers.add_parser("dry-run", help="Validate a batch plan without assistant invocation.")
    outer_dry_run.add_argument("--plan", required=True, help="Path to a plan.json artifact.")
    outer_dry_run.add_argument("--json", action="store_true")
    outer_dry_run.set_defaults(func=command_outer)

    outer_run = outer_subparsers.add_parser("run", help="Run a sequential outer-loop plan, dry-run by default.")
    outer_run.add_argument("--plan", required=True, help="Path to a plan.json artifact.")
    mode_group = outer_run.add_mutually_exclusive_group()
    mode_group.add_argument("--dry-run", action="store_true", help="Build payloads and ledger entries without invoking assistant CLIs.")
    mode_group.add_argument("--execute", action="store_true", help="Explicitly allow live assistant CLI invocation.")
    outer_run.add_argument("--max-prompts", type=int, help="Limit the number of plan prompts processed.")
    outer_run.add_argument("--timeout-seconds", type=int, default=900, help="Timeout for each live assistant CLI invocation.")
    outer_run.add_argument("--driver-arg", action="append", default=[], help="Explicit extra argument passed to a live driver command.")
    outer_run.add_argument("--run-id", help=argparse.SUPPRESS)
    outer_run.add_argument("--json", action="store_true")
    outer_run.set_defaults(func=command_outer)

    outer_gate = outer_subparsers.add_parser("gate", help="Collect post-prompt validation, audit, and readiness evidence.")
    outer_gate.add_argument("prompt", help="Prompt id to gate, such as PROMPT_36.")
    outer_gate.add_argument("--plan", help="Path to a plan.json artifact to read validation commands and final-step context.")
    outer_gate.add_argument("--audit-artifact", help="Path to an explicit completion audit artifact, when one exists.")
    outer_gate.add_argument("--json", action="store_true")
    outer_gate.set_defaults(func=command_outer)

    outer_status = outer_subparsers.add_parser("status", help="Summarize an outer-loop run ledger.")
    outer_status.add_argument("--run", required=True, help="Run id or run-ledger.json path.")
    outer_status.add_argument("--json", action="store_true")
    outer_status.set_defaults(func=command_outer)

    outer_resume = outer_subparsers.add_parser("resume", help="Plan a safe resume from an outer-loop run ledger.")
    outer_resume.add_argument("--run", required=True, help="Run id or run-ledger.json path.")
    outer_resume.add_argument("--dry-run", action="store_true", help="Plan resume without invoking assistants.")
    outer_resume.add_argument("--execute", action="store_true", help="Reserved explicit execution flag; uses runner path only in later work.")
    outer_resume.add_argument("--rerun", action="store_true", help="Allow selecting an already-recorded step for explicit rerun.")
    outer_resume.add_argument("--json", action="store_true")
    outer_resume.set_defaults(func=command_outer)

    outer_recovery = outer_subparsers.add_parser("recovery-handoff", help="Create a recovery handoff from a run ledger.")
    outer_recovery.add_argument("--run", required=True, help="Run id or run-ledger.json path.")
    outer_recovery.add_argument("--force", action="store_true", help="Overwrite an existing recovery handoff.")
    outer_recovery.add_argument("--json", action="store_true")
    outer_recovery.set_defaults(func=command_outer)

    commit = subparsers.add_parser("commit", help="Plan, inspect, or explicitly execute prompt-scoped commits.")
    commit_subparsers = commit.add_subparsers(dest="action", required=True)
    commit_plan = commit_subparsers.add_parser("plan", help="Create a prompt-scoped commit plan artifact.")
    commit_plan.add_argument("prompt", nargs="?", help="Prompt id, number, or prompt filename.")
    commit_plan.add_argument("--run", help="Path to a run ledger artifact.")
    commit_plan.add_argument("--out", help="Path for the generated commit plan artifact.")
    commit_plan.add_argument("--json", action="store_true")
    commit_plan.set_defaults(func=command_commit)

    commit_check = commit_subparsers.add_parser("check", help="Inspect recent commit message and grouping hygiene.")
    commit_check.add_argument("--project", help="Target project path; defaults to the current working directory.")
    commit_check.add_argument("--prompt", help="Prompt id, number, or prompt filename to select by subject prefix.")
    range_selectors = commit_check.add_mutually_exclusive_group()
    range_selectors.add_argument("--last", type=int, help="Inspect the last N commits.")
    range_selectors.add_argument("--range", help="Inspect a safe git revision range such as HEAD~10..HEAD.")
    commit_check.add_argument("--json", action="store_true")
    commit_check.set_defaults(func=command_commit)

    commit_execute = commit_subparsers.add_parser("execute", help="Execute commits from an explicit commit plan.")
    commit_execute.add_argument("--plan", required=True, help="Path to a commit plan artifact.")
    commit_execute.add_argument("--operator-approved", action="store_true", help="Required approval flag for real commit execution.")
    commit_execute.add_argument("--allow-failed", action="store_true", help="Allow committing blocked or failed validation status.")
    commit_execute.add_argument("--dry-run", action="store_true", help="Check the plan and render message files without staging or committing.")
    commit_execute.add_argument("--json", action="store_true")
    commit_execute.set_defaults(func=command_commit)

    portable = subparsers.add_parser("portable", help="Run portable-operator rehearsal helpers.")
    portable_subparsers = portable.add_subparsers(dest="action", required=True)
    portable_rehearsal = portable_subparsers.add_parser("rehearsal", help="Run deterministic portable-operator fixture rehearsal.")
    portable_rehearsal.add_argument("--basic-project", help="Override the basic fixture path for failure testing.")
    portable_rehearsal.add_argument("--gapped-project", help="Override the gapped fixture path for failure testing.")
    portable_rehearsal.add_argument("--json", action="store_true")
    portable_rehearsal.set_defaults(func=command_portable)

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

    domain_pack = subparsers.add_parser("domain-pack", help="Validate optional domain pack manifests.")
    domain_pack.add_argument("action", choices=("check",))
    domain_pack.add_argument("--json", action="store_true")
    domain_pack.set_defaults(func=command_domain_pack)

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
