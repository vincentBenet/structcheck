"""
Generic tools usage in the repository.
"""

import os


def find_owner(path_file):
    """
    Get the owner of a file.

    :param path_file:
    :return:
    """
    try:
        import pwd
    except ModuleNotFoundError:
        return ""
    try:
        return pwd.getpwuid(os.stat(path_file).st_uid).pw_name
    except KeyError:
        return ""
