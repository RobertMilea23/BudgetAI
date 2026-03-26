import os

def get_files_info(working_directory, directory="."):
    try:


        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'


        contents = []

        for filename in os.listdir(target_dir):
            full_path = os.path.join(target_dir, filename)
            size = os.path.getsize(full_path)
            contents.append(f"- {filename}: file_size={size} bytes, is_dir={os.path.isdir(full_path)}")
        return "\n".join(contents)


    except Exception as e:
            return f"Error: {e}"
