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

"""Setup host OS. To make os package available, BB creates an alias as
host_os:

  import bb.host_os

  print bb.host_os.name
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import inspect
import os
import os.path
import platform
import sys

# TODO: choose the right names

# Host environment variables
os.environ["OS_NAME"] = platform.system() # NOTE: what about os.name?
os.environ["PROCESSOR_NAME"] = platform.processor()
os.environ["ARCH_NAME"] = platform.machine()

def _abs_join(*args):
  return os.path.abspath(os.path.join(*args))

# BB basic variables
bb_home = _abs_join(os.path.dirname(os.path.realpath(__file__)), "../..")
os.environ.setdefault("BB_HOME", bb_home)
bb_package_file_path = inspect.getsourcefile(sys.modules["bb"])
bb_package_dir_path = _abs_join(os.path.dirname(bb_package_file_path), "..", "bb")
os.environ["BB_PACKAGE_PATH"] = bb_package_dir_path

# Application environment variables
os.environ["BB_APPLICATION_HOME"] = os.path.realpath(os.curdir)
sys.path.append(os.environ["BB_APPLICATION_HOME"])

# Build environment
os.environ.setdefault("BB_BUILD_DIR_NAME", "build")
