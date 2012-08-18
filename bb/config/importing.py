#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import imp
import sys
import os
import logging
import inspect

import bb

logging.basicConfig(level=logging.DEBUG)

class BBImporter(object):
  """Read more about import hooks here
  <http://www.python.org/dev/peps/pep-0302/>,
  <http://docs.python.org/py3k/library/importlib.html>,
  <http://docs.python.org/library/imp.html>.
  """

  def __init__(self, *args, **kargs):
    self._mod = None

  def find_module(self, fullname, path=None):
    # Control only bb. modules
    #if fullname == 'bb' or fullname.startswith('bb.'):
    #  return self
    return None

  @classmethod
  def load_source(klass, fullname, file_path):
    logging.debug("Load '%s'", file_path)
    imp.load_source(fullname, file_path)

  @classmethod
  def get_filename(klass, fullname, path=None):
    fullname = fullname.split(".")
    filename = None
    files = []
    for search_path in sys.path:
      path = search_path
      parts = ""
      for part in fullname:
        parts = os.path.join(parts, part)
        path = os.path.join(search_path, parts)
        if os.path.exists(path) and os.path.isdir(path):
          files.append((search_path, os.path.join(parts, "__init__")))
          continue
        if os.path.exists(path + ".py"):
          files.append((search_path, parts))
          continue
        files = []
        break
      if files:
        break
    if files:
      return files.pop()
    return (None, None)

  def is_package(self, fullname):
    """Looks for an __init__ file name as returned by get_filename()."""
    search_path, mod_path = self.get_filename(fullname)
    filename = os.path.basename(mod_path)
    return filename == '__init__'

  def get_mod_path(self, fullname):
    search_path, mod_path = self.get_filename(fullname)
    if mod_path and mod_path.endswith('__init__'):
      mod_path = mod_path[:len(mod_path) - 9]
    return mod_path

  def include_autogen_module(self):
    frame = inspect.getouterframes(inspect.currentframe())[2][0]
    if not frame:
      raise Exception("Cannot find frame")
    master_mod = inspect.getmodule(frame)
    if not master_mod:
      raise Exception("Cannot define module by frame")
    for k, v in self._mod.__dict__.items():
      master_mod.__dict__[k] = v
    for k, v in master_mod.__dict__.items():
      try:
        self._mod.__dict__[k] = v
      except TypeError, e:
        pass

  def load_module(self, fullname):
    if fullname in sys.modules:
      return sys.modules[fullname]
    self._mod = None
    mod_path = self.get_mod_path(fullname)
    if not mod_path:
      return None
    fh, path, descr = imp.find_module(mod_path)
    sys.modules.setdefault(fullname, imp.new_module(fullname))
    self._mod = imp.load_module(fullname, fh, path, descr)
    self._mod.__loader__ = self
    self._mod.__file__ = "<%s>" % self.__class__.__name__
    if self.is_package(fullname):
      self._mod.__path__ = ""
      self._mod.__package__ = fullname
    else:
      self._mod.__package__ = fullname.rpartition('.')[0]
    if fullname.endswith('_autogen'):
      self.include_autogen_module()
    return self._mod

#sys.meta_path = [BBImporter()]
