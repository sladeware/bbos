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

import bb
from bb.hardware.devices.processors import Processor
from bb.lib.utils import typecheck

class Mapping(object):
  OS_CLASS = bb.os.OS

  def __init__(self, name, os_class=None, processor=None):
    self._name = None
    self._threads = dict()
    self._os_class = None
    self._is_simulation_mode = False
    self._processor = None
    # NOTE: for now we will force user to provide a name
    self.set_name(name)
    if os_class:
      self.set_os_class(os_class)
    else:
      self.set_os_class(self.OS_CLASS)
    if processor:
      self.set_processor(processor)

  def set_name(self, name):
    if not typecheck.is_string(name):
      raise Exception("name must be string")
    self._name = name

  def get_name(self):
    return self._name

  def register_thread(self, thread):
    if not isinstance(thread, bb.Thread):
      raise Exception("Must be derived from bb.Thread")
    self._threads[ thread.get_name() ] = thread

  def register_threads(self, threads):
    for thread in threads:
      self.register_thread(thread)

  def get_num_threads(self):
    return len(self.get_threads())

  def get_threads(self):
    return self._threads.values()

  def set_simulation_mode(self):
    self._is_simulation_mode = True

  def is_simulation_mode(self):
    return self._is_simulation_mode

  def get_processor(self):
    return self._processor

  def set_processor(self, processor):
    if not isinstance(processor, Processor):
      raise TypeError("Requires Processor class.")
    self._processor = processor

  def set_os_class(self, os_class):
    if not issubclass(os_class, bb.os.OS):
      raise TypeError("Must be derived from bbos.OS class: %s" % os_class)
    self._os_class = os_class

  def get_os_class(self):
    return self._os_class
