import os
import sys
from . import structcheck
import pkg_resources


if __name__ == "__main__":
    version = pkg_resources.get_distribution('structcheck').version
    directory = os.getcwd()

    print(f"structckeck version = {version}")
    print(f"Scanning directory = {directory}")

    args = sys.argv
    if len(args) > 1:
        args = args[1:]
    else:
        args = ["-p", directory]

    raise SystemExit(
        structcheck.scan(args)
    )
