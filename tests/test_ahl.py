import contextlib
from datetime import datetime as RealDateTime
import importlib.util
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ahl", ROOT / "scripts" / "ahl.py")
ahl = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ahl)


class AhlTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.addCleanup(self.tempdir.cleanup)

    def run_cli(self, *args):
        out = io.StringIO()
        with mock.patch("pathlib.Path.cwd", return_value=self.root):
            with contextlib.redirect_stdout(out):
                code = ahl.main(list(args))
        return code, out.getvalue()

    def write(self, path, content=""):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def add_foundations(self):
        self.write("README.md", "# Test\n")
        self.write("AGENT.md", "# Agent\n")
        self.write(
            ".gitignore",
            "\n".join(
                [
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
                    "!.env.example",
                    "*.pem",
                    "*.key",
                    "id_rsa",
                    "id_ed25519",
                ]
            )
            + "\n",
        )
        (self.root / ".prompts").mkdir()
        (self.root / "docs").mkdir()
        for dirname in ("contracts", "doctrine", "memory", "quality", "roles", "routines", "runtime", "safety", "skills"):
            (self.root / "docs" / dirname).mkdir()
        (self.root / "runbooks").mkdir()
        (self.root / "templates").mkdir()
        (self.root / "scripts").mkdir()
        (self.root / "tests").mkdir()
        self.write("tests/test_ahl.py", "# tests\n")

    def test_promptset_numbering_success(self):
        self.write(".prompts/PROMPT_01.txt")
        self.write(".prompts/PROMPT_02.txt")

        code, output = self.run_cli("promptset", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["numbers"], [1, 2])
        self.assertEqual(data["gaps"], [])
        self.assertTrue(data["strict_two_digit"])

    def test_help_json_lists_makefile_targets(self):
        code, output = self.run_cli("help", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertIn("doctor", data["makefile_targets"])
        self.assertTrue(any(item["name"] == "check-docs" for item in data["commands"]))

    def test_project_locate_discovers_ahl_home_from_script_location(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AHL_HOME", None)
            code, output = self.run_cli("project", "locate", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["ahl_home"]["source"], "script")
        self.assertEqual(Path(data["ahl_home"]["path"]), ROOT)
        self.assertTrue(data["ahl_home"]["valid"])

    def test_project_locate_rejects_invalid_ahl_home_override(self):
        with mock.patch.dict(os.environ, {"AHL_HOME": str(self.root)}, clear=False):
            code, output = self.run_cli("project", "locate", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertEqual(data["ahl_home"]["source"], "AHL_HOME")
        self.assertFalse(data["ahl_home"]["valid"])
        self.assertTrue(any("AHL_HOME" in problem for problem in data["problems"]))

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_project_locate_detects_project_root_inside_git_repo(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.write(".prompts/PROMPT_01.txt", "# Prompt\n")
        nested = self.root / "src" / "pkg"
        nested.mkdir(parents=True)

        code, output = self.run_cli("project", "locate", "--project", str(nested), "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(Path(data["project"]["root"]).resolve(), self.root.resolve())
        self.assertEqual(data["project"]["source"], "git-root")
        self.assertTrue(data["project"]["git"]["inside_work_tree"])
        self.assertTrue(data["project"]["prompt_dir_exists"])
        self.assertEqual(data["project"]["prompt_count"], 1)

    def test_project_locate_falls_back_without_git_root(self):
        self.write(".prompts/PROMPT_01.txt", "# Prompt\n")

        code, output = self.run_cli("project", "locate", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(Path(data["project"]["root"]).resolve(), self.root.resolve())
        self.assertEqual(data["project"]["source"], "path")
        self.assertIn("PROMPT_01.txt", data["project"]["prompt_files"])

    def test_project_locate_reports_missing_prompts_without_crashing(self):
        code, output = self.run_cli("project", "locate", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertFalse(data["project"]["prompt_dir_exists"])
        self.assertEqual(data["project"]["prompt_count"], 0)
        self.assertTrue(any(".prompts" in warning for warning in data["warnings"]))

    def test_project_locate_json_has_stable_fields(self):
        code, output = self.run_cli("project", "locate", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("ok", "ahl_home", "project", "warnings", "problems"):
            self.assertIn(key, data)
        for key in ("path", "source", "valid", "problems"):
            self.assertIn(key, data["ahl_home"])
        for key in (
            "requested",
            "requested_exists",
            "requested_is_dir",
            "root",
            "source",
            "git",
            "prompt_dir",
            "prompt_dir_exists",
            "prompt_count",
            "prompt_files",
        ):
            self.assertIn(key, data["project"])

    def test_project_status_reports_valid_promptset_and_context_files(self):
        self.write(".prompts/PROMPT_01.txt", "# Prompt\n")
        self.write(".prompts/PROMPT_02.txt", "# Prompt\n")
        self.write("AGENT.md", "# Agent\n")
        self.write("human-notes.md", "# Notes\n")
        (self.root / ".context").mkdir()

        code, output = self.run_cli("project", "status", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["project"]["promptset"]["state"], "valid-sequential")
        self.assertEqual(data["project"]["promptset"]["lowest_prompt_number"], 1)
        self.assertEqual(data["project"]["promptset"]["highest_prompt_number"], 2)
        self.assertEqual(data["project"]["next_prompt"]["next_after_highest_prompt_file"], "PROMPT_03")
        self.assertEqual(data["project"]["next_prompt"]["likely_next_prompt"], "PROMPT_03")
        self.assertTrue(data["project"]["files"]["AGENT.md"])
        self.assertTrue(data["project"]["files"][".context"])
        self.assertTrue(data["project"]["files"]["human-notes.md"])

    def test_project_status_reports_claude_without_agent(self):
        self.write("CLAUDE.md", "# Claude\n")

        code, output = self.run_cli("project", "status", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertFalse(data["project"]["files"]["AGENT.md"])
        self.assertTrue(data["project"]["files"]["CLAUDE.md"])

    def test_project_status_reports_missing_prompts(self):
        code, output = self.run_cli("project", "status", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["project"]["promptset"]["state"], "missing")
        self.assertFalse(data["project"]["promptset"]["prompt_dir_exists"])
        self.assertTrue(any(".prompts" in warning for warning in data["warnings"]))

    def test_project_status_reports_gaps_and_malformed_prompt_names(self):
        self.write(".prompts/PROMPT_01.txt")
        self.write(".prompts/PROMPT_03.txt")
        self.write(".prompts/PROMPT_3.txt")

        code, output = self.run_cli("project", "status", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["project"]["promptset"]["state"], "duplicates")
        self.assertIn(2, data["project"]["promptset"]["gaps"])
        self.assertIn(3, data["project"]["promptset"]["duplicates"])
        self.assertIn("PROMPT_3.txt", data["project"]["promptset"]["malformed"])
        self.assertFalse(data["project"]["promptset"]["strict_two_digit"])

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_project_status_reports_dirty_and_untracked_git_summary(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.write(".prompts/PROMPT_01.txt", "# Prompt\n")
        self.write("tracked.txt", "one\n")
        subprocess.run(["git", "add", "tracked.txt"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(
            ["git", "-c", "user.name=AHL Test", "-c", "user.email=ahl@example.test", "commit", "-m", "Initial"],
            cwd=self.root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.write("tracked.txt", "two\n")
        self.write("untracked.txt", "new\n")

        code, output = self.run_cli("project", "status", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["project"]["git"]["found"])
        self.assertTrue(data["project"]["git"]["dot_git_exists"])
        self.assertEqual(data["project"]["git"]["dirty_count"], 1)
        self.assertEqual(data["project"]["git"]["untracked_count"], 2)

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_project_status_detects_prompt_prefixed_commits(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.write(".prompts/PROMPT_01.txt", "# Prompt\n")
        self.write(".prompts/PROMPT_02.txt", "# Prompt\n")
        self.write("done.txt", "done\n")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(
            ["git", "-c", "user.name=AHL Test", "-c", "user.email=ahl@example.test", "commit", "-m", "[PROMPT_01] Finish fixture"],
            cwd=self.root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        code, output = self.run_cli("project", "status", "--json")
        data = json.loads(output)
        summary = data["project"]["next_prompt"]["prompt_prefixed_commit_summary"]

        self.assertEqual(code, 0)
        self.assertEqual(summary["max_prompt_number"], 1)
        self.assertEqual(summary["next_after_highest_prompt_commit"], "PROMPT_02")
        self.assertEqual(data["project"]["next_prompt"]["likely_next_prompt"], "PROMPT_02")
        self.assertEqual(data["project"]["next_prompt"]["confidence"], "medium")
        self.assertEqual(summary["prompt_prefixed_commits"][0]["prompt_numbers"], [1])

    def test_project_status_json_has_stable_fields(self):
        self.write(".prompts/PROMPT_01.txt")

        code, output = self.run_cli("project", "status", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("ok", "ahl_home", "project", "warnings", "problems"):
            self.assertIn(key, data)
        for key in ("root", "git", "promptset", "next_prompt", "files"):
            self.assertIn(key, data["project"])
        self.assertIn("dot_git_exists", data["project"]["git"])
        for key in (
            "prompt_dir_exists",
            "prompt_count",
            "state",
            "lowest_prompt_number",
            "highest_prompt_number",
            "gaps",
            "duplicates",
            "malformed",
            "strict_two_digit",
        ):
            self.assertIn(key, data["project"]["promptset"])
        for key in (
            "next_after_highest_prompt_file",
            "prompt_prefixed_commit_summary",
            "likely_next_prompt",
            "confidence",
            "reason",
        ):
            self.assertIn(key, data["project"]["next_prompt"])

    def test_lifecycle_snippets_normalizes_prompt_numbers(self):
        self.assertEqual(ahl.normalize_prompt_id("84"), "PROMPT_84")
        self.assertEqual(ahl.normalize_prompt_id("PROMPT_84"), "PROMPT_84")
        self.assertEqual(ahl.normalize_prompt_id("PROMPT_84.txt"), "PROMPT_84")

    def test_lifecycle_snippets_generates_run_snippet_path(self):
        self.write("AGENT.md", "# Agent\n")
        self.write(".prompts/PROMPT_84.txt", "# Prompt\n")

        code, output = self.run_cli("lifecycle", "snippets", "84", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["snippets"]["run"], "Load AGENT.md, then run .prompts/PROMPT_84.txt")
        self.assertEqual(data["prompt"]["path"], ".prompts/PROMPT_84.txt")

    def test_lifecycle_audit_snippet_preserves_agent_context_update_doctrine(self):
        self.write("AGENT.md", "# Agent\n")
        (self.root / ".context").mkdir()
        self.write(".prompts/PROMPT_84.txt", "# Prompt\n")

        code, output = self.run_cli("lifecycle", "snippets", "PROMPT_84", "--json")
        data = json.loads(output)
        snippet = data["snippets"]["audit_next_readiness_context_update"]

        self.assertEqual(code, 0)
        self.assertIn("Does everything look appropriately implemented for PROMPT_84?", snippet)
        self.assertIn("Do not run\nPROMPT_85", snippet)
        self.assertIn("whether AGENT.md or .context/ should be updated", snippet)
        self.assertIn("Do not update them just because they ran.", snippet)

    def test_lifecycle_commit_plan_snippet_includes_heredoc_guidance(self):
        self.write("AGENT.md", "# Agent\n")

        code, output = self.run_cli("lifecycle", "snippets", "PROMPT_84.txt", "--json")
        data = json.loads(output)
        snippet = data["snippets"]["commit_plan"]

        self.assertEqual(code, 0)
        self.assertIn("heredoc EOF", snippet)
        self.assertIn("no \\n end up in the commit string", snippet)
        self.assertIn("with [PROMPT_84]", snippet)
        self.assertNotIn("Co-authored-by", snippet)

    def test_lifecycle_commit_check_snippet_includes_required_checks(self):
        self.write("AGENT.md", "# Agent\n")

        code, output = self.run_cli("lifecycle", "snippets", "84", "--json")
        data = json.loads(output)
        snippet = data["snippets"]["commit_check"]

        self.assertEqual(code, 0)
        for expected in (
            "Tim Pope-style subject/body formatting",
            "wrapped secondary/body lines",
            "no literal `\\n` sequences",
            "no co-author trailer",
            "prefix such as `[PROMPT_84]` is present",
            "commit grouping matches the implemented changes",
            "amend or rebase guidance is suggested only when there is a clear issue",
        ):
            self.assertIn(expected, snippet)

    def test_lifecycle_snippets_selects_claude_bootstrap(self):
        self.write("CLAUDE.md", "# Claude\n")

        code, output = self.run_cli("lifecycle", "snippets", "84", "--bootstrap", "CLAUDE.md", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["configuration"]["bootstrap_doc"], "CLAUDE.md")
        self.assertEqual(data["snippets"]["run"], "Load CLAUDE.md, then run .prompts/PROMPT_84.txt")

    def test_lifecycle_snippets_supports_no_bootstrap(self):
        self.write("AGENT.md", "# Agent\n")

        code, output = self.run_cli("lifecycle", "snippets", "84", "--bootstrap", "none", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertIsNone(data["configuration"]["bootstrap_doc"])
        self.assertEqual(data["snippets"]["run"], "Run .prompts/PROMPT_84.txt")

    def test_lifecycle_snippets_json_has_stable_fields(self):
        self.write("AGENT.md", "# Agent\n")
        self.write(".prompts/PROMPT_84.txt", "# Prompt\n")

        code, output = self.run_cli("lifecycle", "snippets", "PROMPT_84", "--include-repair", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("ok", "ahl_home", "project", "prompt", "configuration", "snippets", "warnings", "problems"):
            self.assertIn(key, data)
        for key in ("input", "id", "number", "path", "exists"):
            self.assertIn(key, data["prompt"])
        for key in (
            "run",
            "audit_next_readiness_context_update",
            "commit_plan",
            "make_commits",
            "commit_check",
            "repair",
        ):
            self.assertIn(key, data["snippets"])

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_lifecycle_context_check_no_changed_files_has_no_candidates(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.write(".prompts/PROMPT_84.txt", "# Prompt\n")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(
            ["git", "-c", "user.name=AHL Test", "-c", "user.email=ahl@example.test", "commit", "-m", "Initial"],
            cwd=self.root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        code, output = self.run_cli("lifecycle", "context-check", "PROMPT_84", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["changed_paths"], [])
        self.assertEqual(data["candidates"], [])
        self.assertIn("no context update candidates", data["conclusion"])
        self.assertTrue(data["read_only"])

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_lifecycle_context_check_docs_and_commands_produce_questions(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.write(".prompts/PROMPT_84.txt", "# Prompt\n")
        self.write("docs/workflow.md", "# Workflow\n")
        self.write("scripts/ahl.py", "# helper\n")

        code, output = self.run_cli("lifecycle", "context-check", "84", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        paths = {candidate["path"] for candidate in data["candidates"]}
        self.assertIn("docs/workflow.md", paths)
        self.assertIn("scripts/ahl.py", paths)
        self.assertTrue(any("AGENT.md" in question for question in data["questions"]))

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_lifecycle_context_check_test_only_changes_do_not_force_candidates(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.write(".prompts/PROMPT_84.txt", "# Prompt\n")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(
            ["git", "-c", "user.name=AHL Test", "-c", "user.email=ahl@example.test", "commit", "-m", "Initial"],
            cwd=self.root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.write("tests/test_feature.py", "def test_feature():\n    pass\n")

        code, output = self.run_cli("lifecycle", "context-check", "PROMPT_84", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["candidates"], [])
        self.assertEqual(data["ignored_changes"], [{"path": "tests/test_feature.py", "kind": "test"}])

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_lifecycle_context_check_json_has_stable_fields(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.write(".prompts/PROMPT_84.txt", "# Prompt\n")
        self.write("README.md", "# Project\n")

        code, output = self.run_cli("lifecycle", "context-check", "PROMPT_84.txt", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in (
            "ok",
            "ahl_home",
            "project",
            "prompt",
            "git",
            "changed_paths",
            "candidates",
            "ignored_changes",
            "questions",
            "conclusion",
            "read_only",
            "warnings",
            "problems",
        ):
            self.assertIn(key, data)
        for key in ("path", "kind", "confidence", "reason", "questions"):
            self.assertIn(key, data["candidates"][0])

    def test_lifecycle_run_range_resolves_valid_external_project(self):
        self.write("AGENT.md", "# Agent\n")
        self.write(".prompts/PROMPT_18.txt", "# Prompt 18\n## Validation\n- python3 -m unittest tests/test_ahl.py\n")
        self.write(".prompts/PROMPT_19.txt", "# Prompt 19\n")

        code, output = self.run_cli("lifecycle", "run-range", "18", "19", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["mode"], "dry-run")
        self.assertTrue(data["dry_run"])
        self.assertEqual(Path(data["project"]["root"]).resolve(), self.root.resolve())
        self.assertEqual(data["prompt_ids"], ["PROMPT_18", "PROMPT_19"])
        self.assertEqual([step["prompt_id"] for step in data["steps"]], ["PROMPT_18", "PROMPT_19"])
        self.assertEqual(data["next_prompt"], "PROMPT_18")

    def test_lifecycle_run_range_reports_missing_prompt(self):
        self.write(".prompts/PROMPT_18.txt", "# Prompt 18\n")
        self.write(".prompts/PROMPT_20.txt", "# Prompt 20\n")

        code, output = self.run_cli("lifecycle", "run-range", "18", "20", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertIn("PROMPT_19", data["missing_prompt_ids"])
        self.assertEqual(data["stop_reason"], "range-validation-failed")
        self.assertTrue(any("missing prompt file: .prompts/PROMPT_19.txt" == problem for problem in data["problems"]))

    def test_lifecycle_run_range_rejects_reversed_range(self):
        self.write(".prompts/PROMPT_18.txt", "# Prompt 18\n")

        code, output = self.run_cli("lifecycle", "run-range", "20", "18", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("reversed" in problem for problem in data["problems"]))
        self.assertEqual(data["steps"], [])

    def test_lifecycle_run_range_rejects_malformed_prompt_filenames(self):
        self.write(".prompts/PROMPT_18.txt", "# Prompt 18\n")
        self.write(".prompts/PROMPT_19.txt", "# Prompt 19\n")
        self.write(".prompts/PROMPT_19_notes.txt", "# Notes\n")

        code, output = self.run_cli("lifecycle", "run-range", "18", "19", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertIn("PROMPT_19_notes.txt", data["malformed_prompt_filenames"])

    def test_lifecycle_run_range_default_does_not_write_target_project(self):
        self.write("AGENT.md", "# Agent\n")
        self.write(".prompts/PROMPT_18.txt", "# Prompt 18\n")

        before = sorted(path.relative_to(self.root).as_posix() for path in self.root.rglob("*"))
        code, output = self.run_cli("lifecycle", "run-range", "18", "18", "--json")
        after = sorted(path.relative_to(self.root).as_posix() for path in self.root.rglob("*"))
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertIsNone(data["planned_artifact"])
        self.assertEqual(after, before)

    def test_lifecycle_run_range_writes_explicit_artifact(self):
        self.write(".prompts/PROMPT_18.txt", "# Prompt 18\n")
        artifact = self.root / "plans" / "run-range.json"

        code, output = self.run_cli(
            "lifecycle",
            "run-range",
            "18",
            "18",
            "--artifact",
            str(artifact),
            "--plan-id",
            "fixture-plan",
            "--json",
        )
        data = json.loads(output)
        written = json.loads(artifact.read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertTrue(artifact.is_file())
        self.assertEqual(written["plan_id"], "fixture-plan")
        self.assertEqual(written["prompt_ids"], ["PROMPT_18"])

    def test_lifecycle_run_range_phases_include_commit_check_and_fresh_boundary(self):
        self.write(".prompts/PROMPT_18.txt", "# Prompt 18\n")

        code, output = self.run_cli("lifecycle", "run-range", "18", "18", "--json")
        data = json.loads(output)
        step = data["steps"][0]

        self.assertEqual(code, 0)
        self.assertIn("commit_check", step["phase_order"])
        self.assertIn("fresh_session_boundary", step["phase_order"])
        self.assertTrue(any(phase["name"] == "commit_check" for phase in step["phases"]))
        self.assertIn("fresh assistant session", step["fresh_session_boundary"])

    def test_lifecycle_run_range_json_has_stable_fields(self):
        self.write(".prompts/PROMPT_18.txt", "# Prompt 18\n")

        code, output = self.run_cli("lifecycle", "run-range", "PROMPT_18", "PROMPT_18.txt", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in (
            "ok",
            "schema",
            "plan_id",
            "mode",
            "dry_run",
            "project",
            "requested_range",
            "prompt_ids",
            "steps",
            "next_prompt",
            "safety_notes",
            "problems",
        ):
            self.assertIn(key, data)

    def test_promptset_detects_gap_or_malformed_filename(self):
        self.write(".prompts/PROMPT_01.txt")
        self.write(".prompts/PROMPT_03.txt")
        self.write(".prompts/PROMPT_4.txt")

        code, output = self.run_cli("promptset", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertIn(2, data["gaps"])
        self.assertIn("PROMPT_4.txt", data["malformed"])

    def prompt_text(self, prompt_id, next_id=None, include_endcap=True):
        lines = [
            f"# {prompt_id} - Fixture Prompt",
            "",
            "## Startup Instructions",
            "",
            "Inspect repo state before editing.",
            "",
            "## Required Deliverables",
            "",
            "- Update a fixture file.",
            "",
            "## Constraints",
            "",
            "- Use only local files.",
            "",
            "## Validation",
            "",
            "Run fixture validation.",
            "",
        ]
        if include_endcap:
            lines.extend(
                [
                    "## Endcap",
                    "",
                    "Audit deliverables before ending.",
                ]
            )
            if next_id:
                lines.append(f"Inspect `.prompts/{next_id}.txt` before closeout.")
        return "\n".join(lines) + "\n"

    def test_promptset_lint_accepts_valid_promptset(self):
        self.write(".prompts/PROMPT_01.txt", self.prompt_text("PROMPT_01", "PROMPT_02"))
        self.write(".prompts/PROMPT_02.txt", self.prompt_text("PROMPT_02"))

        code, output = self.run_cli("promptset", "lint", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["summary"]["prompt_count"], 2)
        self.assertEqual(data["summary"]["problem_count"], 0)

    def test_promptset_lint_detects_missing_endcap(self):
        self.write(".prompts/PROMPT_01.txt", self.prompt_text("PROMPT_01", include_endcap=False))

        code, output = self.run_cli("promptset", "lint", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("missing endcap" in problem for problem in data["problems"]))

    def test_promptset_lint_detects_bad_filename(self):
        self.write(".prompts/PROMPT_1.txt", self.prompt_text("PROMPT_01"))

        code, output = self.run_cli("promptset", "lint", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertIn("PROMPT_1.txt", data["numbering"]["malformed"])
        self.assertTrue(any("malformed prompt filename" in problem for problem in data["problems"]))

    def test_promptset_lint_json_has_stable_fields(self):
        self.write(".prompts/PROMPT_01.txt", self.prompt_text("PROMPT_01"))

        code, output = self.run_cli("promptset", "lint", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("ok", "prompt_dir", "summary", "problems", "numbering", "registry", "prompts"):
            self.assertIn(key, data)
        for key in ("filename", "checks", "missing", "readiness_score", "readiness_present", "readiness_total"):
            self.assertIn(key, data["prompts"][0])

    def test_promptset_lint_detects_missing_next_prompt_reference(self):
        self.write(".prompts/PROMPT_01.txt", self.prompt_text("PROMPT_01"))
        self.write(".prompts/PROMPT_02.txt", self.prompt_text("PROMPT_02"))

        code, output = self.run_cli("promptset", "lint", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertTrue(any("missing next prompt reference" in problem for problem in data["problems"]))

    def test_validate_reports_quality_foundations_and_promptset(self):
        self.add_foundations()
        self.write(".prompts/PROMPT_01.txt")
        self.write(".prompts/PROMPT_02.txt")

        code, output = self.run_cli("validate", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertIn("checks", data)
        self.assertTrue(data["promptset"]["strict_two_digit"])

    def test_validate_fails_when_required_quality_foundation_is_missing(self):
        self.add_foundations()
        self.write(".prompts/PROMPT_01.txt")
        shutil.rmtree(self.root / "docs" / "quality")

        code, output = self.run_cli("validate", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("docs/quality" in problem for problem in data["problems"]))

    def write_registry(self, filename, items):
        self.write(
            f"registry/{filename}",
            json.dumps(
                {
                    "schema_version": 1,
                    "description": "test registry",
                    "source_of_truth_note": "test files are authoritative",
                    "items": items,
                },
                indent=2,
            ),
        )

    def registry_item(self, item_id, path, **overrides):
        item = {
            "id": item_id,
            "name": item_id.title(),
            "type": "test",
            "path": path,
            "purpose": "Test registry item.",
            "owner_role": "operator",
            "status": "active",
            "inputs": [],
            "outputs": [],
            "related_docs": [],
            "safe_use_notes": "Test only.",
        }
        item.update(overrides)
        return item

    def add_minimal_registries(self):
        self.write(".prompts/PROMPT_01.txt")
        self.write(".prompts/PROMPT_02.txt")
        self.write("docs/README.md", "# Docs\n")
        self.write("docs/roles/orchestrator.md", "# Orchestrator\n")
        self.write("runbooks/fresh-session-prompt-run.md", "# Runbook\n")
        self.write("templates/session-closeout.md", "# Closeout\n")
        self.write("examples/README.md", "# Examples\n")
        self.write("scripts/ahl.py", "# script\n")
        self.write_registry("artifacts.json", [self.registry_item("artifact-docs", "docs/README.md")])
        self.write_registry(
            "prompts.json",
            [
                self.registry_item("PROMPT_01", ".prompts/PROMPT_01.txt", type="prompt"),
                self.registry_item("PROMPT_02", ".prompts/PROMPT_02.txt", type="prompt"),
            ],
        )
        self.write_registry("roles.json", [self.registry_item("role-orchestrator", "docs/roles/orchestrator.md")])
        self.write_registry(
            "routines.json",
            [self.registry_item("routine-prompt-execution", "runbooks/fresh-session-prompt-run.md")],
        )
        self.write_registry("templates.json", [self.registry_item("template-closeout", "templates/session-closeout.md")])
        self.write_registry("examples.json", [self.registry_item("example-index", "examples/README.md")])
        self.write_registry("scripts.json", [self.registry_item("script-ahl", "scripts/ahl.py")])

    def test_registry_check_accepts_valid_curated_indexes(self):
        self.add_minimal_registries()

        code, output = self.run_cli("registry", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(len(data["registries"]), 7)

    def test_registry_check_detects_missing_field_and_path(self):
        self.add_minimal_registries()
        bad_item = self.registry_item("bad", "missing.md")
        bad_item.pop("purpose")
        self.write_registry("roles.json", [bad_item])

        code, output = self.run_cli("registry", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("missing fields: purpose" in problem for problem in data["problems"]))
        self.assertTrue(any("referenced path does not exist: missing.md" in problem for problem in data["problems"]))

    def test_registry_check_detects_prompt_order_mismatch(self):
        self.add_minimal_registries()
        self.write_registry(
            "prompts.json",
            [
                self.registry_item("PROMPT_02", ".prompts/PROMPT_02.txt", type="prompt"),
                self.registry_item("PROMPT_01", ".prompts/PROMPT_01.txt", type="prompt"),
            ],
        )

        code, output = self.run_cli("registry", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("ordering does not match" in problem for problem in data["problems"]))

    def driver_item(self, driver_id="codex", **overrides):
        item = self.registry_item(driver_id, f"fixtures/assistant-drivers/{driver_id}.json", type="assistant-driver")
        item.update(
            {
                "display_name": f"{driver_id.title()} Driver",
                "driver_kind": "subscription-cli",
                "executable_name": driver_id,
                "supported_invocation_modes": ["interactive"],
                "prompt_input_methods": ["stdin"],
                "structured_output_support": {"status": "unknown"},
                "final_message_capture_support": {"status": "unknown"},
                "sandbox_approval_controls": "requires verification",
                "model_selection_support": "requires verification",
                "reasoning_selection_support": "requires verification",
                "fresh_session_behavior": "new invocation",
                "resume_behavior": "unknown",
                "capability_probe": {"path_check": True, "help_args": ["--help"], "help_only_safe": True},
                "known_limitations": ["not verified"],
                "unsupported_operations": ["live calls during probes"],
            }
        )
        item.update(overrides)
        return item

    def write_driver_registry(self, items=None):
        if items is None:
            items = [
                self.driver_item("codex"),
                self.driver_item("manual", driver_kind="manual", executable_name=None, prompt_input_methods=["manual"]),
            ]
        for item in items:
            path = item.get("path")
            if isinstance(path, str) and path.startswith("fixtures/"):
                self.write(path, json.dumps({"id": item["id"]}))
        self.write_registry("assistant-drivers.json", items)

    def test_driver_check_accepts_valid_registry(self):
        self.write_driver_registry()

        code, output = self.run_cli("driver", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual([driver["id"] for driver in data["drivers"]], ["codex", "manual"])

    def test_driver_check_reports_malformed_registry(self):
        bad = self.driver_item("codex")
        bad.pop("driver_kind")
        self.write_driver_registry([bad])

        code, output = self.run_cli("driver", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("missing driver fields: driver_kind" in problem for problem in data["problems"]))

    def test_driver_list_json_has_stable_fields(self):
        self.write_driver_registry()

        code, output = self.run_cli("driver", "list", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("ok", "drivers", "checks", "problems"):
            self.assertIn(key, data)
        for key in ("id", "display_name", "driver_kind", "executable_name", "supported_invocation_modes"):
            self.assertIn(key, data["drivers"][0])

    def test_unknown_driver_probe_fails_clearly(self):
        self.write_driver_registry()

        code, output = self.run_cli("driver", "probe", "missing", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertIn("unknown assistant driver: missing", data["problems"])

    def test_help_only_probe_degrades_when_executable_missing(self):
        self.write_driver_registry()

        with mock.patch("shutil.which", return_value=None):
            code, output = self.run_cli("driver", "probe", "codex", "--help-only", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertFalse(data["probe"]["available"])
        self.assertTrue(any("executable not found on PATH: codex" in problem for problem in data["problems"]))

    def test_pi_driver_registry_shape_is_external_and_guarded(self):
        pi = self.driver_item(
            "pi",
            driver_kind="external-harness",
            executable_name="pi",
            supported_invocation_modes=["interactive", "print", "json", "rpc-requires-verification"],
            prompt_input_methods=["argument", "stdin", "tool_specific_option"],
            live_run_status="manual-confirmation-required",
            manual_confirmation_required=True,
        )
        self.write_driver_registry([pi])

        code, output = self.run_cli("driver", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["drivers"][0]["id"], "pi")
        self.assertEqual(data["drivers"][0]["driver_kind"], "external-harness")
        self.assertEqual(data["drivers"][0]["live_run_status"], "manual-confirmation-required")
        self.assertTrue(data["drivers"][0]["manual_confirmation_required"])

    def test_pi_help_only_probe_degrades_when_executable_missing(self):
        pi = self.driver_item("pi", driver_kind="external-harness", executable_name="pi")
        self.write_driver_registry([pi])

        with mock.patch("shutil.which", return_value=None):
            code, output = self.run_cli("driver", "probe", "pi", "--help-only", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertFalse(data["probe"]["available"])
        self.assertTrue(any("pi: executable not found on PATH: pi" in problem for problem in data["problems"]))

    def add_outer_promptset(self):
        self.write(".prompts/PROMPT_01.txt", self.prompt_text("PROMPT_01", "PROMPT_02"))
        self.write(".prompts/PROMPT_02.txt", self.prompt_text("PROMPT_02", "PROMPT_03"))
        self.write(".prompts/PROMPT_03.txt", self.prompt_text("PROMPT_03"))
        self.write_driver_registry()

    def test_outer_plan_creates_valid_prompt_range(self):
        self.add_outer_promptset()

        code, output = self.run_cli(
            "outer",
            "plan",
            "--from",
            "PROMPT_01",
            "--count",
            "2",
            "--driver",
            "manual",
            "--plan-id",
            "fixture-plan",
            "--json",
        )
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["plan_id"], "fixture-plan")
        self.assertEqual([item["prompt_id"] for item in data["prompts"]], ["PROMPT_01", "PROMPT_02"])
        self.assertTrue((self.root / "runs" / "outer-loop" / "fixture-plan" / "plan.json").exists())

    def test_outer_plan_missing_prompt_in_range_fails(self):
        self.write(".prompts/PROMPT_01.txt", self.prompt_text("PROMPT_01"))
        self.write_driver_registry()

        code, output = self.run_cli(
            "outer",
            "plan",
            "--from",
            "PROMPT_01",
            "--count",
            "2",
            "--driver",
            "manual",
            "--json",
        )
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("missing prompt file: .prompts/PROMPT_02.txt" in problem for problem in data["problems"]))

    def test_outer_plan_invalid_driver_fails(self):
        self.add_outer_promptset()

        code, output = self.run_cli(
            "outer",
            "plan",
            "--from",
            "PROMPT_01",
            "--count",
            "1",
            "--driver",
            "missing",
            "--json",
        )
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertIn("unknown assistant driver: missing", data["problems"])

    def test_pi_outer_plan_dry_run_works(self):
        self.add_outer_promptset()
        pi = self.driver_item(
            "pi",
            driver_kind="external-harness",
            executable_name="pi",
            supported_invocation_modes=["interactive", "print", "json"],
            prompt_input_methods=["argument", "stdin", "tool_specific_option"],
            live_run_status="manual-confirmation-required",
            manual_confirmation_required=True,
        )
        self.write_driver_registry([pi])

        code, output = self.run_cli(
            "outer",
            "plan",
            "--from",
            "PROMPT_01",
            "--count",
            "1",
            "--driver",
            "pi",
            "--plan-id",
            "pi-plan",
            "--json",
        )
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["driver"]["id"], "pi")
        self.assertEqual(data["driver"]["driver_kind"], "external-harness")
        self.assertTrue((self.root / "runs" / "outer-loop" / "pi-plan" / "plan.json").exists())

    def test_outer_plan_next_selects_fixture_promptset_start(self):
        self.add_outer_promptset()

        code, output = self.run_cli(
            "outer",
            "plan",
            "--next",
            "2",
            "--driver",
            "manual",
            "--plan-id",
            "next-two",
            "--json",
        )
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["requested_range"]["mode"], "next")
        self.assertEqual([item["prompt_id"] for item in data["prompts"]], ["PROMPT_01", "PROMPT_02"])

    def test_outer_dry_run_pass_json_has_stable_fields(self):
        self.add_outer_promptset()
        code, output = self.run_cli(
            "outer",
            "plan",
            "--from",
            "PROMPT_01",
            "--count",
            "1",
            "--driver",
            "manual",
            "--plan-id",
            "dry-run-pass",
            "--json",
        )
        self.assertEqual(code, 0)
        plan = json.loads(output)["artifact"]

        code2, output2 = self.run_cli("outer", "dry-run", "--plan", plan, "--json")
        data = json.loads(output2)

        self.assertEqual(code2, 0)
        self.assertTrue(data["ok"])
        for key in ("ok", "plan_id", "steps", "problems"):
            self.assertIn(key, data)
        for key in ("prompt_id", "path", "status", "validation_commands", "problems"):
            self.assertIn(key, data["steps"][0])

    def test_outer_dry_run_detects_missing_prompt_referenced_by_plan(self):
        self.add_outer_promptset()
        plan = {
            "plan_id": "missing-prompt-plan",
            "driver": {"id": "manual"},
            "required_ahl_checks": ["python3 scripts/ahl.py doctor"],
            "stop_conditions": ["missing_prompt_file"],
            "prompts": [
                {
                    "prompt_id": "PROMPT_09",
                    "path": ".prompts/PROMPT_09.txt",
                    "validation_commands": ["python3 -m unittest tests/test_ahl.py"],
                }
            ],
        }
        self.write("runs/outer-loop/missing-prompt-plan/plan.json", json.dumps(plan))

        code, output = self.run_cli(
            "outer",
            "dry-run",
            "--plan",
            "runs/outer-loop/missing-prompt-plan/plan.json",
            "--json",
        )
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertEqual(data["steps"][0]["status"], "fail")
        self.assertTrue(any("referenced path does not exist" in problem for problem in data["problems"]))

    def test_outer_plan_refuses_artifact_overwrite(self):
        self.add_outer_promptset()
        args = (
            "outer",
            "plan",
            "--from",
            "PROMPT_01",
            "--count",
            "1",
            "--driver",
            "manual",
            "--plan-id",
            "overwrite-plan",
            "--json",
        )

        code, _ = self.run_cli(*args)
        self.assertEqual(code, 0)
        code2, output2 = self.run_cli(*args)
        data = json.loads(output2)

        self.assertEqual(code2, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("refusing to overwrite" in problem for problem in data["problems"]))

    def git_status_ok(self, lines=""):
        return subprocess.CompletedProcess(["git"], 0, stdout=lines, stderr="")

    def test_outer_gate_existing_prompt_no_plan_needs_human_review(self):
        self.write(".prompts/PROMPT_01.txt", self.prompt_text("PROMPT_01", "PROMPT_02"))
        self.write(".prompts/PROMPT_02.txt", self.prompt_text("PROMPT_02"))

        with mock.patch.object(ahl, "run_git", return_value=(self.git_status_ok(""), None)):
            code, output = self.run_cli("outer", "gate", "PROMPT_01", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["status"], "needs-human-review")
        self.assertEqual(data["prompt_id"], "PROMPT_01")
        self.assertEqual(data["next_prompt_readiness"]["status"], "ready")

    def test_outer_gate_detects_missing_prompt(self):
        self.write(".prompts/PROMPT_02.txt", self.prompt_text("PROMPT_02"))

        with mock.patch.object(ahl, "run_git", return_value=(self.git_status_ok(""), None)):
            code, output = self.run_cli("outer", "gate", "PROMPT_01", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "blocked")
        self.assertTrue(any("missing prompt file: .prompts/PROMPT_01.txt" in problem for problem in data["problems"]))

    def test_outer_gate_detects_missing_next_prompt_when_required(self):
        self.write(".prompts/PROMPT_01.txt", self.prompt_text("PROMPT_01"))

        with mock.patch.object(ahl, "run_git", return_value=(self.git_status_ok(""), None)):
            code, output = self.run_cli("outer", "gate", "PROMPT_01", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "blocked")
        self.assertEqual(data["next_prompt_readiness"]["status"], "blocked")
        self.assertTrue(any("missing next prompt file: .prompts/PROMPT_02.txt" in problem for problem in data["problems"]))

    def test_outer_gate_records_skipped_validations_honestly(self):
        self.write(".prompts/PROMPT_01.txt", self.prompt_text("PROMPT_01", "PROMPT_02"))
        self.write(".prompts/PROMPT_02.txt", self.prompt_text("PROMPT_02"))
        plan = {
            "plan_id": "gate-plan",
            "prompts": [
                {
                    "prompt_id": "PROMPT_01",
                    "path": ".prompts/PROMPT_01.txt",
                    "validation_commands": ["python3 -m unittest tests/test_ahl.py"],
                }
            ],
            "required_ahl_checks": ["python3 scripts/ahl.py promptset lint"],
            "commit_policy": "none",
        }
        self.write("runs/outer-loop/gate-plan/plan.json", json.dumps(plan))

        with mock.patch.object(ahl, "run_git", return_value=(self.git_status_ok(""), None)):
            code, output = self.run_cli("outer", "gate", "PROMPT_01", "--plan", "runs/outer-loop/gate-plan/plan.json", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["validation_commands"]["source"], "plan")
        self.assertEqual(data["validation_outcomes"][0]["status"], "skipped")
        self.assertIn("record-only mode", data["validation_outcomes"][0]["reason"])
        self.assertEqual(data["next_prompt_readiness"]["status"], "not-required")

    def test_outer_gate_json_has_stable_fields(self):
        self.write(".prompts/PROMPT_01.txt", self.prompt_text("PROMPT_01", "PROMPT_02"))
        self.write(".prompts/PROMPT_02.txt", self.prompt_text("PROMPT_02"))

        with mock.patch.object(ahl, "run_git", return_value=(self.git_status_ok("?? notes.md\n"), None)):
            code, output = self.run_cli("outer", "gate", "PROMPT_01", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in (
            "ok",
            "status",
            "prompt_id",
            "changed_files",
            "validation_commands",
            "validation_outcomes",
            "ahl_checks",
            "completion_audit",
            "next_prompt_readiness",
            "handoff",
            "commit_plan",
            "decision",
            "warnings",
            "problems",
        ):
            self.assertIn(key, data)

    def test_outer_gate_represents_unsafe_git_state_without_crashing(self):
        self.write(".prompts/PROMPT_01.txt", self.prompt_text("PROMPT_01", "PROMPT_02"))
        self.write(".prompts/PROMPT_02.txt", self.prompt_text("PROMPT_02"))

        with mock.patch.object(ahl, "run_git", return_value=(self.git_status_ok("UU docs/conflict.md\n"), None)):
            code, output = self.run_cli("outer", "gate", "PROMPT_01", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "unsafe-git-state")
        self.assertTrue(data["git"]["unsafe"])
        self.assertTrue(any("unmerged git status entry" in problem for problem in data["problems"]))

    def create_outer_plan_fixture(self, plan_id="run-plan", driver_id="manual", count=2):
        self.add_outer_promptset()
        code, output = self.run_cli(
            "outer",
            "plan",
            "--from",
            "PROMPT_01",
            "--count",
            str(count),
            "--driver",
            driver_id,
            "--plan-id",
            plan_id,
            "--json",
        )
        self.assertEqual(code, 0)
        return json.loads(output)["artifact"]

    def passing_gate(self, prompt_id):
        return {
            "ok": True,
            "status": "pass",
            "prompt_id": prompt_id,
            "decision": "continue",
            "problems": [],
            "warnings": [],
        }

    def test_outer_run_dry_run_does_not_invoke_external_commands(self):
        plan = self.create_outer_plan_fixture(count=1)

        with mock.patch.object(ahl.subprocess, "run", side_effect=AssertionError("external command invoked")):
            with mock.patch.object(ahl, "outer_gate_report", return_value=self.passing_gate("PROMPT_01")):
                code, output = self.run_cli("outer", "run", "--plan", plan, "--dry-run", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["mode"], "dry-run")
        self.assertEqual(data["steps"][0]["driver"]["status"], "not-invoked")

    def test_outer_run_manual_driver_creates_ledger_entry(self):
        plan = self.create_outer_plan_fixture(count=1)

        with mock.patch.object(ahl, "outer_gate_report", return_value=self.passing_gate("PROMPT_01")):
            code, output = self.run_cli("outer", "run", "--plan", plan, "--execute", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["steps"][0]["driver"]["status"], "manual-action-required")
        self.assertTrue((self.root / data["artifact"]).exists())

    def test_outer_run_live_execution_requires_execute(self):
        plan = self.create_outer_plan_fixture(plan_id="live-default", driver_id="codex", count=1)

        with mock.patch.object(ahl.subprocess, "run", side_effect=AssertionError("external command invoked")):
            with mock.patch.object(ahl, "outer_gate_report", return_value=self.passing_gate("PROMPT_01")):
                code, output = self.run_cli("outer", "run", "--plan", plan, "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["mode"], "dry-run")
        self.assertEqual(data["steps"][0]["driver"]["status"], "not-invoked")

    def test_outer_run_pi_live_invocation_is_guarded(self):
        self.add_outer_promptset()
        pi = self.driver_item(
            "pi",
            driver_kind="external-harness",
            executable_name="pi",
            supported_invocation_modes=["interactive", "print", "json"],
            prompt_input_methods=["argument", "stdin", "tool_specific_option"],
            live_run_status="manual-confirmation-required",
            manual_confirmation_required=True,
        )
        self.write_driver_registry([pi])
        code, output = self.run_cli(
            "outer",
            "plan",
            "--from",
            "PROMPT_01",
            "--count",
            "1",
            "--driver",
            "pi",
            "--plan-id",
            "pi-guarded",
            "--json",
        )
        self.assertEqual(code, 0)
        plan = json.loads(output)["artifact"]

        with mock.patch.object(ahl.subprocess, "run", side_effect=AssertionError("external command invoked")):
            code, output = self.run_cli("outer", "run", "--plan", plan, "--execute", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "driver-failed")
        self.assertEqual(data["steps"][0]["driver"]["status"], "driver-failed")
        self.assertTrue(any("manual confirmation" in problem for problem in data["steps"][0]["problems"]))

    def test_outer_run_pi_dry_run_never_invokes_executable(self):
        self.add_outer_promptset()
        pi = self.driver_item(
            "pi",
            driver_kind="external-harness",
            executable_name="pi",
            supported_invocation_modes=["interactive", "print", "json"],
            prompt_input_methods=["argument", "stdin", "tool_specific_option"],
            live_run_status="manual-confirmation-required",
            manual_confirmation_required=True,
        )
        self.write_driver_registry([pi])
        code, output = self.run_cli(
            "outer",
            "plan",
            "--from",
            "PROMPT_01",
            "--count",
            "1",
            "--driver",
            "pi",
            "--plan-id",
            "pi-dry-run",
            "--json",
        )
        self.assertEqual(code, 0)
        plan = json.loads(output)["artifact"]

        with mock.patch.object(ahl.subprocess, "run", side_effect=AssertionError("external command invoked")):
            with mock.patch.object(ahl, "outer_gate_report", return_value=self.passing_gate("PROMPT_01")):
                code, output = self.run_cli("outer", "run", "--plan", plan, "--dry-run", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["driver"]["id"], "pi")
        self.assertEqual(data["steps"][0]["driver"]["status"], "not-invoked")

    def test_outer_run_max_prompts_limits_execution(self):
        plan = self.create_outer_plan_fixture(count=2)

        with mock.patch.object(ahl, "outer_gate_report", return_value=self.passing_gate("PROMPT_01")):
            code, output = self.run_cli("outer", "run", "--plan", plan, "--max-prompts", "1", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(len(data["steps"]), 1)
        self.assertEqual(data["steps"][0]["prompt_id"], "PROMPT_01")

    def test_outer_run_driver_failure_records_and_stops(self):
        plan = self.create_outer_plan_fixture(plan_id="driver-fail", driver_id="codex", count=2)
        failure = subprocess.CompletedProcess(["codex"], 2, stdout="", stderr="boom")

        with mock.patch.object(ahl.subprocess, "run", return_value=failure):
            code, output = self.run_cli("outer", "run", "--plan", plan, "--execute", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "driver-failed")
        self.assertEqual(len(data["steps"]), 1)
        self.assertEqual(data["steps"][0]["driver"]["returncode"], 2)

    def test_outer_run_gate_failure_stops_subsequent_steps(self):
        plan = self.create_outer_plan_fixture(count=2)
        gate = {
            "ok": False,
            "status": "failed-validation",
            "prompt_id": "PROMPT_01",
            "decision": "stop",
            "problems": ["failed check"],
            "warnings": [],
        }

        with mock.patch.object(ahl, "outer_gate_report", return_value=gate):
            code, output = self.run_cli("outer", "run", "--plan", plan, "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "failed-validation")
        self.assertEqual(len(data["steps"]), 1)

    def test_outer_run_prompt_payload_includes_required_guardrails(self):
        plan = self.create_outer_plan_fixture(count=1)

        with mock.patch.object(ahl, "outer_gate_report", return_value=self.passing_gate("PROMPT_01")):
            code, output = self.run_cli("outer", "run", "--plan", plan, "--json")
        data = json.loads(output)
        payload = (self.root / data["steps"][0]["payload_artifact"]).read_text(encoding="utf-8")

        self.assertEqual(code, 0)
        self.assertIn("Run exactly one prompt file", payload)
        self.assertIn("AGENT.md", payload)
        self.assertIn("Do not commit", payload)
        self.assertIn("Preserve unrelated", payload)
        self.assertIn("Do not store raw transcripts", payload)

    def test_outer_run_json_has_stable_fields(self):
        plan = self.create_outer_plan_fixture(count=1)

        with mock.patch.object(ahl, "outer_gate_report", return_value=self.passing_gate("PROMPT_01")):
            code, output = self.run_cli("outer", "run", "--plan", plan, "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("ok", "status", "run_id", "plan_id", "mode", "driver", "steps", "problems"):
            self.assertIn(key, data)
        for key in ("prompt_id", "status", "payload_artifact", "driver", "gate"):
            self.assertIn(key, data["steps"][0])

    def write_outer_ledger(self, run_id="fixture-run", status="interrupted", steps=None):
        if steps is None:
            steps = [
                {"index": 1, "prompt_id": "PROMPT_01", "status": "completed"},
                {"index": 2, "prompt_id": "PROMPT_02", "status": "pending"},
            ]
        ledger = {
            "ok": status == "completed",
            "status": status,
            "run_id": run_id,
            "plan_id": "fixture-plan",
            "mode": "dry-run",
            "driver": {"id": "manual"},
            "steps": steps,
            "resume_pointer": {"next_prompt": "PROMPT_02", "completed_prompts": ["PROMPT_01"], "pending_prompts": ["PROMPT_02"]},
            "stop_reason": "user-interrupted" if status == "interrupted" else status,
            "recovery_recommendation": "Resume from PROMPT_02.",
            "problems": [],
        }
        self.write(f"runs/outer-loop/{run_id}/run-ledger.json", json.dumps(ledger))
        return ledger

    def test_outer_status_reports_completed_blocked_and_interrupted_ledgers(self):
        self.write_outer_ledger("completed-run", "completed", [{"index": 1, "prompt_id": "PROMPT_01", "status": "completed"}])
        self.write_outer_ledger("blocked-run", "blocked", [{"index": 1, "prompt_id": "PROMPT_01", "status": "blocked"}])
        self.write_outer_ledger("interrupted-run", "interrupted")

        for run_id, expected in (("completed-run", "completed"), ("blocked-run", "blocked"), ("interrupted-run", "interrupted")):
            code, output = self.run_cli("outer", "status", "--run", run_id, "--json")
            data = json.loads(output)
            self.assertEqual(code, 0)
            self.assertEqual(data["status"], expected)
            self.assertIn("completed", data["steps"])
            self.assertIn("failed", data["steps"])
            self.assertIn("pending", data["steps"])

    def test_outer_resume_dry_run_selects_correct_next_prompt(self):
        self.write_outer_ledger("resume-run")
        clean = subprocess.CompletedProcess(["git"], 0, stdout="", stderr="")

        with mock.patch.object(ahl, "run_git", return_value=(clean, None)):
            code, output = self.run_cli("outer", "resume", "--run", "resume-run", "--dry-run", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["next_prompt"], "PROMPT_02")
        self.assertEqual(data["completed_prompts"], ["PROMPT_01"])

    def test_outer_resume_refuses_unsafe_git_state(self):
        self.write_outer_ledger("dirty-run")
        dirty = subprocess.CompletedProcess(["git"], 0, stdout="?? scratch.md\n", stderr="")

        with mock.patch.object(ahl, "run_git", return_value=(dirty, None)):
            code, output = self.run_cli("outer", "resume", "--run", "dirty-run", "--dry-run", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "refused")
        self.assertIn("worktree is not clean; refusing resume", data["problems"])

    def test_outer_resume_refuses_malformed_ledger(self):
        self.write("runs/outer-loop/bad-run/run-ledger.json", "{bad json")
        clean = subprocess.CompletedProcess(["git"], 0, stdout="", stderr="")

        with mock.patch.object(ahl, "run_git", return_value=(clean, None)):
            code, output = self.run_cli("outer", "resume", "--run", "bad-run", "--dry-run", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "refused")
        self.assertTrue(any("invalid JSON" in problem for problem in data["problems"]))

    def test_outer_recovery_handoff_refuses_overwrite_by_default(self):
        self.write_outer_ledger("handoff-run")
        self.write("templates/outer-loop/recovery-handoff.md", "Run {{RUN_ID}} next {{NEXT_PROMPT}}\n")
        self.write("runs/outer-loop/handoff-run/recovery-handoff.md", "existing\n")

        code, output = self.run_cli("outer", "recovery-handoff", "--run", "handoff-run", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["created"])
        self.assertIn("recovery handoff already exists: runs/outer-loop/handoff-run/recovery-handoff.md", data["problems"])

    def test_outer_resume_json_has_stable_fields(self):
        self.write_outer_ledger("stable-run")
        clean = subprocess.CompletedProcess(["git"], 0, stdout="", stderr="")

        with mock.patch.object(ahl, "run_git", return_value=(clean, None)):
            code, output = self.run_cli("outer", "resume", "--run", "stable-run", "--dry-run", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("ok", "status", "run_id", "plan_id", "dry_run", "rerun", "next_prompt", "completed_prompts", "failed_prompts", "pending_prompts", "git", "problems"):
            self.assertIn(key, data)

    def write_docs_index(self):
        for dirname in (
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
        ):
            self.write(f"{dirname}/README.md", f"# {dirname}\n")
        self.write(
            "docs/README.md",
            "\n".join(
                [
                    "# Docs",
                    "",
                    "- [Domain packs](../domain-packs/README.md)",
                    "- [Dry runs](../dry-runs/README.md)",
                    "- [Runbooks](../runbooks/README.md)",
                    "- [Templates](../templates/README.md)",
                    "- [Scripts](../scripts/README.md)",
                    "- [Registry](../registry/README.md)",
                    "- [Examples](../examples/README.md)",
                    "- [Experiments](../experiments/README.md)",
                    "- [Findings](../findings/README.md)",
                    "- [Reports](../reports/README.md)",
                    "- [Role packs](../role-packs/README.md)",
                    "- [Lane playbooks](../lane-playbooks/README.md)",
                    "- [Prompt templates](../prompt-templates/README.md)",
                    "- [Fixtures](../fixtures/README.md)",
                    "- [Memory](../memory/README.md)",
                ]
            )
            + "\n",
        )

    def test_docs_check_accepts_valid_local_markdown_link(self):
        self.write_docs_index()
        self.write("docs/topic.md", "[Next](next.md)\n")
        self.write("docs/next.md", "# Next\n")

        code, output = self.run_cli("docs", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["missing_links"], [])
        self.assertTrue(any(link["target"] == "next.md" for link in data["links"]))

    def test_docs_check_detects_broken_local_markdown_link(self):
        self.write_docs_index()
        self.write("docs/topic.md", "[Missing](missing.md)\n")

        code, output = self.run_cli("docs", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any(link["target"] == "missing.md" for link in data["missing_links"]))

    def test_docs_check_ignores_external_links(self):
        self.write_docs_index()
        self.write("docs/topic.md", "[External](https://example.com/missing.md)\n")

        code, output = self.run_cli("docs", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["missing_links"], [])
        self.assertFalse(any(link["target"].startswith("https://") for link in data["links"]))

    def test_docs_check_json_has_stable_fields(self):
        self.write_docs_index()

        code, output = self.run_cli("docs", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in (
            "ok",
            "scan_roots",
            "anchors_validated",
            "checks",
            "problems",
            "scanned_files",
            "links",
            "missing_links",
            "navigation",
            "registry",
        ):
            self.assertIn(key, data)
        self.assertFalse(data["anchors_validated"])

    def test_outer_loop_navigation_links_pi_comparison_docs(self):
        outer_index = (ROOT / "docs" / "outer-loop" / "README.md").read_text(encoding="utf-8")

        self.assertIn("pi-adapter.md", outer_index)
        self.assertIn("pi-vs-ahl.md", outer_index)
        self.assertIn("provider-harness-comparison.md", outer_index)

    def test_docs_check_reports_missing_index_page(self):
        self.write("docs/topic.md", "# Topic\n")

        code, output = self.run_cli("docs", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("missing docs index page" in problem for problem in data["problems"]))

    def write_minimal_fixture_set(self):
        for spec in ahl.FIXTURE_SPECS.values():
            if spec["schema"] is not None:
                self.write(spec["schema"], "{}\n")

        self.write(
            "fixtures/run-records/success.json",
            json.dumps(
                {
                    "prompt_id": "PROMPT_19",
                    "run_id": "fixture-success",
                    "assistant_tool": "codex-fixture",
                    "validation_commands": [],
                    "completion_audit_status": "passed",
                }
            ),
        )
        self.write(
            "fixtures/run-records/blocked.json",
            json.dumps(
                {
                    "prompt_id": "PROMPT_19",
                    "run_id": "fixture-blocked",
                    "assistant_tool": "codex-fixture",
                    "validation_commands": [],
                    "completion_audit_status": "failed",
                }
            ),
        )
        self.write(
            "fixtures/readiness-reports/ready.json",
            json.dumps(
                {
                    "artifact_id": "ready",
                    "active_prompt": "PROMPT_19",
                    "next_prompt": "PROMPT_20",
                    "readiness_label": "ready",
                    "blockers": [],
                    "next_step": "Run the next prompt.",
                }
            ),
        )
        self.write(
            "fixtures/readiness-reports/blocked.json",
            json.dumps(
                {
                    "artifact_id": "blocked",
                    "active_prompt": "PROMPT_19",
                    "next_prompt": "PROMPT_20",
                    "readiness_label": "blocked",
                    "blockers": ["Artificial blocker."],
                    "next_step": "Repair the blocker.",
                }
            ),
        )
        self.write(
            "fixtures/promptset-index/valid.json",
            json.dumps(
                {
                    "ok": True,
                    "prompt_dir": ".prompts",
                    "prompts": [],
                    "filenames": [],
                    "numbers": [],
                    "duplicates": [],
                    "gaps": [],
                }
            ),
        )
        self.write(
            "fixtures/lane-records/single-lane.json",
            json.dumps(
                {
                    "lane_id": "fixture-lane",
                    "prompt_id": "PROMPT_19",
                    "owner_role": "worker",
                    "scope": "Test lane.",
                    "status": "completed",
                    "inputs": [],
                    "outputs": [],
                }
            ),
        )
        self.write(
            "fixtures/traceability/prompt-to-commit.json",
            json.dumps(
                {
                    "traceability_id": "fixture-trace",
                    "prompt_id": "PROMPT_19",
                    "source_artifact": ".prompts/PROMPT_19.txt",
                    "commit_links": [],
                    "validation_evidence": [],
                }
            ),
        )
        self.write(
            "fixtures/traceability/working-tree-summary.json",
            json.dumps(
                {
                    "prompt_id": "PROMPT_20",
                    "prompt_file_exists": True,
                    "branch": "main",
                    "head": "abc1234",
                    "changed_files": [],
                    "docs_changed": False,
                }
            ),
        )
        for driver_id in ("codex", "gemini", "pi"):
            self.write(
                f"fixtures/assistant-drivers/{driver_id}.json",
                json.dumps(
                    {
                        "id": driver_id,
                        "display_name": f"{driver_id.title()} Driver",
                        "driver_kind": "subscription-cli",
                        "executable_name": driver_id,
                        "probe_expectation": "PATH lookup only.",
                        "live_run_status": "deferred",
                    }
                ),
            )
        self.write(
            "fixtures/outer-loop/plans/valid-next-three.json",
            json.dumps(
                {
                    "plan_id": "fixture-valid-next-three",
                    "created_at": "2026-05-06T00:00:00Z",
                    "requested_range": {"mode": "explicit", "from": "PROMPT_01", "count": 2},
                    "prompts": [
                        {
                            "prompt_id": "PROMPT_01",
                            "path": ".prompts/PROMPT_01.txt",
                            "validation_commands": ["python3 -m unittest tests/test_ahl.py"],
                        }
                    ],
                    "driver": {"id": "manual"},
                    "required_ahl_checks": ["python3 scripts/ahl.py doctor"],
                    "stop_conditions": ["missing_prompt_file"],
                    "commit_policy": "none",
                    "run_artifact_dir": "runs/outer-loop/fixture-valid-next-three",
                }
            ),
        )
        self.write(
            "fixtures/outer-loop/plans/missing-prompt.json",
            json.dumps(
                {
                    "plan_id": "fixture-missing-prompt",
                    "created_at": "2026-05-06T00:00:00Z",
                    "requested_range": {"mode": "explicit", "from": "PROMPT_09", "count": 1},
                    "prompts": [
                        {
                            "prompt_id": "PROMPT_09",
                            "path": ".prompts/PROMPT_09.txt",
                            "validation_commands": ["python3 -m unittest tests/test_ahl.py"],
                        }
                    ],
                    "driver": {"id": "manual"},
                    "required_ahl_checks": ["python3 scripts/ahl.py doctor"],
                    "stop_conditions": ["missing_prompt_file"],
                    "commit_policy": "none",
                    "run_artifact_dir": "runs/outer-loop/fixture-missing-prompt",
                }
            ),
        )
        self.write(
            "fixtures/outer-loop/reports/dry-run-pass.json",
            json.dumps(
                {
                    "ok": True,
                    "plan_id": "fixture-valid-next-three",
                    "steps": [
                        {
                            "prompt_id": "PROMPT_01",
                            "path": ".prompts/PROMPT_01.txt",
                            "status": "pass",
                            "validation_commands": ["python3 -m unittest tests/test_ahl.py"],
                            "problems": [],
                        }
                    ],
                    "problems": [],
                }
            ),
        )
        self.write(
            "fixtures/portable-operator/run-range/valid-plan.json",
            json.dumps(
                {
                    "ok": True,
                    "schema": "schemas/portable-operator-run-plan.schema.json",
                    "plan_id": "fixture-portable-run-range",
                    "mode": "dry-run",
                    "dry_run": True,
                    "project": {"root": "/tmp/example-project"},
                    "requested_range": {"start": "18", "end": "18"},
                    "prompt_ids": ["PROMPT_18"],
                    "steps": [],
                    "next_prompt": "PROMPT_18",
                    "safety_notes": [],
                    "problems": [],
                }
            ),
        )
        gate_report = {
            "ok": True,
            "status": "pass",
            "prompt_id": "PROMPT_36",
            "changed_files": [],
            "validation_commands": {"source": "plan", "commands": []},
            "validation_outcomes": [],
            "ahl_checks": [],
            "completion_audit": {"status": "present"},
            "next_prompt_readiness": {"status": "ready", "next_prompt": "PROMPT_37"},
            "handoff": {"status": "absent"},
            "commit_plan": {"status": "none"},
            "decision": "continue",
        }
        self.write("fixtures/outer-loop/gates/pass.json", json.dumps(gate_report))
        blocked_gate_report = dict(gate_report)
        blocked_gate_report.update(
            {
                "ok": False,
                "status": "blocked",
                "next_prompt_readiness": {"status": "blocked", "next_prompt": "PROMPT_37"},
                "decision": "stop",
            }
        )
        self.write("fixtures/outer-loop/gates/blocked.json", json.dumps(blocked_gate_report))
        self.write(
            "fixtures/outer-loop/runs/live-runner-example.json",
            json.dumps(
                {
                    "ok": True,
                    "status": "completed",
                    "run_id": "fixture-live-runner-example",
                    "plan_id": "fixture-valid-next-three",
                    "mode": "dry-run",
                    "driver": {"id": "manual"},
                    "steps": [],
                    "problems": [],
                }
            ),
        )
        ledger_fixture = {
            "ok": False,
            "status": "interrupted",
            "run_id": "fixture-resumable-ledger",
            "plan_id": "fixture-valid-next-three",
            "mode": "dry-run",
            "driver": {"id": "manual"},
            "steps": [{"prompt_id": "PROMPT_01", "status": "completed"}, {"prompt_id": "PROMPT_02", "status": "pending"}],
            "resume_pointer": {"next_prompt": "PROMPT_02"},
            "stop_reason": "user-interrupted",
            "recovery_recommendation": "Resume from PROMPT_02.",
            "problems": [],
        }
        self.write("fixtures/outer-loop/runs/resumable-ledger.json", json.dumps(ledger_fixture))
        interrupted_fixture = dict(ledger_fixture)
        interrupted_fixture.update({"run_id": "fixture-interrupted-ledger", "status": "interrupted", "stop_reason": "driver-timeout"})
        self.write("fixtures/outer-loop/runs/interrupted-ledger.json", json.dumps(interrupted_fixture))
        blocked_fixture = dict(ledger_fixture)
        blocked_fixture.update({"run_id": "fixture-blocked-ledger", "status": "blocked", "stop_reason": "next-prompt-readiness-blocked"})
        self.write("fixtures/outer-loop/runs/blocked-ledger.json", json.dumps(blocked_fixture))
        commit_plan = {
            "ok": True,
            "schema": "schemas/commit-plan.schema.json",
            "plan_id": "commit-plan-PROMPT_38",
            "mode": "plan-only",
            "prompt_ids": ["PROMPT_38"],
            "groups": [
                {
                    "group_id": "commit-1",
                    "prompt_ids": ["PROMPT_38"],
                    "subject": "[PROMPT_38] Package prompt changes",
                    "changed_files": [{"path": "docs/outer-loop/commit-planning.md", "status": "modified"}],
                    "validation_status": "passed",
                }
            ],
            "git": {"available": True, "unsafe": False, "status_lines": [], "modified": [], "untracked": [], "deleted": [], "staged": []},
            "problems": [],
        }
        self.write("fixtures/outer-loop/commits/plan-one-prompt.json", json.dumps(commit_plan))
        batch_plan = dict(commit_plan)
        batch_plan.update(
            {
                "plan_id": "commit-plan-PROMPT_38-PROMPT_39",
                "prompt_ids": ["PROMPT_38", "PROMPT_39"],
                "groups": [
                    {
                        "group_id": "commit-1",
                        "prompt_ids": ["PROMPT_38", "PROMPT_39"],
                        "subject": "[PROMPT_38-PROMPT_39] Package prompt changes",
                        "changed_files": [{"path": "docs/outer-loop/commit-planning.md", "status": "modified"}],
                        "validation_status": "passed",
                    }
                ],
            }
        )
        self.write("fixtures/outer-loop/commits/plan-batch.json", json.dumps(batch_plan))

    def test_fixtures_check_accepts_expected_fixture_set(self):
        self.write_minimal_fixture_set()

        code, output = self.run_cli("fixtures", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(len(data["fixtures"]), len(ahl.FIXTURE_SPECS))

    def test_fixtures_check_detects_invalid_prompt_id(self):
        self.write_minimal_fixture_set()
        self.write(
            "fixtures/lane-records/single-lane.json",
            json.dumps(
                {
                    "lane_id": "fixture-lane",
                    "prompt_id": "PROMPT_9",
                    "owner_role": "worker",
                    "scope": "Test lane.",
                    "status": "completed",
                    "inputs": [],
                    "outputs": [],
                }
            ),
        )

        code, output = self.run_cli("fixtures", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("invalid prompt id references" in problem for problem in data["problems"]))

    def write_minimal_dry_run_set(self):
        self.write("AGENT.md", "# Agent\n")
        self.write("runbooks/fresh-session-prompt-run.md", "# Runbook\n")
        self.write("dry-runs/expected/sequential-prompt-run.md", "# Expected\n")
        self.write(
            "dry-runs/PARITY.md",
            "\n".join(
                [
                    "# Dry-Run Parity",
                    "",
                    "| Scenario id | Capability covered | Status | Evidence |",
                    "| --- | --- | --- | --- |",
                    "| sequential-prompt-run | Normal run | verified | dry-runs/scenarios/sequential-prompt-run.json |",
                ]
            )
            + "\n",
        )
        self.write(
            "dry-runs/scenarios/sequential-prompt-run.json",
            json.dumps(
                {
                    "id": "sequential-prompt-run",
                    "purpose": "Exercise a normal prompt run.",
                    "input_artifacts": [
                        "AGENT.md",
                        "runbooks/fresh-session-prompt-run.md",
                    ],
                    "routine_sequence": ["load context", "audit"],
                    "expected_checks": ["artifacts exist"],
                    "expected_outputs": ["dry-runs/expected/sequential-prompt-run.md"],
                    "failure_modes_covered": ["missing artifact"],
                }
            ),
        )

    def test_dry_run_list_reports_scenarios(self):
        self.write_minimal_dry_run_set()

        code, output = self.run_cli("dry-run", "list", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["scenario_count"], 1)
        self.assertEqual(data["scenarios"][0]["id"], "sequential-prompt-run")

    def test_dry_run_check_accepts_successful_scenario(self):
        self.write_minimal_dry_run_set()

        code, output = self.run_cli("dry-run", "check", "sequential-prompt-run", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["results"][0]["status"], "pass")

    def test_dry_run_check_detects_missing_artifact(self):
        self.write_minimal_dry_run_set()
        (self.root / "AGENT.md").unlink()

        code, output = self.run_cli("dry-run", "check", "sequential-prompt-run", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertEqual(data["results"][0]["status"], "fail")
        self.assertTrue(any("referenced path does not exist: AGENT.md" in problem for problem in data["problems"]))

    def test_dry_run_check_json_has_stable_fields(self):
        self.write_minimal_dry_run_set()

        code, output = self.run_cli("dry-run", "check", "--all", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("ok", "scenario_count", "checked", "results", "parity", "problems"):
            self.assertIn(key, data)
        for key in ("id", "status", "problems"):
            self.assertIn(key, data["results"][0])

    def test_dry_run_check_reports_parity_missing_backing_json(self):
        self.write_minimal_dry_run_set()
        (self.root / "dry-runs" / "scenarios" / "sequential-prompt-run.json").unlink()

        code, output = self.run_cli("dry-run", "check", "--all", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertIn("sequential-prompt-run", data["parity"]["missing_backing_json"])
        self.assertEqual(data["results"][0]["status"], "missing")

    def write_minimal_lane_demo(self):
        for filename in ahl.LANE_REQUIRED_FILES:
            if filename == "lane-status.json":
                continue
            self.write(f"simulations/lane-demo/{filename}", f"# {filename}\n")
        self.write(
            "simulations/lane-demo/lane-status.json",
            json.dumps(
                {
                    "lane_id": "lane-demo",
                    "simulation": "template-docs-refresh",
                    "state": "done",
                    "roles": {
                        "orchestrator": "set intent",
                        "lead": "planned docs validation",
                        "worker-01": "checked template index",
                        "reviewer": "reported no blocking findings",
                        "auditor": "closed simulation",
                    },
                    "artifacts": [
                        "simulations/lane-demo/orchestrator-brief.md",
                        "simulations/lane-demo/lead-plan.md",
                        "simulations/lane-demo/worker-01-result.md",
                        "simulations/lane-demo/reviewer-report.md",
                        "simulations/lane-demo/auditor-closeout.md",
                    ],
                    "current_step": "closed",
                    "stop_escalation": {"needed": False, "reason": "No blocker."},
                }
            ),
        )

    def test_lane_check_accepts_complete_demo(self):
        self.write_minimal_lane_demo()

        code, output = self.run_cli("lane", "check", "simulations/lane-demo", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["state"], "done")
        self.assertEqual(data["missing_artifacts"], [])

    def test_lane_status_reports_current_state(self):
        self.write_minimal_lane_demo()

        code, output = self.run_cli("lane", "status", "simulations/lane-demo", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["lane_dir"], "simulations/lane-demo")
        self.assertEqual(data["state"], "done")
        self.assertIn("roles", data["status"])

    def test_lane_check_reports_missing_artifacts_and_bad_status(self):
        self.write_minimal_lane_demo()
        (self.root / "simulations" / "lane-demo" / "worker-01-result.md").unlink()
        self.write("simulations/lane-demo/lane-status.json", json.dumps({"state": "moving"}))

        code, output = self.run_cli("lane", "check", "simulations/lane-demo", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertIn("simulations/lane-demo/worker-01-result.md", data["missing_artifacts"])
        self.assertTrue(any("missing required fields" in problem for problem in data["problems"]))
        self.assertTrue(any("state must be one of" in problem for problem in data["problems"]))

    def write_minimal_domain_pack(self):
        self.write("domain-packs/docs-pack/README.md", "# Docs Pack\n")
        self.write("domain-packs/docs-pack/routines.md", "# Routines\n")
        self.write(
            "domain-packs/docs-pack/pack.json",
            json.dumps(
                {
                    "schema_version": 1,
                    "id": "docs-pack",
                    "name": "Docs Pack",
                    "status": "draft",
                    "purpose": "Test pack.",
                    "entrypoint": "README.md",
                    "files": ["README.md", "routines.md"],
                    "optional": True,
                    "core_doctrine_changes": False,
                }
            ),
        )

    def test_domain_pack_check_accepts_valid_manifest(self):
        self.write_minimal_domain_pack()

        code, output = self.run_cli("domain-pack", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["packs"][0]["id"], "docs-pack")
        self.assertEqual(data["packs"][0]["status"], "pass")

    def test_domain_pack_check_detects_missing_reference_and_required_flags(self):
        self.write("domain-packs/bad/README.md", "# Bad\n")
        self.write(
            "domain-packs/bad/pack.json",
            json.dumps(
                {
                    "schema_version": 1,
                    "id": "bad",
                    "name": "Bad",
                    "status": "draft",
                    "purpose": "Bad pack.",
                    "entrypoint": "README.md",
                    "files": ["README.md", "missing.md"],
                    "optional": False,
                    "core_doctrine_changes": True,
                }
            ),
        )

        code, output = self.run_cli("domain-pack", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("optional must be true" in problem for problem in data["problems"]))
        self.assertTrue(any("core_doctrine_changes must be false" in problem for problem in data["problems"]))
        self.assertTrue(any("missing.md" in problem for problem in data["problems"]))

    def write_experiment_templates(self):
        self.write(
            "experiments/templates/experiment-plan.md",
            "\n".join(
                [
                    "# Experiment Plan",
                    "",
                    "- Experiment id:",
                    "- Date opened:",
                    "- Status: Planned / Active",
                    "",
                    "- Hypothesis or question:",
                    "- Workflow problem:",
                    "- Stop condition:",
                ]
            )
            + "\n",
        )
        self.write(
            "experiments/templates/experiment-log.md",
            "\n".join(
                [
                    "# Experiment Log",
                    "",
                    "- Experiment id:",
                    "- Log date:",
                    "- What happened:",
                    "- Validation result:",
                    "- Current read:",
                ]
            )
            + "\n",
        )
        self.write("experiments/templates/experiment-closeout.md", "# Experiment Closeout\n- Experiment id:\n")

    def write_finding_template(self):
        self.write(
            "findings/templates/finding-record.md",
            "\n".join(
                [
                    "# Finding Record",
                    "",
                    "- Finding id:",
                    "- Date:",
                    "- Status: Draft / Reviewed / Superseded / Rejected",
                ]
            )
            + "\n",
        )

    def test_experiment_new_scaffolds_template_files(self):
        self.write_experiment_templates()

        code, output = self.run_cli("experiment", "new", "closeout-check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["directory"], "experiments/active/closeout-check")
        self.assertFalse(data["catalog_updated"])
        self.assertTrue((self.root / "experiments/active/closeout-check/experiment-plan.md").exists())
        plan_text = (self.root / "experiments/active/closeout-check/experiment-plan.md").read_text(encoding="utf-8")
        self.assertIn("- Experiment id: closeout-check", plan_text)
        self.assertIn("- Status: Active", plan_text)

    def test_experiment_new_refuses_overwrite_unless_forced(self):
        self.write_experiment_templates()

        code, _ = self.run_cli("experiment", "new", "overwrite-check", "--json")
        self.assertEqual(code, 0)

        code2, output2 = self.run_cli("experiment", "new", "overwrite-check", "--json")
        self.assertEqual(code2, 1)
        self.assertFalse(json.loads(output2)["ok"])

        code3, output3 = self.run_cli("experiment", "new", "overwrite-check", "--force", "--json")
        self.assertEqual(code3, 0)
        self.assertTrue(json.loads(output3)["ok"])

    def test_finding_new_scaffolds_record(self):
        self.write_finding_template()

        code, output = self.run_cli("finding", "new", "repeated-closeout-gap", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["directory"], "findings/draft/repeated-closeout-gap")
        record = self.root / "findings/draft/repeated-closeout-gap/finding-record.md"
        self.assertTrue(record.exists())
        self.assertIn("- Finding id: repeated-closeout-gap", record.read_text(encoding="utf-8"))

    def write_memory_templates(self):
        self.write(
            "templates/memory/promotion-candidate.md",
            "\n".join(
                [
                    "# Promotion Candidate",
                    "",
                    "- Candidate id:",
                    "- Date proposed:",
                    "- Proposed by:",
                    "- Status: Proposed / In Review / Accepted / Rejected / Superseded",
                    "",
                    "## Candidate",
                    "",
                    "- Candidate fact:",
                    "- Proposed target artifact:",
                    "- Proposed memory plane:",
                    "",
                    "## Evidence",
                    "",
                    "- Source evidence:",
                    "- Validation performed:",
                    "",
                    "## Review Notes",
                    "",
                    "- Review needed:",
                    "",
                    "## Disposition",
                    "",
                    "- Decision:",
                ]
            )
            + "\n",
        )
        self.write(
            "templates/memory/promotion-decision.md",
            "\n".join(
                [
                    "# Promotion Decision",
                    "",
                    "- Decision id:",
                    "- Candidate id:",
                    "- Candidate source:",
                    "- Decision date:",
                    "- Decision: Accepted / Rejected",
                    "- Status: Draft / Reviewed",
                ]
            )
            + "\n",
        )

    def test_memory_propose_scaffolds_candidate(self):
        self.write_memory_templates()

        code, output = self.run_cli("memory", "propose", "stable-cli-boundary", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["created"], "memory/promotion-queue/stable-cli-boundary.md")
        candidate = self.root / data["created"]
        self.assertTrue(candidate.exists())
        text = candidate.read_text(encoding="utf-8")
        self.assertIn("- Candidate id: stable-cli-boundary", text)
        self.assertIn("- Status: Proposed", text)

    def test_memory_propose_refuses_overwrite_unless_forced(self):
        self.write_memory_templates()

        code, _ = self.run_cli("memory", "propose", "overwrite-memory", "--json")
        self.assertEqual(code, 0)

        code2, output2 = self.run_cli("memory", "propose", "overwrite-memory", "--json")
        self.assertEqual(code2, 1)
        self.assertFalse(json.loads(output2)["ok"])

        code3, output3 = self.run_cli("memory", "propose", "overwrite-memory", "--force", "--json")
        self.assertEqual(code3, 0)
        self.assertTrue(json.loads(output3)["ok"])

    def test_memory_check_validates_queue_candidate_fields(self):
        self.write(
            "memory/promotion-queue/good.md",
            "\n".join(
                [
                    "# Promotion Candidate",
                    "",
                    "- Candidate id: good",
                    "- Date proposed: 2026-04-29",
                    "- Proposed by: test",
                    "- Status: Proposed",
                    "",
                    "## Candidate",
                    "",
                    "- Candidate fact: A validated repo fact.",
                    "- Proposed target artifact: docs/memory/README.md",
                    "- Proposed memory plane: durable repo memory",
                    "",
                    "## Evidence",
                    "",
                    "- Source evidence: tests",
                    "",
                    "## Review Notes",
                    "",
                    "- Review needed: operator approval",
                    "",
                    "## Disposition",
                    "",
                    "- Decision: Pending",
                ]
            )
            + "\n",
        )
        self.write("memory/promotion-queue/bad.md", "# Promotion Candidate\n- Candidate id:\n")

        code, output = self.run_cli("memory", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertEqual(len(data["candidates"]), 2)
        self.assertTrue(any("bad.md" in problem and "missing" in problem for problem in data["problems"]))

    def test_memory_decision_scaffolds_decision_record(self):
        self.write_memory_templates()
        code, _ = self.run_cli("memory", "propose", "decision-memory", "--json")
        self.assertEqual(code, 0)

        code2, output2 = self.run_cli("memory", "decision", "decision-memory", "--accepted", "--json")
        data = json.loads(output2)

        self.assertEqual(code2, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["decision"], "accepted")
        self.assertEqual(data["created"], "memory/accepted/decision-memory-decision.md")
        decision = self.root / data["created"]
        self.assertTrue(decision.exists())
        text = decision.read_text(encoding="utf-8")
        self.assertIn("- Candidate source: memory/promotion-queue/decision-memory.md", text)
        self.assertIn("- Decision: Accepted", text)

    def test_experiment_check_json_has_stable_fields(self):
        self.write("experiments/active/filled/experiment-plan.md", "# Plan\n- Experiment id: filled\n- Date opened: 2026-04-29\n- Status: Active\n- Hypothesis or question: Test question.\n- Workflow problem: Missed closeout.\n- Stop condition: One run.\n")
        self.write("experiments/active/filled/experiment-log.md", "# Log\n- Experiment id: filled\n- Log date: 2026-04-29\n- What happened: Recorded.\n- Validation result: Pass.\n- Current read: Supports\n")

        code, output = self.run_cli("experiment", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("ok", "directory", "checks", "problems", "experiments"):
            self.assertIn(key, data)
        for key in ("id", "path", "status", "problems"):
            self.assertIn(key, data["experiments"][0])
        self.assertEqual(data["experiments"][0]["status"], "pass")

    def test_experiment_check_detects_missing_required_fields_or_files(self):
        self.write("experiments/active/broken/experiment-plan.md", "# Plan\n- Experiment id:\n")

        code, output = self.run_cli("experiment", "check", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("missing required file: experiment-log.md" in problem for problem in data["problems"]))
        self.assertTrue(any("missing value for - Experiment id:" in problem for problem in data["problems"]))

    def test_doctor_fails_structurally_for_minimal_fixture(self):
        fixture = ROOT / "tests" / "fixtures" / "minimal_repo"
        shutil.copytree(fixture, self.root, dirs_exist_ok=True)

        code, output = self.run_cli("doctor", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertIn("checks", data)
        self.assertTrue(any("README.md" in problem for problem in data["problems"]))

    def test_doctor_accepts_safety_hygiene_fixture(self):
        self.add_foundations()

        code, output = self.run_cli("doctor", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertTrue(any(check["name"] == "tmp/HANDOFF.md absent unless actively needed" for check in data["checks"]))

    def test_doctor_detects_stale_handoff_and_transcript_dump(self):
        self.add_foundations()
        self.write("tmp/HANDOFF.md", "# Handoff\n")
        self.write("transcripts/session.md", "# Raw chat\n")
        self.write("chat-export.json", "{}\n")

        code, output = self.run_cli("doctor", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("tmp/HANDOFF.md is present" in problem for problem in data["problems"]))
        self.assertTrue(any("transcripts/" in problem for problem in data["problems"]))
        self.assertTrue(any("chat-export.json" in problem for problem in data["problems"]))

    def test_doctor_detects_missing_safety_ignore_entries(self):
        self.add_foundations()
        self.write(".gitignore", "tmp/\nagent-context-base/\npi-mono/\nclaw-code/\n")

        code, output = self.run_cli("doctor", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("missing .gitignore entry for .env" in problem for problem in data["problems"]))
        self.assertTrue(any("missing .gitignore entry for transcripts/" in problem for problem in data["problems"]))

    def test_doctor_detects_unignored_secret_looking_file_by_name_only(self):
        self.add_foundations()
        self.write(".gitignore", "tmp/\n.runtime/\n.session/\nagent-context-base/\npi-mono/\nclaw-code/\ntranscripts/\nconversation-dumps/\nchat-transcripts/\nassistant-transcripts/\nchatgpt-export/\nclaude-export/\n")
        self.write(".env", "not inspected\n")

        code, output = self.run_cli("doctor", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("secret-looking file is not ignored" in problem for problem in data["problems"]))

    def test_scaffold_run_creates_artifact_without_overwriting(self):
        self.write("templates/runs/run-manifest.md", "# Run Manifest\n- Prompt id:\n- Run id:\n")

        with mock.patch.object(ahl.dt, "datetime") as fake_datetime:
            fake_datetime.now.return_value = RealDateTime(2026, 4, 28, 12, 0, 0)
            code, output = self.run_cli("scaffold-run", "PROMPT_09", "--json")
            data = json.loads(output)

        self.assertEqual(code, 0)
        created = self.root / data["created"]
        self.assertTrue(created.exists())

        collision = self.root / "runs" / "PROMPT_09-20260428-120000" / "run-manifest.md"
        collision.parent.mkdir(parents=True, exist_ok=True)
        collision.write_text("existing\n", encoding="utf-8")
        with mock.patch.object(ahl.dt, "datetime") as fake_datetime:
            fake_datetime.now.return_value = RealDateTime(2026, 4, 28, 12, 0, 0)
            code3, output3 = self.run_cli("scaffold-run", "PROMPT_09", "--json")
        self.assertEqual(code3, 1)
        self.assertFalse(json.loads(output3)["ok"])

    def test_new_handoff_refuses_overwrite_unless_forced(self):
        self.write("templates/handoffs/handoff.md", "# Handoff\n")

        code, _ = self.run_cli("new-handoff", "--json")
        self.assertEqual(code, 0)

        code2, output2 = self.run_cli("new-handoff", "--json")
        self.assertEqual(code2, 1)
        self.assertFalse(json.loads(output2)["ok"])

        code3, output3 = self.run_cli("new-handoff", "--force", "--json")
        self.assertEqual(code3, 0)
        self.assertTrue(json.loads(output3)["ok"])

    def test_resume_returns_structured_json_fields(self):
        self.write("context/TASK.md", "# Task\n")

        code, output = self.run_cli("resume", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("branch", "head", "clean", "runtime_files", "posture", "recommendation"):
            self.assertIn(key, data)

    def test_checkpoint_scaffolds_missing_context_file_in_json(self):
        self.write("context/TASK.example.md", "# Task\n")
        self.write("context/SESSION.example.md", "# Session\n")
        self.write("context/MEMORY.example.md", "# Memory\n")

        code, output = self.run_cli("checkpoint", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertIn("context/TASK.md", data["scaffolded"])
        self.assertTrue((self.root / "context" / "TASK.md").exists())

    def test_metadata_example_returns_run_record_skeleton(self):
        code, output = self.run_cli("metadata-example", "13", "--assistant", "codex", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["prompt_id"], "PROMPT_13")
        self.assertEqual(data["assistant_tool"], "codex")
        self.assertEqual(data["permission_posture"], "workspace-write")
        self.assertEqual(data["completion_audit_status"], "not_started")
        self.assertIn("changed_files", data)

    def write_commit_prompt(self):
        self.write(
            ".prompts/PROMPT_38.txt",
            "\n".join(
                [
                    "# PROMPT_38 - Commit Planner",
                    "",
                    "## Required Deliverables",
                    "",
                    "- `docs/outer-loop/commit-planning.md`",
                    "- `templates/outer-loop/commit-plan.md`",
                    "",
                    "## Validation",
                    "",
                    "Run `python3 -m unittest tests/test_ahl.py`.",
                    "",
                ]
            )
            + "\n",
        )

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_plan_generation_with_modified_and_untracked_files(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.write_commit_prompt()
        self.write("docs/outer-loop/commit-planning.md", "# Commit Planning\n")
        self.write("templates/outer-loop/commit-plan.md", "# Commit Plan\n")
        self.write("human-notes.md", "# Local notes\n")

        code, output = self.run_cli("commit", "plan", "PROMPT_38", "--out", "runs/plan.json", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["groups"][0]["subject"], "[PROMPT_38] Package prompt changes")
        planned = {item["path"] for item in data["groups"][0]["changed_files"]}
        self.assertIn("docs/outer-loop/commit-planning.md", planned)
        self.assertIn("templates/outer-loop/commit-plan.md", planned)
        self.assertTrue(any(item["path"] == "human-notes.md" for item in data["unrelated_changes"]))
        self.assertTrue((self.root / "runs/plan.json").exists())

    def test_commit_execute_requires_explicit_approval(self):
        plan = {
            "ok": True,
            "schema": "schemas/commit-plan.schema.json",
            "plan_id": "commit-plan-PROMPT_38",
            "mode": "plan-only",
            "prompt_ids": ["PROMPT_38"],
            "groups": [
                {
                    "group_id": "commit-1",
                    "prompt_ids": ["PROMPT_38"],
                    "subject": "[PROMPT_38] Package prompt changes",
                    "changed_files": [{"path": "docs/file.md", "status": "modified"}],
                    "validation_status": "passed",
                }
            ],
            "git": {"available": True, "unsafe": False, "status_lines": [], "modified": [], "untracked": [], "deleted": [], "staged": []},
            "problems": [],
        }
        self.write("plans/commit-plan.json", json.dumps(plan))
        self.write("docs/file.md", "# File\n")

        with mock.patch.object(ahl, "run_git", return_value=(self.git_status_ok(""), None)):
            code, output = self.run_cli("commit", "execute", "--plan", "plans/commit-plan.json", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("--operator-approved" in problem for problem in data["problems"]))

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_executor_stages_only_listed_files_and_reports_hash(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.root, check=True)
        self.write("README.md", "# Repo\n")
        subprocess.run(["git", "add", "README.md"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.write("docs/file.md", "# File\n")
        self.write("notes.md", "# Notes\n")
        plan = {
            "ok": True,
            "schema": "schemas/commit-plan.schema.json",
            "plan_id": "commit-plan-PROMPT_38",
            "mode": "plan-only",
            "prompt_ids": ["PROMPT_38"],
            "groups": [
                {
                    "group_id": "commit-1",
                    "prompt_ids": ["PROMPT_38"],
                    "subject": "[PROMPT_38] Add commit doc",
                    "summary": "Add commit doc.",
                    "changed_files": [{"path": "docs/file.md", "status": "untracked"}],
                    "validation_status": "passed",
                    "validation_evidence": [{"command": "python3 -m unittest tests/test_ahl.py", "status": "passed"}],
                    "follow_up_notes": [],
                }
            ],
            "git": {"available": True, "unsafe": False, "status_lines": [], "modified": [], "untracked": [], "deleted": [], "staged": []},
            "problems": [],
        }
        self.write("plans/commit-plan.json", json.dumps(plan))

        code, output = self.run_cli("commit", "execute", "--plan", "plans/commit-plan.json", "--operator-approved", "--json")
        data = json.loads(output)
        status = subprocess.run(["git", "status", "--short"], cwd=self.root, check=True, text=True, stdout=subprocess.PIPE)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertEqual(data["status"], "committed")
        self.assertIsNotNone(data["commits"][0]["hash"])
        self.assertIn("?? notes.md", status.stdout)

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_executor_refuses_unrelated_staged_files(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.write("docs/file.md", "# File\n")
        self.write("notes.md", "# Notes\n")
        subprocess.run(["git", "add", "notes.md"], cwd=self.root, check=True)
        plan = {
            "ok": True,
            "schema": "schemas/commit-plan.schema.json",
            "plan_id": "commit-plan-PROMPT_38",
            "mode": "plan-only",
            "prompt_ids": ["PROMPT_38"],
            "groups": [
                {
                    "group_id": "commit-1",
                    "prompt_ids": ["PROMPT_38"],
                    "subject": "[PROMPT_38] Add commit doc",
                    "changed_files": [{"path": "docs/file.md", "status": "untracked"}],
                    "validation_status": "passed",
                }
            ],
            "git": {"available": True, "unsafe": False, "status_lines": [], "modified": [], "untracked": [], "deleted": [], "staged": []},
            "problems": [],
        }
        self.write("plans/commit-plan.json", json.dumps(plan))

        code, output = self.run_cli("commit", "execute", "--plan", "plans/commit-plan.json", "--operator-approved", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertTrue(any("unrelated staged files" in problem for problem in data["problems"]))

    def test_commit_plan_json_has_stable_fields(self):
        self.write_commit_prompt()
        with mock.patch.object(ahl, "run_git", return_value=(self.git_status_ok("?? docs/outer-loop/commit-planning.md\n"), None)):
            code, output = self.run_cli("commit", "plan", "PROMPT_38", "--out", "runs/plan.json", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("ok", "schema", "plan_id", "created_at", "mode", "source", "prompt_ids", "prompt_context", "grouping_policy", "git", "groups", "unrelated_changes", "warnings", "problems", "artifact"):
            self.assertIn(key, data)

    def init_git_repo(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.root, check=True)

    def make_git_commit(self, path, content, subject, body=None):
        self.write(path, content)
        subprocess.run(["git", "add", path], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        command = ["git", "commit", "-m", subject]
        if body is not None:
            command.extend(["-m", body])
        subprocess.run(command, cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_check_accepts_prompt_prefixed_commit_with_body(self):
        self.init_git_repo()
        self.make_git_commit("docs/one.md", "# One\n", "[PROMPT_84] Add commit check docs", "Record validation evidence.\n\nValidation:\n- python3 -m unittest tests/test_ahl.py")

        code, output = self.run_cli("commit", "check", "--prompt", "PROMPT_84", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertTrue(data["ok"])
        self.assertTrue(data["read_only"])
        self.assertEqual(data["selector"]["matched_commit_count"], 1)
        self.assertEqual(data["commits"][0]["issues"], [])

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_check_detects_missing_prompt_prefix(self):
        self.init_git_repo()
        self.make_git_commit("docs/one.md", "# One\n", "Add commit check docs")

        code, output = self.run_cli("commit", "check", "--last", "1", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertEqual(data["commits"][0]["issues"][0]["code"], "missing_prompt_prefix")
        self.assertTrue(any("amend" in item for item in data["guidance"]))

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_check_detects_literal_newline_sequence(self):
        self.init_git_repo()
        self.make_git_commit("docs/one.md", "# One\n", "[PROMPT_84] Bad literal \\n sequence")

        code, output = self.run_cli("commit", "check", "--last", "1", "--json")
        data = json.loads(output)
        codes = {issue["code"] for issue in data["commits"][0]["issues"]}

        self.assertEqual(code, 1)
        self.assertIn("literal_newline_sequence", codes)

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_check_detects_co_author_trailer(self):
        self.init_git_repo()
        self.make_git_commit("docs/one.md", "# One\n", "[PROMPT_84] Add docs", "Body.\n\nCo-authored-by: Bot <bot@example.test>")

        code, output = self.run_cli("commit", "check", "--prompt", "84", "--json")
        data = json.loads(output)
        codes = {issue["code"] for issue in data["commits"][0]["issues"]}

        self.assertEqual(code, 1)
        self.assertIn("co_author_trailer", codes)

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_check_detects_overlong_subject_and_unwrapped_body(self):
        self.init_git_repo()
        long_subject = "[PROMPT_84] " + "Add a subject that is too long for normal review hygiene and needs cleanup"
        long_body = "This body line is intentionally much too long for the wrapping guidance used by the helper and should be reported."
        self.make_git_commit("docs/one.md", "# One\n", long_subject, long_body)

        code, output = self.run_cli("commit", "check", "--last", "1", "--json")
        data = json.loads(output)
        codes = {issue["code"] for issue in data["commits"][0]["issues"]}

        self.assertEqual(code, 1)
        self.assertIn("overlong_subject", codes)
        self.assertIn("unwrapped_body_line", codes)

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_check_supports_range_and_last_selection(self):
        self.init_git_repo()
        self.make_git_commit("one.txt", "one\n", "[PROMPT_83] First")
        self.make_git_commit("two.txt", "two\n", "[PROMPT_84] Second")

        last_code, last_output = self.run_cli("commit", "check", "--last", "1", "--json")
        last_data = json.loads(last_output)
        range_code, range_output = self.run_cli("commit", "check", "--range", "HEAD~1..HEAD", "--json")
        range_data = json.loads(range_output)

        self.assertEqual(last_code, 0)
        self.assertEqual(last_data["selector"]["searched_commit_count"], 1)
        self.assertEqual(last_data["commits"][0]["subject"], "[PROMPT_84] Second")
        self.assertEqual(range_code, 0)
        self.assertEqual(range_data["selector"]["mode"], "range")
        self.assertEqual(range_data["selector"]["matched_commit_count"], 1)

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_check_prompt_selection_finds_more_than_three_commits(self):
        self.init_git_repo()
        for index in range(4):
            self.make_git_commit(f"docs/{index}.md", f"# {index}\n", f"[PROMPT_84] Part {index}")

        code, output = self.run_cli("commit", "check", "--prompt", "PROMPT_84", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["selector"]["matched_commit_count"], 4)
        self.assertEqual(data["summary"]["prompt_counts"]["PROMPT_84"], 4)

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_check_does_not_run_commit_rewrite_or_staging_commands(self):
        self.init_git_repo()
        self.make_git_commit("docs/one.md", "# One\n", "Missing prefix")
        observed = []
        real_run_git = ahl.run_git

        def recording_run_git(root, args):
            observed.append(tuple(args))
            return real_run_git(root, args)

        with mock.patch.object(ahl, "run_git", side_effect=recording_run_git):
            code, output = self.run_cli("commit", "check", "--last", "1", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        forbidden = {"commit", "rebase", "reset", "add"}
        self.assertFalse(any(args and args[0] in forbidden for args in observed))

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_commit_check_json_has_stable_fields(self):
        self.init_git_repo()
        self.make_git_commit("docs/one.md", "# One\n", "[PROMPT_84] Add docs")

        code, output = self.run_cli("commit", "check", "--prompt", "PROMPT_84", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        for key in ("ok", "read_only", "project", "selector", "summary", "commits", "guidance", "warnings", "problems"):
            self.assertIn(key, data)
        for key in ("mode", "description", "prompt", "searched_commit_count", "matched_commit_count", "truncated"):
            self.assertIn(key, data["selector"])
        for key in ("hash", "short_hash", "subject", "parents", "changed_files", "issues"):
            self.assertIn(key, data["commits"][0])

    def test_trace_returns_degraded_result_outside_git_repo(self):
        self.write(".prompts/PROMPT_20.txt", "# Prompt\n")

        code, output = self.run_cli("trace", "PROMPT_20", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["prompt_id"], "PROMPT_20")
        self.assertTrue(data["prompt_file_exists"])
        self.assertTrue(data["git"]["degraded"])
        self.assertFalse(data["git"]["inside_work_tree"])
        self.assertIn("changed_files", data)
        self.assertIn("run_record_skeleton", data)
        self.assertIn("assistant_tool", data["suggested_run_record_missing_fields"])

    @unittest.skipUnless(shutil.which("git"), "git is not available")
    def test_trace_summarizes_temporary_git_repo_changes(self):
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.write(".prompts/PROMPT_20.txt", "# Prompt\n")
        self.write("docs/traceability.md", "# Traceability\n")
        self.write("tests/test_trace.py", "# Tests\n")
        self.write("templates/reports/traceability-summary.md", "# Template\n")

        code, output = self.run_cli("trace", "20", "--json")
        data = json.loads(output)

        self.assertEqual(code, 0)
        self.assertEqual(data["prompt_id"], "PROMPT_20")
        self.assertTrue(data["git"]["inside_work_tree"])
        self.assertTrue(data["docs_changed"])
        self.assertTrue(data["tests_changed"])
        self.assertTrue(data["templates_changed"])
        self.assertIn("?? docs/traceability.md", data["changed_files"])

    def test_trace_reports_missing_prompt_argument_clearly(self):
        out = io.StringIO()
        err = io.StringIO()
        with mock.patch("pathlib.Path.cwd", return_value=self.root):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                with self.assertRaises(SystemExit) as raised:
                    ahl.main(["trace"])

        self.assertEqual(raised.exception.code, 2)
        self.assertIn("prompt", err.getvalue())


if __name__ == "__main__":
    unittest.main()
