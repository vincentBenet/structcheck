import os
from . import structcheck
import pkg_resources


if __name__ == "__main__":
    version = pkg_resources.get_distribution('structcheck').version
    directory = os.getcwd()

    print(f"structckeck version = {version}")
    print(f"Scanning directory = {directory}")

    raise SystemExit(
        structcheck.scan(
            ["-p", directory]
        )
    )
