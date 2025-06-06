import subprocess
import os
import csv
import time
from datetime import datetime

def run_command(command, cwd=None):
    """Run a shell command and return its output and error."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8')

def evaluate_bug(defects4j_path, project_name, bug_id, buggyFiles, fix_function, llm):
    #print(buggyFiles)
    """
    Evaluate a bug-fixing function on a buggy project from Defects4J.

    Args:
        defects4j_path (str): Path to Defects4J framework.
        project_name (str): Name of the project in Defects4J.
        bug_id (int): The bug ID to evaluate.
        fix_function (function): Function that takes the buggy code directory and applies a fix.

    Returns:
        dict: Result of the evaluation.
    """
    # Step 1: Checkout the buggy version
    working_dir = f"./tmp/{project_name}_{bug_id}"
    if os.path.exists(working_dir):
        subprocess.call(f"rm -rf {working_dir}", shell=True)
    checkout_command = f"defects4j checkout -p {project_name} -v {bug_id}b -w {working_dir}"
    output, error = run_command(checkout_command)
    #print(output)
    if error:
        print(f"Error during checkout for bug {bug_id} in project {project_name}: {error}")
        #return None

    # Step 2: Apply the bug-fixing function
    start_time = time.time()
    fix_success = fix_function(working_dir,buggyFiles, llm)
    if not fix_success:
        print(f"Fix function failed for bug {bug_id} in project {project_name}")
        return None

    # Step 3: Compile the fixed code
    compile_command = "defects4j compile"
    output, error = run_command(compile_command, cwd=working_dir)
    if "FAIL" in output or error:
        print(f"Compilation failed for bug {bug_id} in project {project_name}: {error}")
        return None

    # Step 4: Run the relevant test cases
    test_command = "defects4j test"
    output, error = run_command(test_command, cwd=working_dir)
    exec_time = time.time() - start_time

    # Step 5: Determine if the fix is successful
    success = "Failing tests: 0" in output

    return {
        "bug_id": bug_id,
        "project_name": project_name,
        "success": success,
        "exec_time": exec_time,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def save_results_to_csv(results, csv_filename):
    """Save evaluation results to a CSV file."""
    fieldnames = ['bug_id', 'project_name', 'success', 'exec_time', 'timestamp']
    write_header = not os.path.exists(csv_filename)

    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(results)

def get_bug_ids(defects4j_path, project_name):
    """Retrieve bug IDs for the given project from Defects4J."""
    command = f"defects4j query -p {project_name} -q 'classes.relevant.src'"
    output, error = run_command(command)
    if error:
        print(f"Error retrieving bug IDs for project {project_name}: {error}")
        return []
    
    # Initialize an empty dictionary
    output_dict = {}

    # Split the data into lines
    lines = output.strip().split("\n")
    
    # Process each line
    for line in lines:
        # Split each line into key and value based on the first comma
        key, value = line.split(",", 1)
        base_path = f"./tmp/{project_name}_{key}/src/main/java/"
        # Remove the surrounding quotes and split the classes by ';'
        value_list = value.strip('"').split(";")
        value_list = [base_path + v.replace(".", "/") + ".java" for v in value_list]
        # Convert the key to an integer and assign the list of values to the dictionary
        output_dict[int(key)] = value_list
    
    print(output_dict)
    return output_dict

def main(defects4j_path, projects, fix_function,llm, csv_filename='evaluation_results.csv'):
    """Main function to evaluate all bugs in the specified projects."""
    results = []

    for project_name in projects:
        bug_ids = get_bug_ids(defects4j_path, project_name)
        #print(bug_ids)
        for bug_id in bug_ids.keys():
            print(f"Evaluating bug {bug_id} in project {project_name}...")
            result = evaluate_bug(defects4j_path, project_name, bug_id, bug_ids[bug_id], fix_function,llm)
            if result:
                results.append(result)

    save_results_to_csv(results, csv_filename)

# Function to read the file content
def get_file_contents(file_path):
    print(file_path)
    try:
        with open(file_path, 'r') as file:
            # Read the file content
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to write the modified content back to the file
def write_file_contents(file_path, content):
    try:
        with open(file_path, 'w') as file:
            # Write the content back to the file
            file.write(content)
        return "File written successfully."
    except Exception as e:
        return f"An error occurred while writing the file: {e}"

# Dummy function that modifies the content
def dummy_function(content):
    # In this case, we'll just append a comment at the end of the content
    modified_content = content + "\n// This is a dummy modification.\n"
    return modified_content

 # Define a dummy bug-fixing function
def final_fix_function(bug_dir, buggyFiles,llm):
    """
    Placeholder function that simulates fixing a bug.
    """
    for file in buggyFiles: 
        output = get_file_contents(file)
    if(output != "File not found."):
        mod_output = llm(output)
    print(mod_output)
    write_file_contents(file, mod_output)


def evaluatorFunction(llm): 
    defects4j_path = "./defects4j"
    projects = ["Lang"]  
    main(defects4j_path, projects, final_fix_function, llm)
# Example usage
if __name__ == "__main__":
    defects4j_path = "./defects4j"
    projects = ["Lang"]  # List of Defects4J projects

    main(defects4j_path, projects, final_fix_function)
