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

class _MetaObject(type):
  """Meta-class for all application objects. You have to use this class as
  meta-class for you classes in order to build or load your object on the late
  stages.
  """

  def __new__(mcs, name, bases, dictionary):
    dictionary['BUNDLE_CLASS'] = bb.buildtime.object_factory(name)
    return type.__new__(mcs, name, bases, dictionary)

  def __enter__(klass):
    if bb.is_build_time_stage():
      return klass.BUNDLE_CLASS
    else:
      raise Exception()

  def __exit__(klass, type, value, traceback):
    pass

class Object(object):

  __metaclass__ = _MetaObject

  def __init__(self):
    self._bundle = self.BUNDLE_CLASS()

  def __enter__(self):
    if bb.is_build_time_stage():
      return self._bundle
    elif bb.is_load_time_stage():
      if not self._bundle.binary:
        raise Exception('No binary associated with this object')
      return self._bundle.binary
    else:
      raise Exception()

  def __exit__(self, type, value, traceback):
    pass
