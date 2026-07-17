import json
import os
import tempfile
import unittest

from parser import _get_request_title


class RequestTitleTests(unittest.TestCase):
    def test_uses_task_from_state(self):
        with tempfile.TemporaryDirectory() as run_path:
            with open(os.path.join(run_path, 'state.json'), 'w', encoding='utf-8') as file:
                json.dump({'task': 'Build a request dashboard'}, file)

            self.assertEqual(_get_request_title(run_path), 'Build a request dashboard')

    def test_extracts_task_from_research_notes(self):
        with tempfile.TemporaryDirectory() as run_path:
            with open(os.path.join(run_path, 'research_notes.md'), 'w', encoding='utf-8') as file:
                file.write('# Research\n\n**Task:** Scrape today\'s gold price.\n')

            self.assertEqual(_get_request_title(run_path), "Scrape today's gold price.")

    def test_falls_back_to_clean_plan_heading(self):
        with tempfile.TemporaryDirectory() as run_path:
            with open(os.path.join(run_path, 'master_plan.md'), 'w', encoding='utf-8') as file:
                file.write('# [Phase 2] Master Plan: Gold Price Scraper\n')

            self.assertEqual(_get_request_title(run_path), 'Gold Price Scraper')


if __name__ == '__main__':
    unittest.main()