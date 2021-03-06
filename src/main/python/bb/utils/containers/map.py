# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC
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
#
# Author: Oleksandr Sviridenko

import collections

__all__ = ["dotdict", "DictWrapper"]

class dotdict(dict):
  """Provides dot notation over bracket notation for dictionary access. Returns
  None instead of raising an exception if key is undefied.
  """

  def __getattr__(self, attr):
    return self.get(attr, None)

  __setattr__= dict.__setitem__
  __delattr__= dict.__delitem__

class DictWrapper(collections.MutableMapping):
  """This class simulates a dictionary. The instance's contents are kept in a
  regular dictionary, which is accessible via the :attr:`data` attribute of
  :class:`DictWrapper` instances. If initialdata is provided, data is
  initialized with its contents; note that a reference to initialdata will not
  be kept, allowing it be used for other purposes.
  """

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

  def merge(self, d):
    """Merges two dictionaries. For example:

      >>> d = DictWrapper({1:[2, 3], 2:[3]})
      >>> d.merge({1:[4], 3:[1]})
      {1:[2, 3, 4], 2:[3], 3:[1]}
    """
    self.update((k, self.data[k] + tuple(d[k]))
                for k in set(self.data).intersection(d))

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
