"""
Report scan functions
"""

import os
import re
import json
import datetime
import getpass

from . import utils


def generate(config, reports, logs):
    """
    Report generation

    :param path_root:
    :param path_conf:
    :param path_report:
    :param path_data:
    :param reports:
    :param logs:
    :param config:
    :return:
    """
    print(f"Generating report at {config['paths']['report']}")
    reports = sorted(reports, key=lambda x: x[0])
    reports_txt = ""
    error_num = 1
    filter_errors = []
    for report_i in reports:
        error_path, error_type, error_args = report_i
        is_root = error_path == config['paths']['root']
        key = f"Error: {error_type}"
        owner = utils.find_owner(error_path)
        owner = owner if owner != '' else config['paths']['root']
        report_error = f"{error_num}: {error_path[len(config['paths']['root']):]} ({owner}) : {error_type} | {error_args}" + "\n"
        first_elem = error_path[len(config['paths']['root']):]
        if first_elem.startswith(os.sep):
            first_elem = first_elem[1:]
        first_elem = first_elem.split(os.sep)[0]
        if (
            first_elem in config['ignored_paths'] or
            is_root and
            error_type in ["Empty directory", "Missing folder matching"] or
            error_path in [
                config['paths']['structure'],
                config['paths']['report'],
                config['paths']['config_report'],
                config['paths']['graph'],
                config['paths']['data'],
                config['paths']['graph_svg'],
                config['paths']['config_report'],
            ]
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

    if os.path.isfile(config['paths']['data']):
        with open(config['paths']['data'], "r", encoding="utf8") as file:
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
    txt += f"Paths : {config['paths']}" + "\n"
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

    with open(config['paths']['report'], "w", encoding="utf8") as file:
        file.write(txt)

    with open(config['paths']['data'], "w", encoding="utf8") as file:
        json.dump({**logs, **coverages}, file, indent=4)

    return txt, reports, logs
