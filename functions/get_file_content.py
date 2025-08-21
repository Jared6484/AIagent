from config import MAX_CHARS
import os
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
name="get_file_content",
description="Print the first 10,000 characters in a file.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="Path to the file, relative to working dir.",
        ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    file_path = os.path.join(working_directory, file_path)

    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(file_path)

    if not abs_full_path.startswith(abs_working_dir):  # add + os.sep
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(file_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)  #max chars in config file.

    if os.path.getsize(file_path) > MAX_CHARS:
        file_content_string += f'\n[...File "{file_path}" truncated at 10000 characters]'

    return file_content_string