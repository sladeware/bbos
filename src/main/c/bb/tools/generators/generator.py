#!/usr/bin/env python

import inspect
import datetime

from bb import host_os

class Generator(object):

  def __init__(self, filename=None, mode="w"):
    self._fname = None
    self._fh = None
    if filename:
      self.open(filename, mode)

  def open(self, filename, mode="a"):
    """If file is not exist, it will be created. See create()."""
    self._fname = filename
    self._fh = open(filename, mode)
    if mode == "w":
      self.header("TIMESTAMP: %s" % datetime.datetime.now())
    elif mode == "a":
      caller_frame = inspect.getouterframes(inspect.currentframe(), 2)
      stamp = "FILE: %s\n" % inspect.getsourcefile(caller_frame[2][0]) \
          + "FUNC: %s\n" % caller_frame[2][3] \
          + "TIME: %s" % datetime.datetime.now()
      self.header(stamp, 2)
    return self

  def create(self, filename):
    self._fh = open(filename, "w")
    return self

  def header(self, data, level=1):
    raise NotImplementedError()

  def write(self, data):
    self._fh.write(data)

  def writeln(self, data=""):
    self._fh.write(data + "\n")

  def edit(self, filename):
    self.open(filename)
    return self

  def close(self):
    self._fh.close()
