# Copyright (c) 2012-2013 Sladeware LLC
# http://www.bionicbunny.org/
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

import inspect

from bb.utils import typecheck

def get_class_fullname(cls):
  return ".".join([inspect.getmodule(cls).__name__, cls.__name__])

def get_all_subclasses(cls):
  """Returns all subclasses."""
  if not typecheck.is_class(cls):
    return [cls.__class__] + get_all_subclasses(cls.__class__)
  return list(cls.__bases__) + [g for s in cls.__bases__
                                for g in get_all_subclasses(s)]

class Cloneable:
  """This (empty) interface must be implemented by all classes that wish to
  support cloning. The implementation of clone() in :class:`Object` checks if
  the object being cloned implements this interface and throws
  :class:`NotImplementedError` if it does not.
  """

  def clone(self):
    """Creates and returns a copy of the object."""
    raise NotImplementedError()

class Object(object):
  """The main object class for objects in BB."""

  Cloneable = Cloneable
