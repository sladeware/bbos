#!/usr/bin/env python

import types

from bb.utils import typecheck
from bb.utils import spawn

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

class ExecutableOptions(dict):
  def __init__(self, *args, **kwargs):
    dict.__init__(self)
    self.update(*args, **kwargs)

  def update(self, *args, **kwargs):
    if args:
      for arg in args:
        if not isinstance(arg, dict):
          print type(arg), arg
          raise TypeError("argument must be a dict object: %s" % arg)
        self.update(**arg)
    if kwargs:
      for key, value in kwargs.items():
        self[key] = value

  def __setitem__(self, key, value):
    if key in self:
      if not type(value) is type(self[key]):
        raise TypeError("Value of '%s' has to be of type %s not %s" % \
                          (key, type(self[key]).__name__, type(value).__name__))
    dict.__setitem__(self, key, value)

class OptionsReaderInterface(object):

  OPTION_HANDLERS = {}

  def read_options(self, options):
    if self.OPTION_HANDLERS:
      for option, handler_name in self.OPTION_HANDLERS.items():
        if not option in options:
          continue
        value = options[option]
        handler = getattr(self, handler_name)
        handler(value)

class ExecutableWrapper(object):
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
    return self._executable

  def check_executable(self):
    """Check executable. All of them has to exist. Print warning if some
    executable was specified but not defined.
    """
    if not self._executable or not spawn.which(self._executable):
      return False
    return True
