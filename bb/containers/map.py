#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import collections

class DictWrapper(collections.MutableMapping):
  """This class simulates a dictionary. The instance's contents are kept in a
  regular dictionary, which is accessible via the :attr:`data` attribute of
  :class:DictWrapper` instances. If initialdata is provided, data is initialized
  with its contents; note that a reference to initialdata will not be kept,
  allowing it be used for other purposes.
  """

  # Start by filling-out the abstract methods
  def __init__(self, dict=None, **kwargs):
    self.data = {}
    if dict is not None:
      self.update(dict)
    if len(kwargs):
      self.update(kwargs)

  def __len__(self):
    return len(self.data)

  def __getitem__(self, key):
    if key in self.data:
      return self.data[key]
    if hasattr(self.__class__, "__missing__"):
      return self.__class__.__missing__(self, key)
    raise KeyError(key)

  def __setitem__(self, key, item):
    self.data[key] = item

  def __delitem__(self, key):
    del self.data[key]

  def __iter__(self):
    return iter(self.data)

  # Modify __contains__ to work correctly when __missing__ is present
  def __contains__(self, key):
    return key in self.data

  # Now, add the methods in dicts but not in MutableMapping
  def __repr__(self):
    return repr(self.data)

  def update(self, *args, **kwargs):
    return self.data.update(*args, **kwargs)

  def copy(self):
    if self.__class__ is UserDict:
      return UserDict(self.data.copy())
    import copy
    data = self.data
    try:
      self.data = {}
      c = copy.copy(self)
    finally:
      self.data = data
    c.update(self)
    return c

  @classmethod
  def fromkeys(cls, iterable, value=None):
    d = cls()
    for key in iterable:
      d[key] = value
    return d
