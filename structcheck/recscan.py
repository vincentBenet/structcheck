"""
Recursive scan functions
"""

import re
import os
import datetime


def init_scan(path_root, config):
    """
    First scan of tree structure to check for empty directory

    :param path_root:
    :param config:
    :return:
    """
    logs = {
        "Total files": 0,
        "Total folders": 0,
        "Total empty directory": 0,
        "Errors": 0
    }

    for raw, _, files in os.walk(path_root):
        ignore = False
        for ignored_folder in config.get("ignored_folders", []):
            if raw.startswith(os.path.join(path_root, ignored_folder)):
                ignore = True
        if not ignore:
            logs["Total files"] += len(files)
            logs["Total folders"] += 1
        if len(files) == 0:
            logs["Total empty directory"] += 1

    return logs


def check_iter_unallowed_dict(
        path_file, struct, dates_format, report=None, log=None, date_parent=None, key=None, path_next=None):
    """
    Check for not allowed foldersand dates non-regression.

    :param path_file:
    :param struct:
    :param dates_format:
    :param report:
    :param log:
    :param date_parent:
    :param key:
    :param path_next:
    :return:
    """
    log["Folder allowed validated"] = log.get("Folder allowed validated", 0) + 1
    date_call = date_parent
    validate_iter = True
    for date_regex in dates_format:
        if date_regex not in key:
            continue
        regex = re.search(date_regex, path_next)
        if not regex:
            continue
        date_str = regex.group(0)
        date_file = datetime.datetime.strptime(date_str, dates_format[date_regex])
        if date_parent is None:
            date_call = date_file
        elif date_file < date_parent:
            report.append([path_file, "Date folder anteriority", f"> {date_file} < higher than > {date_parent}"])
        else:
            log["Date folder validation"] = log.get("Date folder validation", 0) + 1
            if date_parent is None:
                date_parent = date_file
            elif date_parent < date_file:
                date_call = date_file
        break
    report, log = check_unallowed(path_file, struct[key], dates_format, report, log, date_call)
    return report, log, validate_iter, date_parent


def check_iter_unallowed_list(path_file, struct, dates_format, report=None, log=None, date_parent=None, key=None,
                              path_next=None):
    """
    Check for not allowed files and date corresponding.

    :param path_file:
    :param struct:
    :param dates_format:
    :param report:
    :param log:
    :param date_parent:
    :param key:
    :param path_next:
    :return:
    """
    validate_iter = False
    for struct_file in struct[key]:
        if re.match(struct_file, path_next) or path_next == struct_file:
            log["File allowed validated"] = log.get("File allowed validated", 0) + 1
            validate_iter = True
            for date_regex in dates_format:
                if date_regex in struct_file:
                    regex = re.search(date_regex, path_next)
                    if not regex:
                        continue
                    date_str = regex.group(0)
                    date_file = datetime.datetime.strptime(date_str, dates_format[date_regex])
                    if date_parent is None:
                        pass
                    elif date_file != date_parent:
                        report.append([path_file, "Date file different",
                                       f"> {date_file} < different of parent date > {date_parent} <"])
                    else:
                        log["Date file validation"] = log.get("Date file validation", 0) + 1
                    break
            break
    return report, log, validate_iter, date_parent


def check_unallowed(path, struct, dates_format, report=None, log=None, date_parent=None):
    """
    Run scan for not allowed paths.

    :param path:
    :param struct:
    :param dates_format:
    :param report:
    :param log:
    :param date_parent:
    :return:
    """
    if report is None:
        report = []
    if log is None:
        log = {}
    if not isinstance(struct, dict):
        return report, log
    for path_next in os.listdir(path):
        path_file = os.path.join(path, path_next)
        if os.path.isfile(path_file):
            log["File allowed checked"] = log.get("File allowed checked", 0) + 1
        elif os.path.isdir(path_file):
            log["Folder allowed checked"] = log.get("Folder allowed checked", 0) + 1
        validate_iter = False
        for key in struct:
            if (
                isinstance(struct[key], dict) and
                (
                    key.startswith("^") and
                    key.endswith("$")
                ) and
                re.match(key, path_next) or
                path_next == key
            ):
                report, log, validate_iter, date_parent = check_iter_unallowed_dict(path_file, struct, dates_format,
                                                                                    report, log, date_parent, key,
                                                                                    path_next)
            elif isinstance(struct[key], list):
                report, log, validate_iter, date_parent = check_iter_unallowed_list(path_file, struct, dates_format,
                                                                                    report, log, date_parent, key,
                                                                                    path_next)
            if validate_iter:
                break
        if validate_iter:
            continue
        if os.path.isfile(path_file):
            report.append([
                path_file,
                "Not allowed file",
                f"< {path_next} >. Allowed matches : {struct.get('Files', []) + struct.get('Files_optionnal', [])}"
            ])
        elif os.path.isdir(path_file):
            report.append([
                path_file,
                "Not allowed folder",
                f"""< {path_next} >. Allowed matches : {
                    struct.get('Files', []) + struct.get('Files_optionnal', []) +
                    [k for k in struct if k not in ['Files', 'Files_optionnal']]
                }"""])
    return report, log


def check_unpresent(path, struct, report=None, log=None):
    """
    Check if all declared paths are presents in structure.

    :param path:
    :param struct:
    :param report:
    :param log:
    :return:
    """
    if report is None:
        report = []
    if log is None:
        log = {}
    if os.path.isfile(path):
        return report, log
    dirs = os.listdir(path)
    if len(dirs) == 0 and struct != {}:
        report.append([path, "Empty directory", ""])
    else:
        for key in struct:
            not_found = True
            breaker2 = False
            for path_next in dirs:
                path_file = os.path.join(path, path_next)
                log["Folder presence checked"] = log.get("Folder presence checked", 0) + os.path.isdir(path_file)
                if isinstance(struct[key], list):
                    for key2 in struct[key]:
                        for path_next2 in dirs:
                            log["File presence checked"] = log.get("File presence checked", 0) + 1
                            if (
                                key2.startswith("^") and
                                key2.endswith("$") and
                                re.match(key2, path_next2) or
                                path_next2 == key2
                            ):
                                log["File presence validated"] = log.get("File presence validated", 0) + 1
                                break
                        else:
                            if key.endswith("_optionnal"):
                                continue
                            report.append([path, "Missing file matching",
                                           f"> {key2} <. Directory content : {dirs if len(dirs) else '> EMPTY <'}"])
                            breaker2 = True
                            break
                elif (
                    isinstance(struct[key], dict) and
                    (
                        key.startswith("^") and
                        key.endswith("$")
                    ) and
                        re.match(key, path_next) or
                        path_next == key
                ):
                    not_found = False
                    log["Folder presence validated"] = log.get("Folder presence validated", 0) + 1
                    report, log = check_unpresent(path_file, struct[key], report, log)
                if breaker2:
                    break
            else:
                if not_found and len(struct) > 0 and key not in ["Files", "Files_optionnal"] and key not in struct.get(
                        'Files_optionnal', []):
                    report.append([path, "Missing folder matching",
                                   f"> {key} <. Directory content : {dirs if len(dirs) else '> EMPTY <'}"])
    return report, log
