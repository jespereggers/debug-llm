import os
import subprocess
import csv
import time

# Dummy LLM function to simulate code fixing (Replace this with actual LLM API call)
def llm_fix_code(buggy_code):
    # Simulate an LLM by fixing common bugs (this is just an example, replace it with your LLM API)
    fixed_code = buggy_code.replace("buggy", "fixed")  # Placeholder fix
    return fixed_code

# Function to run the test case and evaluate the result
def run_test_case(fixed_code, test_case):
    try:
        # Save the fixed code to a temporary Python file
        with open("temp_code.py", "w") as code_file:
            code_file.write(fixed_code)
        
        # Modify the test case to import the function from temp_code
        test_case_with_import = f"from temp_code import *\n{test_case}"
        
        # Execute the modified test case as a subprocess and capture output
        result = subprocess.run(
            ["python3", "-c", test_case_with_import],
            capture_output=True,
            text=True,
            timeout=10  # Timeout to prevent infinite loops
        )
        
        # Check if the test passed (no exception)
        if result.returncode == 0:
            return "Pass"
        else:
            return f"Fail: {result.stderr.strip()}"
    except Exception as e:
        return f"Error: {str(e)}"

# Framework to iterate over bug files, send code to LLM, and run test cases
def evaluate_and_fix_code(bug_file_path, test_case_file_path,LLM):
    # Read the buggy code from the file
    with open(bug_file_path, "r") as bug_file:
        buggy_code = bug_file.read()
    
    # Read the test case from the file
    with open(test_case_file_path, "r") as test_case_file:
        test_case = test_case_file.read()

    # Time how long it takes to send the buggy code to the LLM and receive the fix
    start_time = time.time()
    fixed_code = LLM(buggy_code, test_case)
    end_time = time.time()

    time_taken = end_time - start_time  # Time taken to fix the code
    
    # Run the test case on the fixed code
    test_result = run_test_case(fixed_code, test_case)
    
    # Determine if the bug was fixed based on the test result
    bug_fixed = test_result == "Pass"
    
    return bug_fixed, time_taken, test_result

# CSV file to store the results
csv_file = "code_fix_metrics.csv"

# Directory where the buggy code and test case files are saved
base_dir = "bug_code_organized"

# Main function to iterate over all files, evaluate and fix the code, and save results to a CSV
def LLMBenchmarker(LLM):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Bug Type", "Bug Name", "Bug Fixed", "Time Taken (s)", "Test Result"])

        # Iterate over the different bug types (extra_long_errors, long_errors, medium_errors, etc.)
        for bug_type_dir in os.listdir(base_dir):
            bug_type_path = os.path.join(base_dir, bug_type_dir)
            if os.path.isdir(bug_type_path):
                # Iterate over all the Python files in each directory
                for file_name in os.listdir(bug_type_path):
                    if file_name.endswith(".py") and not file_name.endswith("_test_case.py"):
                        bug_file_path = os.path.join(bug_type_path, file_name)
                        test_case_file_path = bug_file_path.replace(".py", "_test_case.py")

                        # Check if the corresponding test case exists
                        if os.path.exists(test_case_file_path):
                            bug_name = file_name.replace(".py", "")
                            print(f"Evaluating bug: {bug_name}")

                            # Evaluate and fix the buggy code
                            bug_fixed, time_taken, test_result = evaluate_and_fix_code(bug_file_path, test_case_file_path,LLM)

                            # Write the results to the CSV file
                            writer.writerow([bug_type_dir, bug_name, bug_fixed, round(time_taken, 4), test_result])

                            # Print result for quick feedback
                            print(f"Test Result for {bug_name}: {test_result}")
                            print(f"Bug Fixed: {bug_fixed}, Time Taken: {round(time_taken, 4)}s")
                            print("-" * 80)

if __name__ == "__main__":
    evaluate_and_fix_code()
