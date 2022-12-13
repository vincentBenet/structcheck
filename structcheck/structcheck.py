"""
Main file of structure check
"""

import os
import sys
import json
import argparse
import pkg_resources

print(f"structckeck version = {pkg_resources.get_distribution('structcheck').version}")

try:
    import tkinter
    import tkinter.filedialog

    TK = True
except ModuleNotFoundError:
    TK = False

from . import recscan
from . import report
from . import to_graphviz
from . import regex


def scan(argu=None):
    args = parse(argu)
    args = check_args(args)
    return main(
        args["root"],
        args["conf"],
        args["report"],
        args["data"],
        args["names"],
        args["variables"],
        args["styles"],
    )


def parse(args=None):
    """
    Argument parsing function for shell-call.

    :return:
    """
    args = sys.argv[1:] if args is None else args
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        '-c', '--conf', metavar='conf_path', type=str, help='Path of the config structure.', default=None)
    parser.add_argument(
        '-p', '--root', metavar='root_path', type=str, help='Path of the root structure to check.', default=None)
    parser.add_argument(
        '-r', '--report', metavar='report_path', type=str, help='Path of the text report file.', default=None)
    parser.add_argument(
        '-d', '--data', metavar='data_path', type=str,
        help='Path of the json data file to calculate diff with last scan.', default=None)
    parser.add_argument(
        '-n', '--names', metavar='names_path', type=str,
        help='Path of the json file to names of structure.', default=None)
    parser.add_argument(
        '-v', '--variables', metavar='variables_path', type=str,
        help='Path of the json file to variable names.', default=None)
    parser.add_argument(
        '-s', '--styles', metavar='styles_path', type=str,
        help='Path of the json file to styles configuration for graph.', default=None)
    return vars(parser.parse_args(args))


def check_args(args_input):
    """
    Checking arguments of input.

    :param args_input:
    :return:
    """
    if args_input.get("root", None) is None:  # Input folder path
        while TK:
            root = tkinter.Tk()
            root.withdraw()
            root.update()
            args_input["root"] = tkinter.filedialog.askdirectory(
                initialdir=os.getcwd(),
                title="Select the root of architecture folder",
            )
            root.destroy()
            if args_input["root"] != "":
                break
    if args_input.get("conf", None) is None:  # Input file path
        default_path = os.path.join(
            args_input["root"],
            "config.json"
        )
        if os.path.isfile(default_path):
            args_input["conf"] = default_path
        else:
            while TK:
                root = tkinter.Tk()
                root.withdraw()
                root.update()
                args_input["conf"] = tkinter.filedialog.askopenfilename(
                    initialdir=default_path,
                    title="Select the structure configuration file",
                    filetypes=(("Struct check Files", "*.json"),)
                )
                root.destroy()
                if args_input["conf"] != "":
                    break
    if args_input.get("report", None) is None:  # Output text file path
        args_input["report"] = os.path.join(
            args_input["root"],
            "report.txt"
        )
    if args_input.get("data", None) is None:  # Output data save file path
        args_input["data"] = os.path.join(
            args_input["root"],
            "report.json"
        )
    if args_input.get("names", None) is None:
        args_input["names"] = args_input["conf"]
    if args_input.get("variables", None) is None:
        args_input["variables"] = args_input["conf"]
    if args_input.get("styles", None) is None:
        args_input["styles"] = args_input["conf"]
    print(f"{args_input = }")
    return args_input


def main(
        path_root: str,
        path_conf: str,
        path_report: str,
        path_data: str,
        path_names: str,
        path_variables: str,
        path_styles: str,
        display: bool = True
):
    """
    Main call of librairy.

    :param path_root:
    :param path_conf:
    :param path_report:
    :param path_data:
    :param path_data:
    :param path_data:
    :param path_names:
    :param path_variables:
    :param path_styles:
    :param display:
    :return:
    """

    # Creating single config dict
    config = {"paths": {}}
    with open(path_conf, "r", encoding="utf8") as file:
        print(f"Loading config file {path_conf = }")
        config.update(json.load(file))
        config["paths"]["structure"] = path_conf
    with open(path_names, "r", encoding="utf8") as file:
        print(f"Loading config file {path_names = }")
        config.update(json.load(file))
        config["paths"]["names"] = path_names
    with open(path_variables, "r", encoding="utf8") as file:
        print(f"Loading config file {path_variables = }")
        config.update(json.load(file))
        config["paths"]["variables"] = path_variables
    with open(path_styles, "r", encoding="utf8") as file:
        print(f"Loading config file {path_styles = }")
        config.update(json.load(file))
        config["paths"]["styles"] = path_styles
    config["paths"]["root"] = path_root
    config["paths"]["report"] = path_report
    # Build regex config
    config["structure_regexes"] = regex.buid_structure_regex(
        config["structure"],
        config["names"],
        config["variables"]
    )
    config["structure_names"] = regex.buid_structure_names(config["structure"], config["names"])

    config["paths"]["data"] = path_data
    config["paths"]["graph"] = os.path.join(os.path.dirname(path_report), "graph.gv")  # Output path for graph next to report in gv format
    config["paths"]["graph_svg"] = os.path.join(os.path.dirname(path_report), "graph.svg")  # Output path for graph next to report in svg
    config["paths"]["config_report"] = os.path.join(os.path.dirname(path_report), "config.json")

    with open(config["paths"]["config_report"], "w") as file:
        json.dump(config, file, indent=4)

    to_graphviz.main(config)  # Create a graph based on config

    reports, logs = recscan.init_scan(config)
    reports, logs = recscan.check_unallowed(config['paths']['root'], config['structure_regexes'], config, report=reports, log=logs)
    reports, logs = recscan.check_unpresent(config['paths']['root'], config['structure_regexes'], reports, logs)
    txt, reports, logs = report.generate(config, reports, logs)

    if display:
        print(txt)
    return txt, reports, logs


if __name__ == "__main__":
    scan()
