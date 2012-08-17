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

import bb
from bb.os.kernel import Kernel

class OS(object):
  def __init__(self, core, threads=[]):
    self._core = core
    self._kernel = Kernel()
    if threads:
      self._kernel.register_threads(threads)
    core.set_os(self)

  @property
  def core(self):
    return self._core

  def get_core(self):
    return self._core

  @property
  def kernel(self):
    return self.get_kernel()

  def get_kernel(self):
    return self._kernel

  def __str__(self):
    return "OS on core '%s', with %d thread(s): %s" \
        % (self.get_core(), self.kernel.get_num_threads(),
           [str(_) for _ in self.kernel.get_threads()])
