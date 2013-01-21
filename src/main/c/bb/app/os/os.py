#!/usr/bin/env python
#
# Copyright (c) 2012 Sladeware LLC
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

"""The Bionic Bunny Operating System is one or more microkernel for
microprocessors.
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import bb
from bb.app.object import Object
from bb.app.os.kernel import Kernel
from bb.app.os.drivers import Driver
from bb.hardware.devices.processors import Processor

class OS(Object):
  """This class is container/environment for Kernel's."""

  KERNEL_CLASS = Kernel

  def __init__(self, processor, max_message_size=0):
    Object.__init__(self)
    self._processor = None
    self._set_processor(processor)
    self._kernels = []
    self._messages = {}
    self._max_message_size = 0
    for core in processor.get_cores():
      # Skip the core if we do not have a threads for it
      kernel = core.get_kernel()
      if not kernel:
        continue
      self._kernels.append(kernel)
    self._extract_messages()
    self._set_max_message_size(max_message_size)

  def _set_processor(self, processor):
    """Set processor."""
    if not isinstance(processor, Processor):
      raise Exception('processor must be derived from Processor class.')
    self._processor = processor

  def _set_max_message_size(self, max_size=0):
    size = 0
    # Compute min message size
    for message in self.get_messages():
      if message.size > size:
        size = message.size
    if max_size > size:
      size = max_size
    self._max_message_size = size

  def _extract_messages(self):
    self._messages = {}
    for thread in self.get_threads():
      messages = thread.get_supported_messages()
      for message in messages:
        self._messages[message.label] = message

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

  def get_num_threads(self):
    """Returns number of threads within this operating system."""
    return len(self.get_threads())

  def get_threads(self):
    threads = []
    for kernel in self.get_kernels():
      threads.extend(kernel.get_threads())
    return threads

  def get_drivers(self):
    drivers = []
    for thread in self.get_threads():
      if isinstance(thread, Driver):
        drivers.append(thread)
    return drivers

  def get_max_message_size(self):
    return self._max_message_size

  def get_messages(self):
    return self._messages.values()

  def __str__(self):
    return '%s[processor=%s, num_kernels=%d]' % \
        (self.__class__.__name__,
         self._processor and self._processor.__class__.__name__ or None,
         self.get_num_kernels())
