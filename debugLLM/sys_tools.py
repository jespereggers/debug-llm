import ast
from pathlib import Path
from typing import Any, Dict, List, Union


def save_script(content: str, file_path: Union[str, Path]) -> None:
    """
    Save the given content to a file at the specified path.

    :param content: The content to write to the file.
    :param file_path: The path where the file will be saved.
    """
    file_path = Path(file_path)
    with file_path.open('w', encoding='utf-8') as file:
        file.write(content)


def load_script(file_path: Union[str, Path]) -> str:
    """
    Load and return the content of a script from the specified file path.

    :param file_path: The path to the file to read.
    :return: The content of the file as a string.
    """
    file_path = Path(file_path)
    with file_path.open('r', encoding='utf-8', errors='replace') as file:
        return file.read()


def get_script_overview(script: str) -> Dict[str, Dict[str, Any]]:
    """
    Generate an overview of the functions defined in the given script.

    :param script: The Python script as a string.
    :return: A dictionary with function names as keys and their parameters and return types as values.
    """
    function_info: Dict[str, Dict[str, Any]] = {}
    try:
        tree = ast.parse(script)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python script provided: {e}")

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            params = {}
            for arg in node.args.args:
                param_name = arg.arg
                param_type = 'Any'
                if arg.annotation:
                    param_type = ast.unparse(arg.annotation)
                params[param_name] = param_type
            return_type = 'Any'
            if node.returns:
                return_type = ast.unparse(node.returns)
            function_info[func_name] = {'params': params, 'return': return_type}
    return function_info


def get_all_files(path: Union[str, Path]) -> List[Path]:
    """
    Perform a depth-first search to find all Python script files in the given directory path.

    :param path: The root directory path to search.
    :return: A list of paths to Python script files.
    """
    path = Path(path)
    python_files: List[Path] = []

    def dfs(current_path: Path) -> None:
        if current_path.is_file() and current_path.suffix == '.py':
            python_files.append(current_path)
        elif current_path.is_dir():
            for entry in current_path.iterdir():
                dfs(entry)

    dfs(path)
    return python_files
