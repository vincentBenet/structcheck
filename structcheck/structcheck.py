import os
import sys
import json
import argparse
import tkinter
import tkinter.filedialog

import recscan, report

def parse(sysargv):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', '--conf', metavar='conf_path', type=str, help='Path of the config structure.', default=None)
    parser.add_argument('-p', '--root', metavar='root_path', type=str, help='Path of the root structure to check.', default=None)
    parser.add_argument('-r', '--report', metavar='report_path', type=str, help='Path of the text report file.', default=None)
    parser.add_argument('-d', '--data', metavar='data_path', type=str, help='Path of the json data file to calculate diff with last scan.', default=None)
    return vars(parser.parse_args())


def check_args(args_input):
    if args_input.get("root", None) is None:  # Input folder path
        while True:
            root = tkinter.Tk()
            root.withdraw()
            root.update()
            args_input["root"] = tkinter.filedialog.askdirectory(
                initialdir= os.getcwd(),
                title= "Select the root of architecture folder",
            )
            root.destroy()
            if args_input["root"] != "":
                break
    if args_input.get("conf", None) is None:  # Input file path
        default_path = os.path.join(
            args_input["root"],
            ".structcheck.json"
        )
        if os.path.isfile(default_path):
            args_input["conf"] = default_path
        else:
            while True:
                root = tkinter.Tk()
                root.withdraw()
                root.update()
                args_input["conf"] = tkinter.filedialog.askopenfilename(
                    initialdir= default_path,
                    title= "Select the structure configuration file",
                    filetypes = (("Struct check Files", "*.json"),)
                )
                root.destroy()
                if args_input["conf"] != "":
                    break
    if args_input.get("report", None) is None:  # Output text file path
        args_input["report"] = os.path.join(
            args_input["root"],
            "structcheck.txt"
        )
    if args_input.get("data", None) is None:  # Output data save file path
        args_input["data"] = os.path.join(
            args_input["root"],
            ".structdata.json"
        )
    
    return args_input


def main(path_root, path_conf, path_report, path_data, display=True):
    with open(path_conf, "r") as f:
        config = json.load(f)
    logs = recscan.init_scan(path_root, config)

    reports, logs = recscan.check_unallowed(path_root, config[f"Structure"], config.get("dates_format", []), log=logs)
    reports, logs = recscan.check_unpresent(path_root, config[f"Structure"], reports, logs)
    txt, reports, logs = report.generate(path_root, path_conf, path_report, path_data, config, reports, logs)

    if display:
        print(txt)
    return txt, reports, logs

if __name__ == "__main__":
    args = parse(sys.argv)
    args = check_args(args)
    main(args["root"], args["conf"], args["report"], args["data"])
