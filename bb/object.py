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
from bb.lib.utils import typecheck

class _BuildCase(object):
  def __init__(self, owner, toolchain, params):
    self.owner = owner
    self.toolchain = toolchain
    self.params = params

  def __getitem__(self, key):
    return self.params[key]

class _BuildCases(list):
  """Container of build-cases."""

  def __iadd__(self, build_cases):
    # Overload += operator
    self._update(caller(2), build_cases)

  def _update(self, owner, build_cases):
    if not build_cases:
      return
    for case in build_cases:
      if typecheck.is_string(case):
        build_case = _BuildCase(owner, case, build_cases[case])
        self.append(build_case)
      else:
        self.append(case)

  def __getitem__(self, key):
    for build_case in self:
      if build_case.toolchain == key:
        return build_case
    return None

  def get_supported_toolchains(self):
    toolchains = []
    for build_case in self:
      toolchains.append(build_case.toolchain)
    return toolchains

  def update(self, build_cases):
    self._update(caller(2), build_cases)

class MetaBundle(type):
  def __new__(mcs, name, bases, dictionary):
    dictionary['BUILD_CASES'] = _BuildCases()
    return type.__new__(mcs, name, bases, dictionary)

  @property
  def build_cases(klass):
    return klass.__dict__['BUILD_CASES']

  @build_cases.setter
  def build_cases(klass, build_cases):
    klass.__dict__['BUILD_CASES'] += build_cases

class Bundle(object):
  __metaclass__ = MetaBundle
  decomposer = None

  def __init__(self, build_cases=None):
    self._build_cases = _BuildCases()
    self._build_cases.update(build_cases)

  @property
  def build_cases(self):
    return self._build_cases

  @build_cases.setter
  def build_cases(self, build_cases):
    if not build_cases:
      return
    self._build_cases += build_cases

def bundle_factory(object_class_name):
  def __init__(self):
    Bundle.__init__(self, self.BUILD_CASES)
  klass = type("%sBundle" % object_class_name, (Bundle,), {'__init__':__init__,})
  return klass

class _MetaObject(type):
  """Meta-class for all application objects. You have to use this class as
  meta-class for you classes in order to build or load your object on the late
  stages.
  """

  def __new__(mcs, name, bases, dictionary):
    dictionary['BUNDLE_CLASS'] = bundle_factory(name)
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
    else:
      raise Exception()

  def __exit__(self, type, value, traceback):
    pass
