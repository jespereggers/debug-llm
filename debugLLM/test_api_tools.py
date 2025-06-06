import unittest
from unittest.mock import patch
from pathlib import Path

import api_tools


class TestTools(unittest.TestCase):

    def test_call_func_nonexistent_function(self):
        with self.assertRaises(AttributeError):
            api_tools.call_func('nonexistent_function')

    def test_check_syntax_valid_code(self):
        code = 'print("Hello World")'
        result = api_tools.check_syntax(code)
        self.assertEqual(result, 'Proposed code has valid syntax.')

    def test_check_syntax_invalid_code(self):
        code = 'print("Hello World"'
        result = api_tools.check_syntax(code)
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'Proposed code has invalid syntax.')

    @patch('sys_tools.get_all_files')
    @patch('sys_tools.load_script')
    @patch('sys_tools.get_script_overview')
    def test_get_project_index(self, mock_get_script_overview, mock_load_script, mock_get_all_files):
        mock_get_all_files.return_value = [
            Path('script1.py'),
            Path('.venv/script2.py'),
            Path('script3.py'),
        ]
        mock_load_script.return_value = 'def foo(): pass'
        mock_get_script_overview.return_value = {'foo': {'params': {}, 'return': 'None'}}

        result = api_tools.get_project_index()
        expected = {
            'script1.py': {'foo': {'params': {}, 'return': 'None'}},
            'script3.py': {'foo': {'params': {}, 'return': 'None'}},
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
