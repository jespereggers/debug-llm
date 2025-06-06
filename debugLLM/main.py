from typing import Any, Dict, List, Optional

from openai import OpenAI
import api_tools
import sys_tools
import environment
import assist
import fixCodeEvaluator

def run_llm(client: OpenAI, thread: Any, run: Any) -> None:
    """
    Runs the LLM interaction loop until completion.

    :param client: OpenAI client instance.
    :param thread: The thread object for the interaction.
    :param run: The current run object.
    """
    while True:
        if run.status == 'completed':
            # Get completed content
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            print(messages)
            break
        else:
            print(f"Run status: {run.status}")

        # Collect tool outputs
        tool_outputs = collect_tool_outputs(run)

        # Submit all tool outputs at once after collecting them in a list
        if tool_outputs:
            try:
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
            except Exception as e:
                print(f"Failed to submit tool outputs: {e}")
                break  # Exit loop on failure
        else:
            print("No tool outputs to submit.")

        # Check the run status again
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            # Get response text as SolvedPythonScript object
            solution = process_solution(messages)
            # Save the final solution
            sys_tools.save_script(solution.fixed_code, environment.OUTPUT_PATH)
            print('\n' + solution.explanation_of_changes)
            break
        elif run.status == 'requires_action':
            # Continue the loop to handle the required action
            continue
        else:
            print(f"Unhandled status: {run.status}")
            break


def collect_tool_outputs(run: Any) -> List[Dict[str, Any]]:
    """
    Collects tool outputs based on the required actions in the run.

    :param run: The current run object.
    :return: A list of tool output dictionaries.
    """
    tool_outputs = []
    required_action = getattr(run, 'required_action', None)
    submit_tool_outputs = getattr(required_action, 'submit_tool_outputs', None)

    if submit_tool_outputs:
        for tool_call in submit_tool_outputs.tool_calls:
            tool_output = execute_tool_call(tool_call)
            if tool_output:
                tool_outputs.append(tool_output)
    return tool_outputs


def execute_tool_call(tool_call: Any) -> Optional[Dict[str, Any]]:
    """
    Executes a single tool call and returns the output.

    :param tool_call: The tool call object containing function details.
    :return: A dictionary with the tool call ID and output, or None if execution fails.
    """
    function_name = tool_call.function.name
    arguments = tool_call.function.arguments

    try:
        if arguments == '{}' or not arguments:
            # Case for tools that do not require passing arguments
            output = api_tools.call_func(function_name)
        else:
            # Case for tools that require passing arguments
            output = api_tools.call_func(function_name, arguments)
        return {
            "tool_call_id": tool_call.id,
            "output": output
        }
    except Exception as e:
        print(f"Failed to execute tool '{function_name}': {e}")
        return None


def process_solution(messages: Any) -> assist.SolvedPythonScript:
    """
    Processes the solution from the messages and returns a SolvedPythonScript object.

    :param messages: The messages object containing the solution data.
    :return: An instance of SolvedPythonScript.
    """
    try:
        message_content = messages.data[0].content[0].text.value
        solution = assist.SolvedPythonScript.model_validate_json(message_content)
        return solution
    except Exception as e:
        print(f"Failed to process solution: {e}")
        raise


def main() -> None:
    """
    The main function that initializes the client, assistant, thread, and run,
    then starts the LLM interaction loop.
    """
    client = OpenAI(api_key=environment.OPENAI_API_KEY)
    assistant = assist.create_assist(client)
    thread = assist.create_thread(client)
    run = assist.create_run(client, assistant, thread)
    run_llm(client, thread, run)


if __name__ == "__main__":
    main()
