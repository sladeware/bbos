#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import inspect
import types

from bb.containers import DictWrapper
from bb.utils import typecheck
from bb.utils import spawn

class ExecutableOptions(DictWrapper):

  def __init__(self, *args, **kwargs):
    DictWrapper.__init__(self, *args, **kwargs)
    caller_frame = inspect.getouterframes(inspect.currentframe(), 2)
    self.__file__ = inspect.getsourcefile(caller_frame[1][0])

class OptionsReaderInterface(object):

  OPTION_HANDLERS = {}

  def __init__(self):
    self.__processing_options = None

  def get_processing_options(self):
    return self.__processing_options

  def read_options(self, options):
    self.__processing_options = options
    if self.OPTION_HANDLERS:
      for option, handler_name in self.OPTION_HANDLERS.items():
        if not option in options:
          continue
        value = options[option]
        handler = getattr(self, handler_name)
        handler(value)
    self.__processing_options = None

class ExecutableWrapper(object):
  """This class is wrapper for an executable."""

  EXECUTABLE = []

  def __init__(self, executable=[]):
    if issubclass(self.__class__, OptionsReaderInterface):
      OptionsReaderInterface.__init__(self)
    self._executable = []
    if executable:
      self.set_executable(executable)
    elif hasattr(self, "EXECUTABLE"):
      self.set_executable(self.EXECUTABLE)

  def set_executable(self, executable):
    if not typecheck.is_list(executable):
      raise TypeError("Has to be list.")
    self._executable = executable

  def get_executable(self):
    """Returns handled executable."""
    return self._executable

  def check_executable(self):
    """Checks executable. All of them has to exist. Print warning if some
    executable was specified but not defined.
    """
    if not self._executable or not spawn.which(self._executable):
      return False
    return True
