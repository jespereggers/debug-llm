import unittest
from unittest.mock import MagicMock, patch

import main


class TestMain(unittest.TestCase):

    @patch('main.api_tools')
    def test_execute_tool_call_no_arguments(self, mock_api_tools):
        # Setup mocks
        tool_call = MagicMock()
        tool_call.function.name = 'test_function'
        tool_call.function.arguments = '{}'
        tool_call.id = '12345'
        mock_api_tools.call_func.return_value = 'output'

        # Call function
        result = main.execute_tool_call(tool_call)

        # Assertions
        mock_api_tools.call_func.assert_called_with('test_function')
        self.assertEqual(result, {'tool_call_id': '12345', 'output': 'output'})

    @patch('main.api_tools')
    def test_execute_tool_call_with_arguments(self, mock_api_tools):
        # Setup mocks
        tool_call = MagicMock()
        tool_call.function.name = 'test_function'
        tool_call.function.arguments = '{"arg1": "value1"}'
        tool_call.id = '12345'
        mock_api_tools.call_func.return_value = 'output'

        # Call function
        result = main.execute_tool_call(tool_call)

        # Assertions
        mock_api_tools.call_func.assert_called_with('test_function', '{"arg1": "value1"}')
        self.assertEqual(result, {'tool_call_id': '12345', 'output': 'output'})

    @patch('main.assist')
    def test_process_solution(self, mock_assist):
        # Setup mocks
        messages = MagicMock()
        messages.data = [MagicMock()]
        messages.data[0].content = [MagicMock()]
        messages.data[0].content[0].text.value = '{"fixed_code": "code", "explanation_of_changes": "changes"}'

        mock_solution = MagicMock()
        mock_assist.SolvedPythonScript.model_validate_json.return_value = mock_solution

        # Call function
        result = main.process_solution(messages)

        # Assertions
        mock_assist.SolvedPythonScript.model_validate_json.assert_called_with(
            '{"fixed_code": "code", "explanation_of_changes": "changes"}'
        )
        self.assertEqual(result, mock_solution)

    @patch('main.execute_tool_call')
    def test_collect_tool_outputs(self, mock_execute_tool_call):
        # Setup mocks
        mock_run = MagicMock()
        mock_run.required_action.submit_tool_outputs.tool_calls = ['tool_call1', 'tool_call2']
        mock_execute_tool_call.side_effect = [
            {'tool_call_id': '1', 'output': 'output1'},
            {'tool_call_id': '2', 'output': 'output2'}
        ]

        # Call function
        result = main.collect_tool_outputs(mock_run)

        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {'tool_call_id': '1', 'output': 'output1'})
        self.assertEqual(result[1], {'tool_call_id': '2', 'output': 'output2'})


if __name__ == '__main__':
    unittest.main()
