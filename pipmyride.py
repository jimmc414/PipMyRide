import os
import re
import requests
import pyperclip
from collections import defaultdict
from pathlib import Path
import nbformat
from nbconvert import PythonExporter

# Github Personal Access Token Required
# 1. Log in to your GitHub account.
# 2. Go to "Settings" from the profile dropdown menu (in the top right corner).
# 3. Click "Developer settings" at the bottom of the left sidebar.
# 4. Click "Personal access tokens" in the left sidebar.
# 5. Click "Generate new token" button near the top.
# 6. Add a note to describe your token and select the relevant permissions. (For this script, at least 'repo' permission is required)
# 7. Click "Generate token" button at the bottom.
   # - For Linux/Mac:

      # export GITHUB_TOKEN="your_token"
   
   # - For Windows: 
      
      # setx GITHUB_TOKEN "your_token"

TOKEN = os.environ.get("GITHUB_TOKEN")
headers = {"Authorization": f"token {TOKEN}"}

def download_file(url, target_path):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(target_path, "wb") as f:
        f.write(response.content)

def is_allowed_filetype(filename):
    allowed_extensions = ['.py']
    return any(filename.endswith(ext) for ext in allowed_extensions)

def process_ipynb_file(temp_file):
    with open(temp_file, "r", encoding='utf-8', errors='ignore') as f:
        notebook_content = f.read()

    exporter = PythonExporter()
    python_code, _ = exporter.from_notebook_node(nbformat.reads(notebook_content, as_version=4))
    return python_code

def process_directory(url, output):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    files = response.json()

    for file in files:
        if file["type"] == "file" and is_allowed_filetype(file["name"]):
            print(f"Processing {file['path']}...")

            temp_file = f"temp_{file['name']}"
            download_file(file["download_url"], temp_file)

            output.write(f"# {'-' * 3}\n")
            output.write(f"# Filename: {file['path']}\n")
            output.write(f"# {'-' * 3}\n\n")

            if file["name"].endswith(".ipynb"):
                output.write(process_ipynb_file(temp_file))
            else:
                with open(temp_file, "r", encoding='utf-8', errors='ignore') as f:
                    output.write(f.read())

            output.write("\n\n")
            os.remove(temp_file)
        elif file["type"] == "dir":
            process_directory(file["url"], output)

def process_local_directory(local_path, output):
    for root, dirs, files in os.walk(local_path):
        for file in files:
            if is_allowed_filetype(file):
                print(f"Processing {os.path.join(root, file)}...")

                output.write(f"# {'-' * 3}\n")
                output.write(f"# Filename: {os.path.join(root, file)}\n")
                output.write(f"# {'-' * 3}\n\n")

                file_path = os.path.join(root, file)

                if file.endswith(".ipynb"):
                    output.write(process_ipynb_file(file_path))
                else:
                    with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                        output.write(f.read())

                output.write("\n\n")

def process_github_repo(repo_url, output_file):
    api_base_url = "https://api.github.com/repos/"
    repo_url_parts = repo_url.split("https://github.com/")[-1].split("/")
    repo_name = "/".join(repo_url_parts[:2])

    # Check if a subdirectory is provided
    subdirectory = ""
    if len(repo_url_parts) > 4 and repo_url_parts[2] == "tree":
        subdirectory = "/".join(repo_url_parts[4:])

    contents_url = f"{api_base_url}{repo_name}/contents"
    if subdirectory:
        contents_url = f"{contents_url}/{subdirectory}"

    with open(output_file, "w", encoding='utf-8') as output:
        process_directory(contents_url, output)

    print("All files processed.")

def process_local_folder(local_path, output_file):
    with open(output_file, "w", encoding='utf-8') as output:
        process_local_directory(local_path, output)

    print("All files processed.")

def process_input(input_path, output_file):
    if input_path.startswith("http"):
        process_github_repo(input_path, output_file)
    elif os.path.isdir(input_path):
        process_local_folder(input_path, output_file)
    else:
        print("Invalid input. Please provide a GitHub repo URL or a local folder path.")

def process_input_file(input_file_path):
    libraries = set()
    library_pattern = re.compile(r"^import (\w+)|^from (\w+)", re.MULTILINE)
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        input_text = input_file.read()
        library_matches = library_pattern.findall(input_text)
        for match in library_matches:
            library = match[0] if match[0] else match[1]
            libraries.add(library)

    pip_install_command = generate_pip_install_commands(libraries)
    return pip_install_command

def generate_pip_install_commands(libraries):
    pip_install_command = "pip install " + " ".join(libraries)
    return pip_install_command

def main():
    input_path = input("Enter GitHub repo URL or local folder path: ")
    output_filename = "concatenated_files.txt"
    process_input(input_path, output_filename)

    input_file_path = output_filename
    pip_install_command = process_input_file(input_file_path)

    pyperclip.copy(pip_install_command)
    print("\nGenerated pip install command:")
    print(pip_install_command)
    print("\nThe command has been copied to your clipboard and console.")

if __name__ == "__main__":
    main()