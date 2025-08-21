import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
name="run_python_file",
description="Runs file with output, any errors, and return-code.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="Path to the file, relative to working dir.",
            ),
        "args": types.Schema(
            type=types.Type.ARRAY,
            description="Optional list of string args to pass to the Python script",
            items=types.Schema(type=types.Type.STRING)
        )
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)

    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    if not abs_full_path.startswith(abs_working_dir + os.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(abs_full_path):
        return f'Error: File "{file_path}" not found.'
    elif not abs_full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    cmd = ['python3', abs_full_path] + args
    try:
        completed_process = subprocess.run(cmd, 
                                        cwd=working_directory, 
                                        timeout=30, 
                                        capture_output=True,
                                        text=True)
    except Exception as e:
        f"Error: executing Python file: {e}"

    final_output = f'STDOUT: {completed_process.stdout}.  STDERR: {completed_process.stderr}.  '

    if not completed_process.returncode == 0:
        return final_output + "Process exited with code X"
    elif final_output == "":
        return "No output produced."
    else:
        return final_output
    
    completed_process.stdout
    completed_process.stderr
    completed_process.returncode