import unittest
from unittest.mock import mock_open, patch

import sys_tools


class TestAssist(unittest.TestCase):
    suffix = "py"

    @patch('sys_tools.Path.open')
    def test_save_script(self, mock_open_function):
        content = 'print("Hello World")'
        file_path = 'test_script.py'

        sys_tools.save_script(content, file_path)

        # Ensure that Path.open was called with 'w' and encoding='utf-8'
        mock_open_function.assert_called_with('w', encoding='utf-8')

        # Get the mock file handle returned by Path.open().__enter__()
        mock_file_handle = mock_open_function.return_value.__enter__.return_value

        # Assert that write was called with the correct content
        mock_file_handle.write.assert_called_with(content)

    @patch('assist.Path.open', new_callable=mock_open, read_data='print("Hello World")')
    def test_load_script(self, mock_file):
        file_path = 'test_script.py'
        result = sys_tools.load_script(file_path)
        self.assertEqual(result, 'print("Hello World")')

    def test_get_script_overview(self):
        script = '''
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str):
    print(f"Hello, {name}")
'''
        expected = {
            'add': {
                'params': {'a': 'int', 'b': 'int'},
                'return': 'int'
            },
            'greet': {
                'params': {'name': 'str'},
                'return': 'Any'
            }
        }
        result = sys_tools.get_script_overview(script)
        self.assertEqual(result, expected)

    def test_get_script_overview_invalid_script(self):
        script = 'def invalid_syntax('
        with self.assertRaises(ValueError):
            sys_tools.get_script_overview(script)


if __name__ == '__main__':
    unittest.main()
