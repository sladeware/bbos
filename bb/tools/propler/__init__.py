#!/usr/bin/env python

"""Propler.

Example::

    from bb.tools import propler

    uploader = propler.SPIUploader(port="/dev/ttyUSB0")
    uploader.connect()
    uploader.upload_file("helloworld.binary")
    uploader.disconnect()

Output::

    Connected to propeller v1 on '/dev/ttyUSB1'
    Downloading [##################################################] 100.0%
    Verifying... OK
    Disconnected

"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.tools.propler.core import *

def main(argv):
    from bb.tools.propler.config import Config
    cfg = Config(argv)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
