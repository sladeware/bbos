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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.app.images.image import Image
from bb.app.os import OS

class OSImage(Image):

  def __init__(self, os):
    if not isinstance(os, OS):
      raise TypeError("The root object for this image has to be derived " \
                        "from OS class.")
    Image.__init__(self, os)

  def build_graph(self):
    os = self.get_root()
    self.add_node(os)
    #self.add_edge(os, os.get_processor())
    for kernel in os.get_kernels():
      self.add_edge(os, kernel)
      self.add_edge(kernel, kernel.get_scheduler())
      for thread in kernel.get_threads():
        self.add_edge(kernel, thread)
