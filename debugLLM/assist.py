from pathlib import Path
from typing import Any

from openai import Client
from pydantic import BaseModel

import environment


class SolvedPythonScript(BaseModel):
    """
    Model representing the solved Python script and an explanation of changes.
    """
    fixed_code: str
    explanation_of_changes: str


def create_assist(client: Client) -> Any:
    """
    Create an assistant with the specified instructions, model, tools, and response format.

    :param client: The OpenAI client instance.
    :return: The created assistant object.
    """
    return client.beta.assistants.create(
        instructions=environment.OPENAI_INSTRUCTIONS,
        model=environment.OPENAI_MODEL,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_script",
                    "description": "Get the current python file to work with."
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_syntax",
                    "description": "Find out if your new python code proposal has valid syntax.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "new_code_proposal": {
                                "type": "string",
                                "description": "Fixed python code proposal."
                            }
                        },
                        "required": ["new_code_proposal"],
                        "additionalProperties": False
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_project_index",
                    "description": "Find every function across all scripts."
                }
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "PythonScript",
                "schema": SolvedPythonScript.model_json_schema()
            }
        }
    )


def upload_file(client: Client, path: str) -> str:
    """
    Upload a file to the OpenAI client for use with the assistant.

    :param client: The OpenAI client instance.
    :param path: The path to the file to upload.
    :return: The ID of the uploaded file.
    :raises FileNotFoundError: If the file does not exist.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    with file_path.open("rb") as file:
        response = client.files.create(
            file=file,
            purpose="assistants"
        )
    return response.id


def create_thread(client: Client) -> Any:
    """
    Create a new thread and send an initial message to it.

    :param client: The OpenAI client instance.
    :return: The created thread object.
    """
    new_thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=new_thread.id,
        role="user",
        content=environment.OPENAI_MESSAGE
    )
    return new_thread


def create_run(client: Client, assistant: Any, thread: Any) -> Any:
    """
    Create and poll a new run in the thread using the assistant.

    :param client: The OpenAI client instance.
    :param assistant: The assistant to use for the run.
    :param thread: The thread to create the run in.
    :return: The result of the run.
    """
    return client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
