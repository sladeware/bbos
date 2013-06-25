# -*- coding: utf-8; -*-
#
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

"""The Bionic Bunny Operating System is one or more microkernel for
microprocessors.
"""

from __future__ import print_function

import json

from bb.app.os.kernel import Kernel
from bb.app.os.drivers import Driver
from bb.app.os.thread import Thread
from bb.app.os.port import Port
from bb.app.hardware.devices.processors import Processor
from bb.utils import typecheck

class OS(object):
  """This class is container/environment for :class:`Kernel`'s.

  :param processor: A :class:`Processor` instance on which OS runs.
  :param max_message_size: An integer that represents max message size in bytes
    available messaging. Note, this value will be generated automatically.
  """

  kernel_class = Kernel

  def __init__(self, processor=None, max_message_size=0, ports=[]):
    if not processor and not getattr(self.__class__, "kernel_class", None):
      raise Exception()
    self._processor = None
    self._set_processor(processor or getattr(self.__class__, "kernel_class"))
    self._kernels = []
    self._ports = {}
    self._messages = {}
    self._max_message_size = 0
    for core in processor.get_cores():
      kernel = core.get_kernel()
      if not kernel:
        continue
      self._kernels.append(kernel)
    if max_message_size:
      self.set_max_message_size(max_message_size)
    if ports:
      self.add_ports(ports)
    self.update()

  def __str__(self):
    return '%s[processor=%s, num_kernels=%d]' % \
        (self.__class__.__name__,
         self._processor and self._processor.__class__.__name__ or None,
         self.get_num_kernels())

  def __build__(self):
    """Helps b3 to build this OS instance. Returns required dependencies."""
    return [self.get_processor()] + self.get_kernels()

  def _set_processor(self, processor):
    if not isinstance(processor, Processor):
      raise Exception('processor must be derived from Processor class.')
    self._processor = processor

  def update(self):
    """Does lazy update: extracts messages, updates max message size, generates
    thread and port ids. This method is called when the mapping has been
    updated.
    """
    self._messages = {}
    for uid, thread in enumerate(self.get_threads()):
      thread._set_uid(uid)
      if thread.has_port():
        thread.get_port()._set_uid(uid)
      messages = thread.get_supported_messages()
      for message in messages:
        self._messages[message.get_label()] = message
    for uid, port in enumerate(self.get_extra_ports()):
      port._set_uid(uid + len(self.get_standard_ports()))
    if not self.get_max_message_size():
      self._max_message_size = self.get_min_message_size()

  def get_standard_ports(self):
    """Returns a list of standard ports."""
    return [thread.get_port() for thread in self.get_threads() if thread.has_port()]

  def get_extra_ports(self):
    """Returns a list of extra ports."""
    return set(self.get_ports()) - set(self.get_standard_ports())

  def serialize(self):
    """Serialize this OS instance in JSON format."""
    return json.dumps({
        'processor': json.loads(self.get_processor().serialize()),
        'max_message_size': self.get_max_message_size(),
        'messages': [json.loads(msg.serialize()) for msg in self.get_messages()],
        'kernels': [json.loads(k.serialize()) for k in self.get_kernels()],
        'ports': [{'name': p.get_name(), 'uid': p.get_uid(), 'capacity': p.get_capacity()}
                  for p in self.get_ports()],
      })

  @property
  def processor(self):
    """This property returns Processor instance. See get_processor()."""
    return self.get_processor()

  def get_processor(self):
    """Returns processor on which OS will be running.

    :returns: A :class:`Processor` instance.
    """
    return self._processor

  @property
  def kernels(self):
    return self.get_kernels()

  def get_num_kernels(self):
    """Returns number of kernels."""
    return len(self.get_kernels())

  def get_kernels(self):
    """Returns kernels within this OS.

    :returns: A list of :class:`Kernel` instances.
    """
    return self._kernels

  def get_kernel(self, i=0):
    return self._kernels[i]

  def get_num_threads(self):
    """Returns number of threads within this operating system."""
    return len(self.get_threads())

  def get_threads(self):
    """Returns threads from all the kernels.

    :returns: A list of :class:`bb.app.os.thread.Thread` instances.
    """
    threads = []
    for kernel in self.get_kernels():
      threads.extend(kernel.get_threads())
    return threads

  def get_drivers(self):
    """Returns drivers from all the kernels.

    :returns: A list of :class:`Driver` instances.
    """
    drivers = []
    for thread in self.get_threads():
      if isinstance(thread, Driver):
        drivers.append(thread)
    return drivers

  def get_min_message_size(self):
    """Computes min required message size.

    :returns: A size of message in bytes.
    """
    sz = 0
    for msg in self.get_messages():
      if msg.get_byte_size() > sz:
        sz = msg.get_byte_size()
    return sz

  def set_max_message_size(self, size=0):
    """Manually set max message size. It cannot be less than min message size,
    see :func:`get_min_message_size`.

    :param size: A message size in bytes.
    """
    if size > self.get_min_message_size():
      self._max_message_size = size

  def get_max_message_size(self):
    """Returns max message size."""
    return self._max_message_size

  def get_messages(self):
    """Returns all messages that can be pass over this OS.

    :returns: A list of :class:`Message` instances.
    """
    return self._messages.values()

  def get_num_messages(self):
    """Returns number of messages supported by threads within this
    meta-operating system.
    """
    return len(self.get_messages())

  def add_ports(self, ports):
    """Adds ports to the system.

    :param ports: A list of Port instances.
    """
    if not typecheck.is_sequence(ports):
      raise TypeError("ports must be a sequence.")
    for port in ports:
      self.add_port(port)

  def add_port(self, port):
    """Adds port to the system."""
    if not isinstance(port, Port):
      raise TypeError()
    if port.get_name() in self._ports:
      raise Exception("Port '%s' was already registered." % port.get_name())
    self._ports[port.get_name()] = port
    return self

  def get_ports(self):
    """Returns a list of ports."""
    return self._ports.values()

  def get_num_ports(self):
    """Returns number of available ports."""
    return len(self.get_ports())
