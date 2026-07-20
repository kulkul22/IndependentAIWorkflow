import unittest
from unittest.mock import patch

from call_advisor import call_claude_cli


class AdvisorFailureTests(unittest.TestCase):
    @patch("call_advisor.subprocess.run")
    def test_timeout_is_not_approval(self, run):
        import subprocess
        run.side_effect = subprocess.TimeoutExpired(cmd="claude", timeout=30)
        self.assertEqual(
            call_claude_cli("review", timeout=180),
            "ERROR_ADVISOR_TIMEOUT_AFTER_180S",
        )

    @patch("call_advisor.subprocess.run")
    def test_nonzero_exit_is_not_approval(self, run):
        run.return_value = type("Result", (), {
            "returncode": 2,
            "stdout": "",
            "stderr": "login required",
        })()
        result = call_claude_cli("review")
        self.assertTrue(result.startswith("ERROR_ADVISOR_EXIT_2:"))


if __name__ == "__main__":
    unittest.main()
