import os


def find_owner(path_file):
    try:
        import pwd
    except ModuleNotFoundError:
        return ""
    try:
        return pwd.getpwuid(os.stat(path_file).st_uid).pw_name
    except KeyError:
        return ""
