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

"""A kernel represents a non-blocking computational resource, which is in most
cases simply a core of a microcontroller. Threads run within a kernel using a
customizable time sharing scheduler algorithm.

The kernel is represented by :class:`bb.os.kernel.Kernel`.
"""

__copyright__ = 'Copyyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import bb
from bb.lib.utils import typecheck
from bb.os.kernel.schedulers import Scheduler, StaticScheduler

class Kernel(object):
  """The heart of BB operating system."""

  def __init__(self, scheduler=StaticScheduler()):
    self._threads = dict()
    # Select scheduler first if defined before any thread will be added
    # By default, if scheduler was not defined will be used static
    # scheduling policy.
    self._scheduler = None
    self.set_scheduler(scheduler)

  def set_scheduler(self, scheduler):
    """Select scheduler."""
    if not isinstance(scheduler, Scheduler):
      raise Exception("Scheduler '%s' must be bb.os.kernel.Scheduler "
                      "sub-class" % scheduler)
    self._scheduler = scheduler

  def get_scheduler(self):
    return self._scheduler

  def get_threads(self):
    return self._threads.values()

  def get_num_threads(self):
    return len(self.get_threads())

  def unregister_thread(self, thread):
    if not isinstance(thread, bb.Thread):
      raise TypeError()
    if thread.get_name() in self._threads:
      del self._threads[thread.get_name()]
    return thread

  def register_thread(self, thread):
    if not isinstance(thread, bb.Thread):
      raise TypeError()
    self._threads[thread.get_name()] = thread
    return thread

  def register_threads(self, threads):
    if not typecheck.is_list(threads):
      raise TypeError("Must be list")
    for thread in threads:
      self.register_thread(thread)
