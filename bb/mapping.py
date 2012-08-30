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
from bb.hardware.devices.boards import Board
from bb.hardware.devices.processors import Processor
from bb.lib.utils import typecheck

def roundrobin_thread_distributor(threads, processors):
  """Default thread distributor provides round-robin distribution of threads
  between all cores within the processors.
  """
  thread_distribution = {}
  for processor in processors:
    if not isinstance(processor, Processor):
      raise TypeError("processor must be derived from Processor")
    thread_distribution[processor] = {}
    for core in processor.get_cores():
      thread_distribution[processor][core] = []
  p = 0
  c = 0
  for thread in threads:
    if not isinstance(thread, bb.os.Thread):
      raise TypeError("thread must be derived from bb.os.Thread")
    processor = processors[p]
    p = (p + 1) % len(processors)
    core = processor.get_cores()[c]
    c = (c + 1) % len(processor.get_cores())
    thread_distribution[processor][core].append(thread)
  return thread_distribution

class Mapping(object):
  OS_CLASS = bb.os.OS

  def __init__(self, name, board=None, os_class=None,
               thread_distributor=roundrobin_thread_distributor):
    self._name = None
    self._threads = dict()
    self._os_class = None
    self._is_simulation_mode = False
    self._board = None
    self._thread_distributor = None
    if thread_distributor:
      self.set_thread_distributor(thread_distributor)
    # NOTE: for now we will force user to provide a name
    self.set_name(name)
    if os_class:
      self.set_os_class(os_class)
    else:
      self.set_os_class(self.OS_CLASS)
    if board:
      self.set_board(board)
    # Once a new mapping was created, it will automatically register itself
    # within existed application. See issue #16.
    bb.application.register_mapping(self)

  def set_name(self, name):
    if not typecheck.is_string(name):
      raise Exception("name must be string")
    self._name = name

  def get_name(self):
    return self._name

  def set_thread_distributor(self, f):
    self._thread_distributor = f

  def get_thread_distributor(self):
    return self._thread_distributor

  def register_thread(self, thread):
    if not isinstance(thread, bb.os.Thread):
      raise Exception("Must be derived from bb.os.Thread: %s", thread)
    if thread.get_name() is None:
      frmt = thread.get_name_format()
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

  def set_simulation_mode(self):
    self._is_simulation_mode = True

  def is_simulation_mode(self):
    return self._is_simulation_mode

  def get_board(self):
    """Return :class:`bb.hardware.devices.boards.board.Board`
    instance.
    """
    return self._board

  def set_board(self, board):
    if not isinstance(board, Board):
      raise TypeError("Requires Board class.")
    self._board = board

  def is_board_defined(self):
    """Whether or not a board was defined. Return ``True`` value if the
    :class:`bb.hardware.devices.boards.board.Board` instance can be
    obtained by using specified core. Otherwise return ``False``.
    """
    return not not self.get_board()

  def set_os_class(self, os_class):
    if not issubclass(os_class, bb.os.OS):
      raise TypeError("Must be derived from bbos.OS class: %s" % os_class)
    self._os_class = os_class

  def get_os_class(self):
    return self._os_class

  def gen_oses(self):
    board = self.get_board()
    if not board:
      raise Exception("Board wasn't defined")
    if not self.get_num_threads():
      raise Exception("No threads. Nothing to do.")
    distributor = self.get_thread_distributor()
    if not distributor:
      raise Exception("Thread-distributor wasn't defined")
    distribution = distributor(self.get_threads(),
                               self.get_board().get_processors())
    os_class = self.get_os_class()
    oses = list()
    for processor, core_distribution in distribution.items():
      for core, threads in core_distribution.items():
        if not threads:
          continue
        kernel = bb.os.Kernel(core=core, threads=threads)
        core.set_kernel(kernel)
      os = os_class(processor)
      processor.set_os(os)
      oses.append(os)
    return oses
