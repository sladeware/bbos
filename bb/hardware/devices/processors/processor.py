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

from bb.hardware import primitives
from bb.hardware.devices import Device
from bb.lib.utils import typecheck

class Processor(Device):
  DESIGNATOR_FORMAT = "PROCESSOR%d"

  class Core(primitives.ElectronicPrimitive):
    DESIGNATOR_FORMAT = "CORE%d"

    def __init__(self, processor, id_=None):
      primitives.ElectronicPrimitive.__init__(self)
      self._processor = None
      self._set_processor(processor)
      self._kernel = None
      if not id_ is None:
        self.set_id(id_)

    def set_kernel(self, kernel):
      self._kernel = kernel

    def get_kernel(self):
      return self._kernel

    def get_processor(self):
      return self._processor

    def _set_processor(self, processor):
      if not isinstance(processor, Processor):
        raise Exception("Requires Processor class")
      self._processor = processor

  def __init__(self, num_cores=0, cores=None):
    self._os = None
    Device.__init__(self)
    if num_cores < 1:
      raise Exception("Number of cores must be greater than zero.")
    self._cores = [None] * num_cores
    if cores:
      self.set_cores(cores)

  def get_os(self):
    return self._os

  def set_os(self, os):
    self._os = os

  def set_cores(self, cores):
    if typecheck.is_sequence(cores) and len(cores):
      for i in range(len(cores)):
        self.set_core(cores[i], i)
    elif typecheck.is_dict(cores) and len(cores):
      for id, core in cores.items():
        self.set_core(core, id)
    else:
      raise Exception("Cores is not a sequnce or dictionary.")

  def set_core(self, core, id):
    self.verify_core(core)
    self.validate_core(core)
    self.validate_core_id(id)
    self._cores[id] = core
    core.set_id(id)

  def get_core(self, id_):
    self.validate_core_id(id_)
    return self._cores[id_]

  def verify_core(self, core):
    if not isinstance(core, Processor.Core):
      raise TypeError('core "%s" must be bb.os.Core sub-class' % core)
    return core

  def validate_core(self, core):
    if not self.is_valid_core(core):
      raise NotImplementedError()

  def is_valid_core(self, core):
    return self.verify_core(core) #is_core(core)

  def validate_core_id(self, id_):
    if id_ >= 0 and self.get_num_cores() <= id_:
      raise Exception('The %s supports up to %d cores. You have too many: %d' %
                      (self.__class__.__name__, self.get_num_cores(), id_))

  def get_cores(self):
    return self._cores

  def get_num_cores(self):
    return len(self._cores)

  def __str__(self):
    return  "%s with %d core(s)" % (Device.__str__(self), self.get_num_cores())
