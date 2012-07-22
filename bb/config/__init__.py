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

import os as host_os # this is host-os support module, do not mix with bb.os
import inspect
import sys
import platform

import bb.config.py_import # override standard __import__

# Compatibility with Python 2.5 through 2.7.
assert (2,5) <= sys.version_info < (3,), """\
This code is meant for Python 2.5 through 2.7.
You might find that the parts you care about still work in older
Pythons or happen to work in newer ones, but you're on your own --
edit __init__.py if you want to try it.
"""

# Setup host environment, check compatibility and some dependencies
if not getattr(bb, 'env', None):
    setattr(bb, 'env', dict())

# TODO: choose the right names

bb.env['BB_HOST_OS'] = platform.system() # NOTE: what about os.name?
bb.env['BB_HOST_PROCESSOR'] = platform.processor()
bb.env['BB_HOST_ARCH'] = platform.machine()
bb.env['BB_HOME'] = host_os.path.abspath(
    host_os.path.join(
        host_os.path.dirname(
            host_os.path.realpath(__file__)), "../..")
    )
bb_package_file = inspect.getsourcefile(sys.modules['bb'])
bb_package_dir = host_os.path.abspath(
    host_os.path.join(host_os.path.dirname(bb_package_file), '..')
    )
bb.env['BB_PACKAGE_HOME'] = bb_package_dir

bb.env['BB_APPLICATION_HOME'] = host_os.path.realpath(host_os.curdir)
sys.path.append(bb.env['BB_APPLICATION_HOME'])

def update_env():
    for k, v in bb.env.items():
        host_os.environ[k] = v
