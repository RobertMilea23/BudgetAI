import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_path = os.path.commonpath([abs_path, target_file]) == abs_path

        if valid_target_path == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok = True)

        with open(target_file, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file at the specified path relative to the working directory, creating any missing parent directories",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file. Overwrites any existing content",
            ),
        },
        required=["file_path", "content"],
    ),
)