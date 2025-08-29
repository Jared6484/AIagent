import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python_file

from functions.call_function import call_function

def main():
    print("Hello from aiagent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    try:
        user_prompt = sys.argv[1]
    except IndexError:
        print("Error: No argument provided.")
        sys.exit(1)

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info, 
            schema_get_file_content,
            schema_run_python_file, 
            schema_write_file
            ]
        )

    
    #system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    loops = 0
    while loops<= 20:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        function_used = False
        for part in response.candidates[0].content.parts:
            #if response.function_calls:
            if part.function_call:
                #for function_call_part in response.function_calls:
                func = part.function_call
                #print(f"Calling function: {func.name}({func.args})")
                print(f"Calling function: {func.name}")
                    
                try:
                    function_call_result = call_function(func)
                    result = function_call_result.parts[0].function_response.response["result"]
                except Exception as e:
                    print(f"Fatality: {e}")
                    sys.exit(1)

                if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
                    print(f"-> {result}")

                messages.append(function_call_result)
                function_used = True
            if loops == 20: 
                print("Fatality: Reached 20 iterations without a final respons." )
                sys.exit(1)

        if not function_used:
            print(response.text)
            if len(sys.argv) >2 and sys.argv[2] == "--verbose":
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            break


if __name__ == "__main__":
    main()

'''

   
                # Check for function calls in the response parts
    if response.candidates and response.candidates[0].content.parts:  
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call_part = part.function_call
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                
                try:
                    function_call_result = call_function(function_call_part.name, function_call_part.args)
                    # The response from `call_function` needs to be handled correctly. 
                    # The original code's `function_call_result.parts[0].function_response.response` is likely incorrect.
                    # Assuming `call_function` returns a string or a structured object. Let's assume it returns a string for now.
                    result = function_call_result
                except Exception as e:
                    print(f"Fatality: {e}")
                    sys.exit(1)
                
                if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
                    print(f"-> {result}")'''