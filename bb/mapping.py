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

"""The mapping of hardware resources to software runtime components such as
processes, threads, queues and pools is determined at compile time. Thereby
permitting system integrators to cleanly separate the concept of what the
software does and where it does it.

Compile time mapping is critical for tuning a system based on application
requirements. It is useful when faced with an existing software application
that must run on a new or updated hardware platform, thus requiring
re-tuning of the application. Equally important is the flexibility afforded
by compile time mapping to system integrators that need to incorporate new
software features as applications inevitably grow in complexity.
"""

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import bb
from bb.hardware.devices.processors import Processor
from bb.lib.utils import typecheck

def roundrobin_thread_distributor(threads, processor):
  """Default thread distributor provides round-robin distribution of threads
  between all cores within the processors.
  """
  thread_distribution = {}
  for core in processor.get_cores():
    thread_distribution[core] = []
  c = 0
  for thread in threads:
    if not isinstance(thread, bb.os.Thread):
      raise TypeError("thread must be derived from bb.os.Thread")
    core = processor.get_cores()[c]
    c = (c + 1) % len(processor.get_cores())
    thread_distribution[core].append(thread)
  return thread_distribution

class Mapping(object):
  OS_CLASS = bb.os.OS

  def __init__(self, name, processor=None, os_class=None,
               thread_distributor=roundrobin_thread_distributor):
    self._name = None
    self._threads = dict()
    self._os_class = None
    self._max_message_size = 0
    self._is_simulation_mode = False
    self._processor = None
    self._thread_distributor = None
    if thread_distributor:
      self.set_thread_distributor(thread_distributor)
    # NOTE: for now we will force user to provide a name.
    self.set_name(name)
    if os_class:
      self.set_os_class(os_class)
    else:
      self.set_os_class(self.OS_CLASS)
    if processor:
      self.set_processor(processor)
    # Once a new mapping was created, it will automatically register itself
    # within existed application. See issue #16.
    bb.application.register_mapping(self)

  def set_name(self, name):
    if not typecheck.is_string(name):
      raise Exception("name must be string")
    self._name = name

  def get_name(self):
    return self._name

  def get_messages(self):
    all_messages = {}
    for thread in self.get_threads():
      messages = thread.get_supported_messages()
      for message in messages:
        all_messages[message.id] = message
    return all_messages.values()

  def set_thread_distributor(self, f):
    self._thread_distributor = f

  def get_thread_distributor(self):
    return self._thread_distributor

  def register_thread(self, thread):
    """Register thread by its name. The name has to be unique within this
    mapping. If thread doesn't have a name, mapping will try to use its name
    format (see Thread.get_name_format()) to generate one.
    """
    if not isinstance(thread, bb.os.Thread):
      raise Exception("Must be derived from bb.os.Thread: %s", thread)
    if thread.get_name() is None:
      frmt = thread.get_name_format()
      if not frmt:
        logging.warning("Thread %s doesn't have a name and the format cannot be"
                        "obtained to generate one." % thread)
        return
      # TODO(team): improve name generation within a mapping
      thread.set_name(frmt % self.get_num_threads())
    self._threads[ thread.get_name() ] = thread

  def get_thread(self, name):
    if not typecheck.is_string(name):
      raise TypeError('name must be a string')
    return self._threads.get(name, None)

  def register_threads(self, threads):
    for thread in threads:
      self.register_thread(thread)

  def get_num_threads(self):
    return len(self.get_threads())

  def get_threads(self):
    """Return list of threads handled by this mapping."""
    return self._threads.values()

  def get_min_message_size(self):
    size = 0
    for message in self.get_messages():
      for field in message.fields:
        size += field.size
    return size

  def set_max_message_size(self, n_bytes):
    self._max_message_size = n_bytes

  def get_max_message_size(self):
    return self._max_message_size

  def set_simulation_mode(self):
    self._is_simulation_mode = True

  def is_simulation_mode(self):
    return self._is_simulation_mode

  def get_processor(self):
    """Return :class:`bb.hardware.devices.processors.processor.Processor`
    instance.
    """
    return self._processor

  def set_processor(self, processor):
    if not isinstance(processor, Processor):
      raise TypeError("'processor' has to be derived from Processor class.")
    self._processor = processor

  def is_processor_defined(self):
    """Whether or not a processor was defined. Return ``True`` value if the
    :class:`bb.hardware.devices.processors.processor.Processor` instance was
    defined, or ``False`` otherwise.
    """
    return not not self.get_processor()

  def set_os_class(self, os_class):
    if not issubclass(os_class, bb.os.OS):
      raise TypeError("Must be derived from bb.os.OS class: %s" % os_class)
    self._os_class = os_class

  def get_os_class(self):
    return self._os_class

  def gen_oses(self):
    processor = self.get_processor()
    if not processor:
      raise Exception("Processor wasn't defined")
    if not self.get_num_threads():
      raise Exception("No threads. Nothing to do.")
    distributor = self.get_thread_distributor()
    if not distributor:
      raise Exception("Thread-distributor wasn't defined")
    distribution = distributor(self.get_threads(), processor)
    for core, threads in distribution.items():
      if not threads:
        continue
      kernel_class = self._os_class.KERNEL_CLASS
      kernel = kernel_class(core=core, threads=threads)
      core.set_kernel(kernel)
    os = self._os_class(processor=processor)
    processor.set_os(os)
    return (os,)
