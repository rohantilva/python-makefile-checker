import argparse
import re
import os, fnmatch
from pathlib import Path
from typing import List

NEWLINE = "\n"


def read_file_contents(path: str) -> str:
    """
    Given a path, read the contents of the file at that path.
    """
    makefile_contents = None
    with open(path) as file:
        makefile_contents = file.read()

    assert makefile_contents is not None, f"Empty file at {path}"
    return makefile_contents


def clean_and_parse_makefile_scripts(makefile_contents: str) -> List[str]:
    """    
    Clean the raw contents of a Makefile.
    Parse out the paths to scripts that are to be run.
    For example, remove comments and any line that is not a path to a script.

    e.g. If the Makefile contains:

    ```
    # This is a comment
    target:
        python this/is/a/script.py
        # This is another comment python this/is/a/script5.py
        python3 this/is/a/script2.py
    ```

    Then the cleaned contents should be:
    [
        "this/is/a/script.py",
        "this/is/a/script2.py"]
    ]

    TODO(rohantilva): just use a regex to parse out the paths to scripts.
    """

    # remove lines that do not start with "python"
    python_lines = [line.strip() for line in makefile_contents.split("\n") if line.strip().startswith("python")]

    scripts = []
    for line in python_lines:
        end_index = line.find(".py")
        line = line[:end_index + 3]
        scripts.append(line)

    return scripts


def get_makefiles_in_current_working_directory(pattern: str = "Makefile") -> List[str]:
    """
    Get all Makefiles that might exist in current working directory.
    There may be multiple Makefiles in different directories / projects.
    Grab them all, and validate them one by one.
    """
    path = os.getcwd()

    result = []
    for root, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def validate_make(path_to_makefile: str) -> List[str]:
    makefile_contents = read_file_contents(path_to_makefile)
    all_scripts = clean_and_parse_makefile_scripts(makefile_contents)

    # get base path that the scripts live under
    parts = path_to_makefile.strip("/").split("/")
    base_path = "/".join(parts[:len(parts) - 1])

    alerts = []
    for script in all_scripts:
        file_path = f"{base_path}/{script}"
        if not Path(file_path.strip("/")).is_file():
            alerts.append(file_path)

    return alerts


def check():
    makefiles = get_makefiles_in_current_working_directory()

    all_scripts = None
    for makefile in makefiles:
        validate_make(makefile)

