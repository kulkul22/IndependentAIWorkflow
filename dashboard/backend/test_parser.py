import json
import os
import tempfile
import unittest

from parser import _get_request_title, get_current_phase


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


class CurrentPhaseTests(unittest.TestCase):
    def test_project_dir_and_active_coding_task_override_stale_test_output(self):
        with tempfile.TemporaryDirectory() as project_path:
            run_path = os.path.join(project_path, 'runs', 'run_20260718_120000')
            os.makedirs(run_path)

            with open(os.path.join(run_path, 'test_results.txt'), 'w', encoding='utf-8') as file:
                file.write('Results from the previous test pass')
            stale_marker = os.path.join(run_path, 'phase_5.md')
            with open(stale_marker, 'w', encoding='utf-8') as file:
                file.write('Status: Test & Validate\n')
            with open(os.path.join(run_path, 'tasks.json'), 'w', encoding='utf-8') as file:
                json.dump([
                    {
                        'id': 'T1',
                        'title': 'Implement dashboard sync',
                        'status': 'in_progress',
                        'assignee': 'codex-coder',
                    }
                ], file)
            os.utime(stale_marker, (100, 100))
            os.utime(os.path.join(run_path, 'test_results.txt'), (100, 100))
            os.utime(os.path.join(run_path, 'tasks.json'), (200, 200))

            current = get_current_phase(project_path)

            self.assertEqual(current['phase'], 4)
            self.assertEqual(current['status'], 'Execute Code')
            self.assertEqual(current['tasks'][0]['status'], 'in_progress')

    def test_latest_phase_marker_wins_over_cumulative_artifacts(self):
        with tempfile.TemporaryDirectory() as project_path:
            run_path = os.path.join(project_path, 'runs', 'run_20260718_120000')
            os.makedirs(run_path)

            with open(os.path.join(run_path, 'test_results.txt'), 'w', encoding='utf-8') as file:
                file.write('Old test results')
            marker_path = os.path.join(run_path, 'phase_4.md')
            with open(marker_path, 'w', encoding='utf-8') as file:
                file.write(
                    'Role: Senior Staff Engineer\n'
                    'Model: Codex\n'
                    'Status: Fixing dashboard synchronization\n'
                )
            os.utime(os.path.join(run_path, 'test_results.txt'), (100, 100))
            os.utime(marker_path, (200, 200))

            current = get_current_phase(project_path)

            self.assertEqual(current['phase'], 4)
            self.assertEqual(current['role'], 'Senior Staff Engineer')
            self.assertEqual(current['model'], 'Codex')
            self.assertEqual(current['status'], 'Fixing dashboard synchronization')


if __name__ == '__main__':
    unittest.main()
