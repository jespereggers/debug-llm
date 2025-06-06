# importing openai module into your openai environment
from openai import OpenAI
import api_tools
import sys_tools
import environment
import assist
import LLMBenchmarkerFramework

# def llmFix(code):
#     completion = client.chat.completions.create(
#         model=environment.OPENAI_MODEL,
#         messages=[
#             {"role": "system", "content": "You are an expert Python developer"},
#             {
#                 "role": "user",
#                 "content": f"Find out if there is a bug in the given file and resolve it. Return the full code with the bug resolved,return nothing else.  {code}"
#             }
#         ]
#     )
#     #print(completion.choices[0].message.content)
#     return completion.choices[0].message.content.replace("```python", "").replace("```", "")

# LLMBenchmarkerFramework.LLMBenchmarker(llmFix)


from openai import OpenAI
import subprocess

class IterativeDebugger:
    def __init__(self, model, testCaseCode):
        self.client = OpenAI()
        self.model = model
        self.testCaseCode = testCaseCode

    def llm_get_info(self, buggy_code):
        messages = [
            {"role": "system", "content": "You are an expert Python developer"},
            {"role": "user", "content": f"Find the bug in this file and explain to me how I can fix it, do not fix the bug for me. {buggy_code}"}
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message.content.replace("```python", "").replace("```", "")

    def llm_fix(self, buggy_code, error_message=None, errorDescription=None):
        """Send the code and optionally an error message to the LLM for debugging."""
        messages = [
            {"role": "system", "content": "You are an expert Python developer"},
            {"role": "user", "content": f"Find the bug in this file and resolve it.Only return the code, return nothing extra {buggy_code}"}
        ]
        if error_message:
            messages.append(
                {"role": "user", "content": f"The following error occurred when testing the code: {error_message}. Please correct the bug.Only return the code, return nothing extra  {buggy_code}"}
            )
        if errorDescription: 
             messages.append(
                {"role": "user", "content": f"The following error occurred when testing the code: {error_message}. This is what the error means: {errorDescription}:  Please correct the bug. {buggy_code}"}
            )
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message.content.replace("```python", "").replace("```", "")

    def run_tests(self):
        """Runs the test script and returns the result."""
        # Read the test case from the file
        # Modify the test case to import the function from temp_code
        test_case_with_import = f"from fixed_code import *\n{self.testCaseCode}"
        # Execute the modified test case as a subprocess and capture output
        result = subprocess.run(
            ["python3", "-c", test_case_with_import],
            capture_output=True,
            text=True,
            timeout=10  # Timeout to prevent infinite loops
        )
        return result.returncode, result.stdout, result.stderr
    
    def writeCodeTempSpot(self,code):
        # Save the fixed code to a temporary Python file
        with open("temp_code.py", "w") as code_file:
            code_file.write(code)

    def iterative_debug(self, buggy_code):
        """Runs the iterative debugging process."""
        ite  = 0
        # Send code to LLM to fix
        fixed_code = self.llm_fix(buggy_code)
        print(fixed_code)
        # Test the fixed code
        with open('fixed_code.py', 'w') as file:
            file.write(fixed_code)

        return_code, output, error = self.run_tests()
        
        
        if return_code == 0:
            print("All tests passed! The bug is fixed.")
            return fixed_code
        else:
            print("ITER 1")
            print(f"Test failed with error:\n{error}")
            ite = ite + 1
            # On failure, retry with error passed to the LLM
            buggy_code = fixed_code  # Update to the last code attempt
            fixed_code = self.llm_fix(buggy_code, error_message=error)
        with open('fixed_code.py', 'w') as file:
            file.write(fixed_code)
        return_code, output, error = self.run_tests()
        print(fixed_code)
        
        if return_code == 0:
            print("All tests passed! The bug is fixed.")
            return fixed_code
        else:
            print("ITER 2")
            # On failure, retry with error passed to the LLM
            buggy_code = fixed_code  # Update to the last code attempt
            bug_info = self.llm_get_info(buggy_code)
            fixed_code = self.llm_fix(buggy_code, error_message=error,errorDescription=bug_info)
        
        with open('fixed_code.py', 'w') as file:
            file.write(fixed_code)
        return_code, output, error = self.run_tests()
        print("FINAL: ", return_code, output, error )
        return fixed_code

def iterativeDebuggerMainFunction(buggyCode, testCaseCode):

    # Example usage
    api_key = "your_openai_api_key"
    model = environment.OPENAI_MODEL # Specify model here
    test_script = "/Users/nitishgopinath/Documents/Github/24SS-DebugLLM/debugLLM/bug_code_organized/medium_errors/improper_exception_handling_test_case.py"  # Path to your test cases
    debugger = IterativeDebugger(model, testCaseCode)
    fixed_code = debugger.iterative_debug(buggyCode)
    return fixed_code

LLMBenchmarkerFramework.LLMBenchmarker(iterativeDebuggerMainFunction)