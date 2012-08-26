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

"""Application build-file."""

import sys

import bb

class MultiKernelOS(object):
  """This image class supports multiple OS'es inside of result binary."""

  def __init__(self, mapping, processor, thread_distribution):
    bb.builder.Image.__init__(self)
    self._mapping = mapping
    os_class = mapping.get_os_class()
    print ' ', str(processor)
    os = os_class(processor=processor,
                  thread_distribution=thread_distribution[processor])
    self.add_target(os)
    self.add_target(processor)
    self.add_targets(mapping.get_drivers())
    for kernel in os.kernels:
      self.add_targets([kernel, kernel.get_scheduler()])
      self.add_targets(kernel.get_threads())

  def get_name(self):
    return '%s' % (self._mapping.get_name(),)
