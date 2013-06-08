# -*- coding: utf-8; -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko <info@bionicbunny.org>

from bb.tools.b3.buildfile import Rule
from bb.tools.b3.rules.cc import CCBinary
from bb.tools.compilers import PropGCC
from bb.tools.loaders import propler
from bb.utils import path_utils
from bb.utils import typecheck

class PropellerBinary(CCBinary):

  def __init__(self, target=None, name=None, srcs=[], deps=[],
               compiler_class=None):
    if not compiler_class:
      compiler_class = PropGCC
    CCBinary.__init__(self, target=target, name=name, srcs=srcs, deps=deps,
                      compiler_class=compiler_class)

class PropellerLoad(Rule):

  def __init__(self, name=None, target=None, binary=None, deps=[], port=None,
               baudrate=None, eeprom=False, timeout=None, terminal_mode=False):
    Rule.__init__(self, name=name, target=target, deps=deps)
    self._binary = binary
    self._port = None
    self._baudrate = baudrate
    self._eeprom = eeprom
    self._timeout = timeout
    self._terminal_mode = terminal_mode
    if port:
      self.set_port(port)

  def set_port(self, port):
    if not typecheck.is_string(port):
      raise TypeError()
    self._port = port

  def get_port(self):
    return self._port

  def execute(self):
    print("Load propeller binary: %s" % self)
    self.resolve()
    if not self._binary or not path_utils.exists(self._binary):
      raise IOError()
    uploader = propler.SPIUploader(port=self.get_port(),
                                   baudrate=self._baudrate)
    if not uploader.connect():
      return
    uploader.upload_file(self._binary, eeprom=self._eeprom)
    if self._terminal_mode:
      propler.terminal_mode(port=self.get_port(), baudrate=self._baudrate)
    uploader.disconnect()
