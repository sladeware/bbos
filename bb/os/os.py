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

"""The Bionic Bunny Operating System is one or more microkernel for
microprocessors.
"""

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import bb
from bb.os.kernel import Kernel
from bb.hardware.devices.processors import Processor

class OS(bb.Object):
  """This class is container/environment for Kernel's."""

  def __init__(self, processor):
    bb.Object.__init__(self)
    if not isinstance(processor, Processor):
      raise Exception('processor must be derived from Processor class.')
    self._processor = processor
    self._kernels = []
    for core in processor.get_cores():
      # Skip the core if we do not have a threads for it
      kernel = core.get_kernel()
      if not kernel:
        continue
      self._kernels.append(kernel)

  @property
  def processor(self):
    """This property returns Processor instance. See get_processor()."""
    return self.get_processor()

  def get_processor(self):
    """Return Processor instance on which OS will be running."""
    return self._processor

  @property
  def kernels(self):
    return self.get_kernels()

  def get_num_kernels(self):
    return len(self.get_kernels())

  def get_kernels(self):
    return self._kernels

  def get_kernel(self, i=0):
    return self._kernels[i]

  def __str__(self):
    return "OS on processor '%s', with %d kernel(s)" \
        % (self.get_processor(), self.get_num_kernels())
