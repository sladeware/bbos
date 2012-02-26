#!/usr/bin/env python

from bb.tools.propler.core import *

def main(argv):
    from bb.tools.propler.config import Config
    cfg = Config(argv)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
