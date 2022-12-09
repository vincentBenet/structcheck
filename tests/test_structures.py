"""
Testing single script for the project
"""

import os
import sys
import inspect
import unittest

current_dir = os.path.dirname(__file__)
source_dir = os.path.join(current_dir, "..")


class TestStructures(unittest.TestCase):
    """
    Testing object from unittest lib
    """
    def setUp(self):
        sys.path.insert(0, source_dir)
        global structcheck
        import structcheck
    
    def test_succes(self):
        """
        Test all structures stored inside the 'data_succes' folder.
        No errors has to be raised!

        :return:
        """
        path_data_succes = os.path.join(current_dir, "data_succes")
        for folder in os.listdir(path_data_succes):
            path_folder = os.path.join(path_data_succes, folder)
            print(f"""\n{'_' * 115}\n{'_' * 115}\n{
                inspect.stack()[0][3]
            }: {folder} - < {path_folder} >\n{'_' * 115}\n{'_' * 115}""")
            args = structcheck.check_args({
                "root": path_folder
            })
            _, reports, _ = structcheck.main(
                args["root"], args["conf"], args["report"], args["data"]
            )

            self.assertEqual(len(reports), 0)  # Check no error

            # Check files are generated
            self.assertEqual(os.path.isfile(os.path.join(path_folder, "structcheck.txt")), True)
            self.assertEqual(os.path.isfile(os.path.join(path_folder, ".structcheck.json")), True)

    def test_fail(self):
        path_data_succes = os.path.join(current_dir, "data_fail")
        for folder in os.listdir(path_data_succes):
            path_folder = os.path.join(path_data_succes, folder)
            print(f"""\n{'_' * 115}\n{'_' * 115}\n{
                inspect.stack()[0][3]}: {folder} - < {path_folder} >\n{'_' * 115}\n{'_' * 115}""")
            args = structcheck.check_args({
                "root": path_folder
            })
            _, reports, _ = structcheck.main(
                args["root"], args["conf"], args["report"], args["data"]
            )

            self.assertEqual(len(reports), 1)  # Check exactly one error

            # Check files are generated
            self.assertEqual(os.path.isfile(os.path.join(path_folder, "structcheck.txt")), True)
            self.assertEqual(os.path.isfile(os.path.join(path_folder, ".structdata.json")), True)

            # Check error type
            if len(reports) == 1:
                _, error_type, _ = reports[0]
                self.assertEqual(error_type, "Date file different")


if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:
        pass
