import ast
from pathlib import Path
from typing import Any, Callable, Dict

import environment
import sys_tools


def call_func(function_name: str, *args: Any) -> Any:
    """
    Call a registered function by its name with given arguments.

    :param function_name: The name of the function to call.
    :param args: Arguments to pass to the function.
    :return: The result of the function call.
    :raises AttributeError: If the function is not found.
    """
    func = FUNCTIONS.get(function_name)
    if callable(func):
        return func(*args)
    else:
        raise AttributeError(f"Function '{function_name}' not found.")


def get_script() -> str:
    """
    Load and return the script from the input path.

    :return: The content of the script as a string.
    """
    return sys_tools.load_script(environment.INPUT_PATH)


def check_syntax(code: str) -> str:
    """
    Check if the provided code has valid Python syntax.

    :param code: The code to check.
    :return: None if the code has valid syntax, otherwise the error message.
    """
    try:
        ast.parse(code)
        return 'Proposed code has valid syntax.'
    except SyntaxError:
        return 'Proposed code has invalid syntax.'


def get_project_index() -> Dict[str, Any]:
    """
    Create a unified index of all scripts in the project.

    :return: A dictionary mapping file paths to their script overview.
    """
    project_index: Dict[str, Any] = {}
    project_path = Path(environment.PROJECT_PATH)
    file_paths = sys_tools.get_all_files(project_path)

    for file_path in file_paths:
        # Exclude virtual environment directories
        if '.venv' in file_path.parts:
            continue

        script_content = sys_tools.load_script(str(file_path))
        index = sys_tools.get_script_overview(script_content)

        if index:
            project_index[str(file_path)] = index

    return project_index


# Define a mapping of function names to actual functions for safer access
FUNCTIONS: Dict[str, Callable] = {
    'get_script': get_script,
    'check_syntax': check_syntax,
    'get_project_index': get_project_index,
}
