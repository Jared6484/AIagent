import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
name="write_file",
description="Write to a file, given it is in the proper directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="Path to the file, relative to working dir."),
        "content": types.Schema(
            type=types.Type.STRING,
            description="Data to put into the file.",)            
        },
        required=["file_path"]
    ),
)

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path =  os.path.abspath(full_path)

    if not abs_full_path.startswith(abs_working_dir + os.sep):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    parent_dir = os.path.dirname(abs_full_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    try:
        with open(abs_full_path, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error:  cannot write to file "{file_path}": {str(e)}'
