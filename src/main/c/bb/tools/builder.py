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
__author__ = "Oleksandr Sviridenko"

import imp
import os.path
import fnmatch
import logging
import inspect
import md5

import bb
from bb.utils import pyimport
from bb.utils import typecheck
from bb.tools import toolchain_manager

BINARIES = []
BUILD_SCRIPTS = []

def all_subclasses(cls):
    return list(cls.__bases__) + [g for s in cls.__bases__
                                   for g in all_subclasses(s)]


def import_build_scripts():
  if BUILD_SCRIPTS:
    return
  search_pathes = (bb.host_os.path.join(bb.env['BB_PACKAGE_HOME'], 'bb'),
                   bb.host_os.path.join(bb.env['BB_APPLICATION_HOME']))
  for search_path in search_pathes:
    for root, dirnames, filenames in bb.host_os.walk(search_path):
      for filename in fnmatch.filter(filenames, '*_build.py'):
        # TODO(team): fix this
        if 'bb/runtime/' in root:
          continue
        BUILD_SCRIPTS.append(bb.host_os.path.join(root, filename))
  logging.debug("Found %d build script(s)" % len(BUILD_SCRIPTS))
  for build_script in BUILD_SCRIPTS:
    fullname = pyimport.get_fullname_by_path(build_script)
    logging.debug('Import script: %s as %s' % (build_script, fullname))
    print fullname
    mod = __import__(fullname, globals(), locals(), [], -1)
  build_script_path = os.path.join(bb.env['BB_APPLICATION_HOME'], 'build.py')
  if not bb.host_os.path.exists(build_script_path):
    logging.warning("Build script '%s' doesn't exist" % build_script_path)
  else:
    logging.debug('Import script: %s' % build_script_path)
    imp.load_source('bb.build', build_script_path)

def extract_images():
  images = []
  print 'Process application'
  if not bb.application.get_num_mappings():
    logging.debug("Application doesn't have any mapping")
    return
  for mapping in bb.application.get_mappings():
    print 'Process mapping "%s"' % mapping.get_name()
    if not mapping.get_num_threads():
      logging.warning('Mapping', mapping.get_name(), "doesn't have threads."
                      'Skip this mapping.')
      continue
    print 'Generate OS'
    os = mapping.gen_os()
    # TODO(team): make different information available in different
    # verbose modes.
    print ' processor =', str(os.get_processor())
    print ' num threads =', os.get_num_threads()
    print ' threads = ['
    for thread in os.get_threads():
      print '  ', str(thread)
    print ' ]'
    print ' num messages =', len(os.get_messages())
    print ' messages = ['
    for message in os.get_messages():
      print '  ', str(message)
    print ' ]'
    print ' max message size =', os.get_max_message_size(), 'byte(s)'
    if not os.get_num_kernels():
      raise Exception('OS should have atleast one kernel.')
    images.append(Image(os))
  return images

def build(build_images=True):
  bb.next_stage()
  import_build_scripts()
  images = extract_images()
  print '%d image(s) to build' % len(images)
  for image in images:
    binary = Binary(image)
    BINARIES.append(binary)
    if build_images:
      logging.debug('Build binary %s' % binary)
      binary.build()
    # If binary was successfully build we can associate it with root object
    with binary.get_image().get_root() as bundle:
      bundle.binary = binary
