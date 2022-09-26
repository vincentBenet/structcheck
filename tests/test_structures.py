import os
import sys
import json
import inspect
import unittest

current_dir = os.path.dirname(__file__)
source_dir = os.path.join(current_dir, "..", "structcheck")
sys.path.insert(0, source_dir)

import structcheck

class TestStructures(unittest.TestCase):
    def test_succes(self):
        path_data_succes = os.path.join(current_dir, "data_succes")
        for folder in os.listdir(path_data_succes):
            path_folder = os.path.join(path_data_succes, folder)
            print(f"\n{'_' * 115}\n{'_' * 115}\n{inspect.stack()[0][3]}: {folder} - < {path_folder} >\n{'_' * 115}\n{'_' * 115}")
            args = structcheck.check_args({
                "root": path_folder
            })
            txt, reports, logs = structcheck.main(
                args["root"], args["conf"], args["report"], args["data"],
                display=False
            )
            
            print(txt)
            
            self.assertEqual(len(reports), 0)  # Check no error
            
            # Check files are generated
            self.assertEqual(os.path.isfile(os.path.join(path_folder, "structcheck.txt")), True)
            self.assertEqual(os.path.isfile(os.path.join(path_folder, ".structcheck.json")), True)

    def test_fail(self):
        path_data_succes = os.path.join(current_dir, "data_fail")
        for folder in os.listdir(path_data_succes):
            path_folder = os.path.join(path_data_succes, folder)
            print(f"\n{'_' * 115}\n{'_' * 115}\n{inspect.stack()[0][3]}: {folder} - < {path_folder} >\n{'_' * 115}\n{'_' * 115}")
            args = structcheck.check_args({
                "root": path_folder
            })
            txt, reports, logs = structcheck.main(
                args["root"], args["conf"], args["report"], args["data"],
                display=False
            )
            
            print(txt)
            
            self.assertEqual(len(reports), 1)  # Check exactly one error
            
            # Check files are generated
            self.assertEqual(os.path.isfile(os.path.join(path_folder, "structcheck.txt")), True)
            self.assertEqual(os.path.isfile(os.path.join(path_folder, ".structdata.json")), True)
            
            # Check error type
            if len(reports) == 1:
                error_path, error_type, error_args = reports[0]
                self.assertEqual(error_type, "Date file different")
            

if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:
        pass
