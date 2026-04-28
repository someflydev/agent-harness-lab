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
        (self.root / "runbooks").mkdir()
        (self.root / "templates").mkdir()

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


if __name__ == "__main__":
    unittest.main()
