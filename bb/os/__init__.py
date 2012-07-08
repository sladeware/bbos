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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Oleksandr Sviridenko"

"""The Bionic Bunny Operating System is a microkernel for microprocessors."""

from bb.os.kernel import *
from bb.builder import toolchain_manager

def os_factory(*args, **kargs):
    """:class:`OS` factory. Return new class derived from
    :class:`OS` class.
    """
    class OperatingSystemContainer(OS):
        def __init__(self):
            OS.__init__(self, *args, **kargs)
    # Tricky moment...
    for toolchain in toolchain_manager.get_toolchains():
        package_class = toolchain.get_package_class(OS)
        toolchain.pack(OperatingSystemContainer, package_class)
    return OperatingSystemContainer
