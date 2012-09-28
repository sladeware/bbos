#!/usr/bin/env python
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

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import bb
from bb.utils import typecheck

class MetaObject(type):
  """Meta-class for all application objects. You have to use this class as
  meta-class for you classes in order to build or load your object on the late
  stages.
  """

  def __new__(mcs, name, bases, dictionary):
    dictionary['TARGET_CLASS'] = None # bb.buildtime.object_factory(name)
    return type.__new__(mcs, name, bases, dictionary)

  def __enter__(klass):
    if bb.is_build_time_stage():
      print '>>>>'
      if not klass.TARGET_CLASS:
        klass.TARGET_CLASS = MetaObject.TARGET_CLASS
      return klass.TARGET_CLASS
    else:
      raise Exception()

  def __exit__(klass, type, value, traceback):
    pass

class Object(object):
  """The main object class."""

  __metaclass__ = MetaObject

  def __init__(self):
    self._target = None # self.TARGET_CLASS()

  def __enter__(self):
    if not self._target:
      print '<<<<', self.TARGET_CLASS
      self._target = Object.TARGET_CLASS(self)
    if bb.is_build_time_stage():
      return self._target
    elif bb.is_load_time_stage():
      if not self._target.binary:
        raise Exception('No binary associated with this object')
      return self._target.binary
    else:
      raise Exception()

  def __exit__(self, type, value, traceback):
    pass
