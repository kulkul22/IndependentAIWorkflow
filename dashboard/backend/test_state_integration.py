import json
import tempfile
import unittest
from pathlib import Path

from parser import get_current_phase


class PersistedStateIntegrationTests(unittest.TestCase):
    def test_state_json_wins_over_stale_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            run = Path(temp) / "runs" / "run_20260720_120000"
            run.mkdir(parents=True)
            (run / "walkthrough.md").write_text("old report", encoding="utf-8")
            (run / "state.json").write_text(json.dumps({
                "current_phase": 4,
                "role": "Senior Staff Engineer",
                "model": "Codex",
                "phase_status": "Executing Code",
            }), encoding="utf-8")

            result = get_current_phase(temp)

            self.assertEqual(result["phase"], 4)
            self.assertEqual(result["status"], "Executing Code")
            self.assertEqual(result["model"], "Codex")

    def test_fractional_visual_phase_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            run = Path(temp) / "runs" / "run_20260720_120001"
            run.mkdir(parents=True)
            (run / "state.json").write_text(json.dumps({
                "current_phase": 5.5,
                "role": "Independent Visual Auditor",
                "model": "Codex",
                "phase_status": "Visual QA",
            }), encoding="utf-8")

            result = get_current_phase(temp)

            self.assertEqual(result["phase"], 5.5)
            self.assertEqual(result["status"], "Visual QA")


if __name__ == "__main__":
    unittest.main()
