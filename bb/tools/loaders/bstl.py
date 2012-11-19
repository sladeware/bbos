#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module provides support for BSTL loader. BSTL is the command line loader
which can be found here http://www.fnarfbargle.com/bst.html

This little application simply allows to load pre-compiled ``.binary`` and
``.eeprom`` files into your propeller. It is a command line application that
takes optional parameters and a file name.

The following example shows how to upload ``helloworld.binary`` image to
propeller device via ``/dev/ttyUSB0`` serial port::

    from bb.tools.loaders import BSTLLoader
    loader = BSTLLoader(verbose=True,
                        mode=BSTLLoader.Modes.EEPROM_AND_RUN,
                        device_filename="/dev/ttyUSB0")
    loader.load("helloworld.binary")
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.utils.spawn import spawn
from bb.tools.loaders import Loader

class BSTLLoader(Loader):
  """This class represents BSTL loader and derived from
  :class:`bb.tools.loaders.loader.Loader` class.

  By default `device_filename` is ``None``, which forces BSTL to use
  ``/dev/ttyUSB0`` device. You can change device manually later by
  using :func:`BSTLLoader.set_device_filename`.
  """

  executables = {
    'loader' : ['bstl']
    }

  """Available program modes:

  ===================  =====
  Mode                 Value
  ===================  =====
  RAM_ONLY             1
  EEPROM_AND_SHUTDOWN  2
  EEPROM_AND_RUN       3
  ===================  =====
  """
  MODE_RAM_ONLY            = 1
  MODE_EEPROM_AND_SHUTDOWN = 2
  MODE_EEPROM_AND_RUN      = 3

  DEFAULT_MODE = MODE_RAM_ONLY
  """Represents default loader mode, which is
  :const:`BSTLLoader.Modes.RAM_ONLY`.
  """

  def __init__(self, verbose=False, device_filename=None, mode=None,
               high_speed=False):
    Loader.__init__(self, verbose)
    self._mode = mode or self.DEFAULT_MODE
    self._device_filename = device_filename
    # Setup high speed
    self._high_speed = None
    self.disable_high_speed()
    if high_speed:
      self.enable_high_speed()

  def set_mode(self, mode):
    """Set program mode. See :class:`BSTLLoader.Modes`."""
    self._mode = mode

  def get_mode(self):
    """Return current program mode."""
    return self._mode

  def set_device_filename(self, filename):
    """Set serial device to use."""
    self._device_filename = filename

  def get_device_filename(self):
    """Return device filename to use."""
    return self._device_filename

  def enable_high_speed(self):
    """Enable high speed."""
    self._high_speed = True

  def disable_high_speed(self):
    """Disable high speed."""
    self._high_speed = False

  def is_high_speed_enabled(self):
    """Whether high speed was enabled."""
    return self._high_speed

  def _load(self, filename, device_filename=None, program_mode=1):
    loader = self.executables['loader']
    flags = []
    if device_filename:
      self.set_device_filename(device_filename)
    # Add high speed flag
    if self.is_high_speed_enabled():
      flags.append('-f')
    # Add device flag
    if self.get_device_filename():
      flags.extend(['-d', self.get_device_filename()])
    # Add mode flag
    flags.extend(['-p', self.get_mode()])
    # Spawn!
    try:
      spawn(loader + flags + [filename], verbose=self.verbose)
    except BuilderExecutionError, msg:
      raise LoaderError, msg
