from pathlib import Path
from typing import List


class Checker:

    def __init__(self, path_to_makefile: str):
        self.path_to_makefile = path_to_makefile


    def read_file_contents(self) -> str:
        """
        Given a path, read the contents of the file at that path.
        """
        makefile_contents = None
        with open(self.path_to_makefile) as file:
            makefile_contents = file.read()

        assert makefile_contents is not None, f"Empty file at {self.path_to_makefile}"
        return makefile_contents


    def clean_and_parse_makefile_scripts(self, makefile_contents: str) -> List[str]:
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
            "this/is/a/script2.py"
        ]

        TODO(rohantilva): just use a regex to parse out the paths to scripts.
        """

        # remove lines that do not start with "python"
        python_lines = [line.strip() for line in makefile_contents.split("\n") if line.strip().startswith("python")]

        scripts = []
        for line in python_lines:
            end_index = line.find(".py")
            line = line[:end_index + 3]
            start_index = line.rindex(" ")
            line = line[start_index + 1:]
            scripts.append(line)

        return scripts


    def get_missing_scripts_for_makefile(self) -> List[str]:
        makefile_contents = self.read_file_contents(self.path_to_makefile)
        all_scripts = self.clean_and_parse_makefile_scripts(makefile_contents)

        # get base path that the scripts live under
        parts = self.path_to_makefile.strip("/").split("/")
        base_path = "/".join(parts[:len(parts) - 1])

        alerts = []
        for script in all_scripts:
            file_path = f"/{base_path}/{script.strip()}"
            if not Path(file_path).is_file():
                alerts.append(file_path)

        return alerts
