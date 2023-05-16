# PipMyRide

PipMyRide is a Python script that generates a pip install command from remote or local repositories. It can process GitHub repo URLs or local folder paths and concatenate all the Python or Jupyter Notebook files into a single text file. Then, it extracts all the imported libraries from the text file and creates a pip install command that can be copied to the clipboard or console.

## Requirements

- Python 3.6 or higher
- Requests
- Pyperclip
- Nbformat
- Nbconvert
```
pip install pyperclip nbconvert collections nbformat os requests pathlib re
```
## Usage

1. Clone or download this repository to your local machine.
2. Set your GitHub personal access token as an environment variable. Follow the instructions in the script comments to generate and set the token.
3. Run the script in your terminal or command prompt: `python pipmyride.py`
4. Enter a GitHub repo URL or a local folder path when prompted. For example: `https://github.com/username/repo` or `C:\Users\username\folder`
5. Wait for the script to process all the files and generate the pip install command.
6. The command will be copied to your clipboard and console. You can paste it in your terminal or command prompt to install the required libraries.

## Example


## How it works

- The program prompts the user to enter a valid GitHub repo URL or a local folder path as an input.
- It checks the input type and calls either the process_github_repo function or the process_local_folder function with the input and a default output filename as arguments.
- It iterates over all the files and subdirectories in the input using either requests or os.walk modules and downloads them to temporary files if they are remote using requests module.
- It converts any Jupyter Notebook files into Python code using nbformat and nbconvert modules and returns the code as a string.
- It concatenates all the Python code into a single text file and writes some comments indicating the original filenames and paths using os.path module.
- It extracts all the imported libraries from the text file using regular expressions and re module and stores them in a set.
- It generates a pip install command using the libraries and joins them with spaces using str.join method.
- It copies the command to the clipboard using pyperclip module and prints it to the console using print function.

## License

This project is licensed under the MIT License.
