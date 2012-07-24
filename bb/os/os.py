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

"""The Bionic Bunny Operating System is a microkernel for microprocessors."""

from bb.config import host_os
from bb.os.microkernel import Microkernel

class OS(object):
  def __init__(self, threads=[]):
    self._microkernel = Microkernel()
    if threads:
      self._microkernel.register_threads(threads)

  @property
  def microkernel(self):
    return self.get_microkernel()

  def get_microkernel(self):
    return self._microkernel
