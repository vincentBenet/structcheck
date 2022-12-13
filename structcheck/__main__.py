import os
from . import structcheck
import pkg_resources


if __name__ == "__main__":

    print(f"structckeck version = {pkg_resources.get_distribution('structcheck').version}")

    raise SystemExit(
        structcheck.scan(
            ["-p", os.getcwd()]
        )
    )
