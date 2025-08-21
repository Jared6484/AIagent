import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
name="get_files_info",
description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "directory": types.Schema(
            type=types.Type.STRING,
            description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):

    full_path = os.path.join(working_directory, directory)

    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    if not abs_full_path.startswith(abs_working_dir):  # add + os.sep
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    try:
        contents = []
        for item in os.scandir(abs_full_path):
            size = os.path.getsize(item)
            is_dir = os.path.isdir(item)
            contents.append(f"- {item.name}: file_size={size} bytes, is_dir={is_dir}")
    

    except OSError as e:
        return f"Error: a problem occurred while accessing the directory: {str(e)}"

    header = f"Result for directory '{directory}':"
    return header + "\n" + "\n".join(contents)


