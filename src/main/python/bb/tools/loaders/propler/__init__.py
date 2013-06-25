#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
__author__ = "Oleksandr Sviridenko"

import sys

from bb.tools.loaders.propler import gen_ld_script
from bb.tools.loaders.propler.image import *
from bb.tools.loaders.propler.disasm import *
from bb.tools.loaders.propler.terminal import *
from bb.tools.loaders.propler.uploader import *

def terminal_mode(port="/dev/ttyUSB0", baudrate=115200):
  """Enter propler to terminal mode."""
  print "Enter to terminal mode on '%s' with baudrate=%d" \
      % (port, baudrate)
  print "_" * 70
  print
  term = Terminal(port, baudrate=baudrate)
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
