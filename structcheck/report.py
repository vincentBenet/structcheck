"""
Report scan functions
"""

import os
import re
import json
import datetime
import getpass

from . import utils


def generate(path_root, path_conf, path_report, path_data, reports, logs):
    """
    Report generation

    :param path_root:
    :param path_conf:
    :param path_report:
    :param path_data:
    :param reports:
    :param logs:
    :return:
    """
    reports = sorted(reports, key=lambda x: x[0])
    reports_txt = ""
    error_num = 1
    filter_errors = []
    with open(path_conf) as file:
        config = json.load(file)
    for report_i in reports:
        error_path, error_type, error_args = report_i
        is_root = error_path == path_root
        key = f"Error: {error_type}"
        owner = utils.find_owner(error_path)
        owner = owner if owner != '' else path_root
        report_error = f"{error_num}: {error_path[len(path_root) + 1:]} ({owner}) : {error_type} | {error_args}" + "\n"
        print(f"{re.match('^bla$', error_path) = }")
        print(f"{error_path = }")
        
        
        if (
                is_root and
                error_type in ["Empty directory", "Missing folder matching"] or
                error_path in [path_conf, path_report, path_data] or
				sum([1 for folder in config.get("ignored_folders", []) if re.match(folder, error_path[len(path_root)+1:])])
        ):
            filter_errors.append("".join(report_i))
            continue
        reports_txt += report_error
        error_num += 1
        logs[key] = logs.get(key, 0) + 1
        logs["Error"] = logs.get("Error", 0) + 1

    reports = [
        [error_path, error_type, error_args]
        for error_path, error_type, error_args in reports
        if "".join([error_path, error_type, error_args]) not in filter_errors
    ]

    if os.path.isfile(path_data):
        with open(path_data, "r", encoding="utf8") as file:
            try:
                logs_old = json.load(file)
            except:
                logs_old = {}
    else:
        logs_old = {}

    coverages = {
        "Coverage files": round(100 * (
            (logs.get('File presence checked', 0) + logs.get('File allowed validated', 0))
        ) / logs.get('Total files', -1), 2),
        "Coverage folders": round(100 * (
            (logs.get('Folder allowed checked', 0) + logs.get('Folder presence checked', 0))
        ) / logs.get('Total folders', -1), 2),
        "Allowed Files": round(100 *
                               logs.get('File allowed validated', 0) / logs.get('File allowed checked', -1), 2),
        "Allowed Folders": round(100 *
                                 logs.get('Folder allowed validated', 0) / logs.get('Folder allowed checked', -1), 2),
        "Presence Files": round(100 *
                                logs.get('File presence validated', 0) / logs.get('File presence checked', -1), 2),
        "Presence Folders": round(100 *
                                  logs.get('Folder presence validated', 0) / logs.get('Folder presence checked', -1),
                                  2),
    }

    diff = {}
    diff_txt = {}
    for coverage in coverages:
        diff[coverage] = round(coverages.get(coverage, 0) - logs_old.get(coverage, 0), 2)
        diff_txt[coverage] = f"{['', '+'][diff[coverage] >= 0]}{diff[coverage]}"

    txt = ("\n" + "_" * 50 + "INTRODUCTION" + "_" * 50) + "\n"
    txt += "Scan structures of files and folders" + "\n"
    txt += "This script use REGEX to validate files and folders structure. "
    txt += "Please find regex usage on < https://regex101.com/ >" + "\n"
    now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    txt += f"Scan : {now} by < {getpass.getuser()} >" + "\n"
    txt += ("\n" + "_" * 50 + "RESUME" + "_" * 50) + "\n"

    for keys in sorted(logs):
        difference = logs_old.get(keys, 0) - logs[keys]
        txt += f"{keys}: {logs[keys]} ({['', '+'][difference >= 0]}{difference})" + "\n"

    txt += "\n"
    txt += f"""Coverage files: {
    logs.get('File allowed checked', 0) + logs.get('File presence checked', 0)
    } / {logs.get('Total files', 0)} : {coverages['Coverage files']}% ({diff_txt['Coverage files']}%)""" + "\n"
    txt += f"""Coverage folders: {
    logs.get('Folder allowed checked', 0) + logs.get('Folder presence checked', 0)
    } / {logs.get('Total folders', 0)} : {coverages['Coverage folders']}% ({diff_txt['Coverage folders']}%)""" + "\n"
    txt += f"""Allowed Files: {
    logs.get('File allowed validated', 0)} / {logs.get('File allowed checked', 0)
    } : {coverages['Allowed Files']}% ({diff_txt['Allowed Files']}%)""" + "\n"
    txt += f"""Allowed Folders: {
    logs.get('Folder allowed validated', 0)} / {logs.get('Folder allowed checked', 0)
    } : {coverages['Allowed Folders']}% ({diff_txt['Allowed Folders']}%)""" + "\n"
    txt += f"""Presence Files: {
    logs.get('File presence validated', 0)} / {logs.get('File presence checked', 0)
    } : {coverages['Presence Files']}% ({diff_txt['Presence Files']}%)""" + "\n"
    txt += f"""Presence Folders: {
    logs.get('Folder presence validated', 0)} / {logs.get('Folder presence checked', 0)
    } : {coverages['Presence Folders']}% ({diff_txt['Presence Folders']}%)""" + "\n"
    txt += "\n" + "_" * 50 + "ERRORS" + "_" * 50 + "\n"
    txt += f'{reports_txt}' + "\n"

    with open(path_report, "w", encoding="utf8") as file:
        file.write(txt)

    with open(path_data, "w", encoding="utf8") as file:
        json.dump({**logs, **coverages}, file)

    return txt, reports, logs
