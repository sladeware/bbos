#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

from bb.hardware.devices import Device
from bb.lib.utils import typecheck

class Board(Device):
  """Base class representing a board -- i.e. computing hardware.

  A board contains one or more processors. Each processor may or may not be the
  same, depending on the board. A board is a piece of hardware that performs
  computation within its processors. Other supporting hardware may be present on
  the board, but BB does not explicitly refer to them.
  """

  def __init__(self, processors=[]):
    Device.__init__(self)
    self._processors = []
    if processors:
      self.add_processors(processors)

  def add_processors(self, processors):
    if not typecheck.is_sequence(processors):
      raise TypeError('Must be a sequence')
    for processor in processors:
      self.add_processor(processor)

  def add_processor(self, processor):
    # Add a new element to the device/board and start tracking it as a processor
    self.add_element(processor)
    self._processors.append(processor)

  def get_processors(self):
    return self._processors

class Breadboard(Board):
  """A breadboard (protoboard) is a construction base for prototyping of
  electronics.

  Because the solderless breadboard does not require soldering, it is
  reusable. This makes it easy to use for creating temporary prototypes and
  experimenting with circuit design.
  """

  DESIGNATOR_FORMAT="PROTOBOARD_%d"

  def __init__(self):
    Device.__init__(self)

# Make Protoboard to be an alias of Breadboard
Protoboard = Breadboard
