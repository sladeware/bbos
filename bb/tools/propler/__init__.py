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

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Olexander Sviridenko'

import sys

from bb.tools.propler import gen_ld_script
from bb.tools.propler.image import *
from bb.tools.propler.disasm import *
from bb.tools.propler.terminal import *
from bb.tools.propler.uploader import *

def terminal_mode(port="/dev/ttyUSB0"):
  """Enter propler to terminal mode."""
  print "Enter to terminal mode"
  print "_" * 70
  print
  term = Terminal(port)
  term.start()
  print
  print "\r", "_" * 70
  print
  print "Exit from terminal mode"

def main(argv):
  from bb.tools.propler.config import Config
  cfg = Config(argv)
  return 0

if __name__ == "__main__":
  sys.exit(main(sys.argv))
