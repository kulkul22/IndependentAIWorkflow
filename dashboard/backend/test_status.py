import unittest

from status import normalize_status


class StatusNormalizationTests(unittest.TestCase):
    def test_agent_aliases_map_to_dashboard_columns(self):
        self.assertEqual(normalize_status("processing"), "in_progress")
        self.assertEqual(normalize_status("QA"), "in_test")
        self.assertEqual(normalize_status("completed"), "done")

    def test_missing_or_blank_status_is_todo(self):
        self.assertEqual(normalize_status(None), "todo")
        self.assertEqual(normalize_status(""), "todo")


if __name__ == "__main__":
    unittest.main()
