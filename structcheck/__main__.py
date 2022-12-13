import sys
from . import structcheck


if __name__ == "__main__":
	raise SystemExit(structcheck.scan(sys.argv))
