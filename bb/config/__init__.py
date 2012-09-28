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

import inspect
import sys
import platform

import bb
#import bb.config.compilers.python.importer # override standard __import__
import bb.config.compilers.python.builtins

# Compatibility with Python 2.5 through 2.7.
assert (2,5) <= sys.version_info < (3,), """\
This code is meant for Python 2.5 through 2.7.
You might find that the parts you care about still work in older
Pythons or happen to work in newer ones, but you're on your own --
edit __init__.py if you want to try it.
"""

class _Environment(object):
  def __init__(self):
    self._vars = dict()

  def get(self, key, default_value=None):
    return self._vars.get(key, default_value)

  def echo(self, key):
    print self.get(key)

  def pwd(self):
    f = caller(n=2)
    return bb.host_os.path.dirname(inspect.getfile(f))

  def __setitem__(self, key, value):
    self._vars[key] = value

  def __getitem__(self, key):
    return self.get(key)

# Setup host environment, check compatibility and some dependencies
if not getattr(bb, 'env', None):
  setattr(bb, 'env', _Environment())

# TODO: choose the right names

#_______________________________________________________________________________
#
# Host environment variables
#_______________________________________________________________________________

bb.env['BB_HOST_OS'] = platform.system() # NOTE: what about os.name?
bb.env['BB_HOST_PROCESSOR'] = platform.processor()
bb.env['BB_HOST_ARCH'] = platform.machine()

#_______________________________________________________________________________
#
# BB basic variables
#_______________________________________________________________________________

bb.env['BB_HOME'] = bb.host_os.path.abspath(
  bb.host_os.path.join(
    bb.host_os.path.dirname(
      bb.host_os.path.realpath(__file__)), "../..")
  )
bb_package_file = inspect.getsourcefile(sys.modules['bb'])
bb_package_dir = bb.host_os.path.abspath(
  bb.host_os.path.join(bb.host_os.path.dirname(bb_package_file), '..')
  )
bb.env['BB_PACKAGE_HOME'] = bb_package_dir

#_______________________________________________________________________________
#
# Application environment variables
#_______________________________________________________________________________

bb.env['BB_APPLICATION_HOME'] = bb.host_os.path.realpath(bb.host_os.curdir)
sys.path.append(bb.env['BB_APPLICATION_HOME'])

#_______________________________________________________________________________
#
# Build environment
#_______________________________________________________________________________

bb.env['BB_BUILD_DIR_NAME'] = bb.host_os.environ.get('BB_BUILD_DIR_NAME', 'build')
