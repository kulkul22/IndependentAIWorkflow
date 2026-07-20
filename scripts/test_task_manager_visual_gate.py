import json
import tempfile
import unittest
from pathlib import Path

from task_manager import visual_gate_error


class VisualGateTests(unittest.TestCase):
    def test_ui_task_fails_closed_without_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            tasks_path = Path(temp) / "tasks.json"
            tasks_path.write_text("[]", encoding="utf-8")
            error = visual_gate_error(str(tasks_path), {"ui_acceptance_ids": ["UI-ACC-001"]})
            self.assertIn("ui_acceptance.json", error)

    def test_ui_task_passes_with_acceptance_and_approved_audit(self):
        with tempfile.TemporaryDirectory() as temp:
            run = Path(temp)
            tasks_path = run / "tasks.json"
            tasks_path.write_text("[]", encoding="utf-8")
            (run / "ui_acceptance.json").write_text(json.dumps([
                {"id": "UI-ACC-001", "status": "pass", "evidence": "visual_evidence/home.png"}
            ]), encoding="utf-8")
            (run / "visual_audit.md").write_text("# Audit\n\nSTATUS: APPROVED\n", encoding="utf-8")

            error = visual_gate_error(str(tasks_path), {"ui_acceptance_ids": ["UI-ACC-001"]})

            self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()
