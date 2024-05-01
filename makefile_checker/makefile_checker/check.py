import os, fnmatch
from typing import List

from makefile_checker.makefile_checker.checker import Checker
from makefile_checker.makefile_checker.exceptions import MissingFilesException


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


def check():
    makefiles = get_makefiles_in_current_working_directory()

    all_alerts = []
    for makefile in makefiles:
        checker = Checker(makefile)
        all_alerts.extend(checker.get_missing_scripts_for_makefile(makefile))

    if len(all_alerts) > 0:
        raise MissingFilesException(all_alerts)