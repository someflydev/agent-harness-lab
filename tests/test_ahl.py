import contextlib
from datetime import datetime as RealDateTime
import importlib.util
import io
import json
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

    def write_docs_index(self):
        for dirname in (
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
        ):
            self.write(f"{dirname}/README.md", f"# {dirname}\n")
        self.write(
            "docs/README.md",
            "\n".join(
                [
                    "# Docs",
                    "",
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
