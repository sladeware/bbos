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

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import fnmatch
import logging

import bb
from bb.lib.utils import pyimport

_BUILD_SCRIPTS = list()

def _import_build_scripts():
  if _BUILD_SCRIPTS:
    return
  search_pathes = (bb.host_os.path.join(bb.env['BB_PACKAGE_HOME'], 'bb'),
                   bb.host_os.path.join(bb.env['BB_APPLICATION_HOME']))
  for search_path in search_pathes:
    for root, dirnames, filenames in bb.host_os.walk(search_path):
      for filename in fnmatch.filter(filenames, '*_build.py'):
        _BUILD_SCRIPTS.append(bb.host_os.path.join(root, filename))
  logging.debug("Found %d build script(s)" % len(_BUILD_SCRIPTS))
  for _ in range(len(_BUILD_SCRIPTS)):
    fullname = pyimport.get_fullname_by_path(_BUILD_SCRIPTS[_])
    __import__(fullname, globals(), locals(), [], -1)

def _process_application():
  print 'Process application'
  if not bb.application.get_num_mappings():
    logging.debug("Application doesn't have any mapping")
    return
  for mapping in bb.application.get_mappings():
    print 'Process mapping "%s"' % mapping.get_name()
    if not mapping.get_num_threads():
      logging.warning("Mapping", mapping.get_name(), "doesn't have threads." \
                        "Skip this mapping.")
      continue
    print "\t", "number of threads", "=", mapping.get_num_threads()
    print "\t", "board", "=", str(board)
    oses = mapping.gen_oses()

def build():
  _import_build_scripts()
  _process_application()
