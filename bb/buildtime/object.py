#!/usr/bin/env python

from bb.utils import typecheck

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

class MetaObject(type):
  def __new__(mcs, name, bases, dictionary):
    dictionary['BUILD_CASES'] = _BuildCases()
    return type.__new__(mcs, name, bases, dictionary)

  @property
  def build_cases(klass):
    return klass.__dict__['BUILD_CASES']

  @build_cases.setter
  def build_cases(klass, build_cases):
    klass.__dict__['BUILD_CASES'] += build_cases

class Object(object):
  __metaclass__ = MetaObject
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

def object_factory(object_class_name):
  def __init__(self):
    Object.__init__(self, self.BUILD_CASES)
  klass = type("%sBundle" % object_class_name, (Object,), {'__init__':__init__,})
  return klass
