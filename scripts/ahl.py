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


PROMPT_RE = re.compile(r"^PROMPT_(\d+)\.txt$")
STRICT_PROMPT_RE = re.compile(r"^PROMPT_(\d{2})\.txt$")
NEXT_MARKER_RE = re.compile(r"^\s*(?:[-*]\s*)?(?:Next|Next step|## Next)\b", re.I)
CONTEXT_FILES = ("TASK.md", "SESSION.md", "MEMORY.md")
REFERENCE_DIRS = ("agent-context-base", "pi-mono", "claw-code")


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
    prompt_dir = root / ".prompts"
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
        "prompt_dir": ".prompts",
        "prompts": prompts,
        "filenames": [item["filename"] for item in prompts],
        "numbers": numbers,
        "duplicates": duplicates,
        "gaps": gaps,
        "strict_two_digit": not malformed,
        "malformed": malformed,
    }


def command_promptset(args: argparse.Namespace) -> int:
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ahl", description="Small helper tooling for agent-harness-lab.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Check expected repository foundations.")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=command_doctor)

    promptset = subparsers.add_parser("promptset", help="Inspect prompt filenames and numbering.")
    promptset.add_argument("--json", action="store_true")
    promptset.set_defaults(func=command_promptset)

    resume = subparsers.add_parser("resume", help="Print a grounded session context briefing.")
    resume.add_argument("--json", action="store_true")
    resume.set_defaults(func=command_resume)

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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
