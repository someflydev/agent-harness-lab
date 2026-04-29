import contextlib
from datetime import datetime as RealDateTime
import importlib.util
import io
import json
import shutil
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
        self.write(".gitignore", "tmp/\nagent-context-base/\npi-mono/\nclaw-code/\n")
        (self.root / ".prompts").mkdir()
        (self.root / "docs").mkdir()
        for dirname in ("contracts", "doctrine", "memory", "quality", "roles", "routines", "runtime", "skills"):
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

    def test_promptset_detects_gap_or_malformed_filename(self):
        self.write(".prompts/PROMPT_01.txt")
        self.write(".prompts/PROMPT_03.txt")
        self.write(".prompts/PROMPT_4.txt")

        code, output = self.run_cli("promptset", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertIn(2, data["gaps"])
        self.assertIn("PROMPT_4.txt", data["malformed"])

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

    def test_doctor_fails_structurally_for_minimal_fixture(self):
        fixture = ROOT / "tests" / "fixtures" / "minimal_repo"
        shutil.copytree(fixture, self.root, dirs_exist_ok=True)

        code, output = self.run_cli("doctor", "--json")
        data = json.loads(output)

        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertIn("checks", data)
        self.assertTrue(any("README.md" in problem for problem in data["problems"]))

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


if __name__ == "__main__":
    unittest.main()
