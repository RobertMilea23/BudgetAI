import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_path = os.path.commonpath([abs_path, target_file]) == abs_path


        if valid_target_path == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path.endswith(".py") == False:
            return f'Error: "{file_path}" is not a Python file'

        
        command = ["python", target_file]

        if args:
            command.extend(args)
        
        result = subprocess.run(
            command,
            cwd = abs_path,
            capture_output = True,
            text = True,
            timeout = 30)

        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            if result.stdout:
                output += f"STDOUT: {result.stdout}"
            if result.stderr:
                output += f"STDERR: {result.stderr}"
        
        return output

    except Exception as e:
        return f"Error: executing python file: {e}"

