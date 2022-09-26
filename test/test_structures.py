import os
import sys
import unittest

current_dir = os.path.dirname(__file__)
source_dir = os.path.join(current_dir, "..", "source")
sys.path.insert(0, source_dir)

import structcheck

class TestStructures(unittest.TestCase):
    def test_succes_python(self):
        path_data_succes = os.path.join(current_dir, "data_succes")
        for folder in os.listdir(path_data_succes):
            path_folder = os.path.join(path_data_succes, folder)
            args = structcheck.check_args({
                "root": path_folder
            })
            _, reports, logs = structcheck.main(
                args["root"], args["conf"], args["report"], args["data"],
                display=False
            )
            self.assertEqual(len(reports), 0)

    

if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:
        pass
