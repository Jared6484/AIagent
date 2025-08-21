import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python_file

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
    available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_file_content,schema_run_python_file, schema_write_file])

    
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

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
    )

    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    print(response.text)
    if len(sys.argv) >2 and sys.argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
