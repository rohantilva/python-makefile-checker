from typing import List


class MissingFilesException(Exception):
    def __init__(self, missing_files: List[str]):
        self.missing_files = missing_files

    def __str__(self):
        base_alert = "Missing files:"
        for file in self.missing_files:
            base_alert += f"\n{file}"
        return base_alert
