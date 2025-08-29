from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python_file
from google.genai import types

WORKING_DIRECTORY = "./calculator"

FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call_part, verbose=False):

    func_name = function_call_part.name
    if function_call_part.args:
        func_args = function_call_part.args.copy()
    else:
        func_args = {}

    func_args["working_directory"] = WORKING_DIRECTORY

    #if verbose:
        #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    #    print(f"Calling function: {func_name}({func_args})")
    #else:
    #    print(f" - Calling function: {func_name}")

    if func_name not in FUNCTION_MAP:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"error": f"Unkown function:{func_name}"},
        )
    ],
)
    try:
        function_result = FUNCTION_MAP[func_name](**func_args)
    except Exception as e:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"error": str(e)},

        )
    ],
)
    # Return this
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=func_name,
            response={"result": function_result},
        )
    ],
)