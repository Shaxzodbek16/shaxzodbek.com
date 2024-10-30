import subprocess
import tempfile
import os
import json
from django.conf import settings
import timeout_decorator
import resource
import signal


class CodeExecutionError(Exception):
    pass


def set_resource_limits():
    # Set maximum CPU time to 2 seconds
    resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
    # Set maximum memory usage to 512 MB
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))


def create_test_case_file(test_cases):
    test_case_content = """
import unittest
import json
from solution import solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.results = []

    def tearDown(self):
        with open('results.json', 'w') as f:
            json.dump(self.results, f)

"""
    for i, test in enumerate(test_cases):
        test_case_content += f"""
    def test_{i + 1}(self):
        try:
            result = solution({test['input']})
            expected = {test['output']}
            self.assertEqual(result, expected)
            self.results.append({{'passed': True, 'input': {test['input']}, 'expected': {test['output']}, 'result': result}})
        except AssertionError as e:
            self.results.append({{'passed': False, 'input': {test['input']}, 'expected': {test['output']}, 'result': result}})
        except Exception as e:
            self.results.append({{'passed': False, 'input': {test['input']}, 'expected': {test['output']}, 'error': str(e)}})
"""

    return test_case_content


@timeout_decorator.timeout(5, use_signals=False)
def execute_code(code, test_cases):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create solution.py with user's code
        solution_path = os.path.join(temp_dir, 'solution.py')
        with open(solution_path, 'w') as f:
            f.write(code)

        # Create test file
        test_path = os.path.join(temp_dir, 'test_solution.py')
        with open(test_path, 'w') as f:
            f.write(create_test_case_file(test_cases))

        # Run tests in a separate process
        try:
            process = subprocess.run(
                ['python', '-m', 'unittest', 'test_solution.py'],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                preexec_fn=set_resource_limits,
                timeout=5
            )

            # Read results
            results_path = os.path.join(temp_dir, 'results.json')
            if os.path.exists(results_path):
                with open(results_path) as f:
                    results = json.load(f)
            else:
                results = []

            return {
                'success': process.returncode == 0,
                'output': process.stdout,
                'error': process.stderr,
                'results': results
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Code execution timed out',
                'results': []
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'results': []
            }
