# DebugLLM
DebugLLM runs multiple contextual attempts, executes local functions, benefits from structured output formats and live-checks solutions for compilability.

Modular built, expandable and located in `debugLLM`.

#### Run DebugLLM
1. Point `INPUT_PATH` in `debugLLM/environment.py` to your Python file.
2. Run `main.py`.
3. Check `debugLLM/output`.

#### Run Iterative debugger
1. run ```export OPENAI_API_KEY= <YOUR_OPEN_AI_KEY>``` in the command line
2. Run `iterativeDebugger.py`
3. check  `code_fix_metrics.csv` for output

## Components

### main.py
Initializes OpenAI client, creates assistant-, thread- and run-object. Request to agent is sent in `run_llm`-function. While tool-outouts are being ran through in `collect_tool_outputs`, the actual execution is outsourced to `execute_tool_call`. In case the run-status is complete, `process_solution` checks for output validity, otherwise the process repeats. Explanation gets printed to terminal and solved script saved into `OUTPUT_PATH` defined in `environment.py`.

The output-format is binded to the `SolvedPythonScript` class and referenced from `assist.py`.

### IterativeDebugger class: The core class that implements the iterative debugging process.
1. ##### llm_fix: Sends the code to the LLM for fixing based on the provided error message and error description.
2. ##### llm_get_info: Retrieves an explanation of the bug from the LLM without directly fixing it.
3. ##### run_tests: Runs the test cases on the current code iteration and captures any errors.
4. ##### iterative_debug: Main function that executes iterative debugging, rerunning tests after each fix attempt.

### assit.py
Provides functions to create assistant-, file-, thread- and run-object.
`SolvedPythonScript` serves as required output-format for the agent.

### environment.py
Collection of all system-wide constants, such as agent instruction prompt and API-keys.

### api_tools.py
All custom functions accessable to the agent. Function-call works via `call_func`.
Currently `get_script` pulls scripts from the file-system, `check_syntax` verifies syntax-validty at runtime and `get_project_index` maps the entire project by its files, functions and params.

### sys_tools.py
Generic multi-purpose functions, such as `save_script`, `load_script` and `get_script_overview` to index a single script. `get_all_files` runs DFS and returns all files within a folder (including subfolders). Both functions are used for `get_project_index` in `api_tools.py`.

### training/fine_tuning.py
Uploads training data stored in `TRAINING_PATH` (defined in `environment.py`), starts and lists fine-tuning jobs.

### training/format_checker.py
Useful for checking validity of training-material before uploading for actual fine-tuning.

### Code Benchmarking Framework
This Python script provides a framework to evaluate and fix buggy code using a Language Learning Model (LLM) and measure performance. The key functionalities of the script include:
1. ##### LLM-Based Code Fixing: The script sends buggy code to an LLM API (currently simulated by a placeholder function) to automatically fix errors. You can replace this dummy function with an actual LLM API call for real-world scenarios.
2. ##### Test Case Execution: After fixing the code, it runs predefined test cases for each buggy file using Python's subprocess module. If the test case passes, the bug is considered fixed.
3. ##### CSV Metrics Logging: The script stores the results of each bug fix attempt, including the bug type, name, whether the bug was fixed, time taken to fix, and the test case result in a CSV file (code_fix_metrics.csv).
4. ##### Batch Processing: It processes multiple bug files stored in an organized directory structure (bug_code_organized), where each subdirectory represents a bug type and contains Python files (buggy code) and corresponding test case files.
 
## Agent specifications
### Custom Function Calling
https://platform.openai.com/docs/guides/function-calling
#### Extend custom functions
1. Write function in api_tools.py
3. Add tool in create_assistant, found in main.py

### Structured Outputs
https://platform.openai.com/docs/guides/structured-outputs
#### Adjust output format
1. Open main.py
2. Change object structure of SolvedPythonScript