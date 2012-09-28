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

import imp
import os.path
import fnmatch
import logging
import inspect
import md5
import networkx
if networkx.__version__ < '1.5':
  raise Exception('networkx version %s is found, 1.5 or higher is required.' \
                      % networkx.__version__)

import bb
from bb.utils import pyimport
from bb.utils import typecheck
from bb.tools import toolchain_manager

BINARIES = []
BUILD_SCRIPTS = []

class Image(networkx.DiGraph):
  def __init__(self, os):
    networkx.DiGraph.__init__(self)
    self._root = os
    self.add_node(os)
    self.add_edge(os, os.get_processor())
    for kernel in os.get_kernels():
      self.add_edge(os, kernel)
      self.add_edge(kernel, kernel.get_scheduler())
      for thread in kernel.get_threads():
        self.add_edge(kernel, thread)

  def __str__(self):
    return '%s[objects=%d]' % (self.__class__.__name__, len(self))

  def get_root(self):
    return self._root

  def get_objects(self):
    return self.nodes()

  def get_bundles(self):
    bundles = []
    for obj in self.get_objects():
      with obj as bundle:
        bundles.append(bundle)
    return bundles

def all_subclasses(cls):
    return list(cls.__bases__) + [g for s in cls.__bases__
                                   for g in all_subclasses(s)]

class Binary(object):

  def __init__(self, image):
    self._image = None
    self._toolchain = None
    self._available_toolchains = list()
    if image:
      self._set_image(image)

  def get_available_toolchains(self):
    """Return list of available toolchains for this image."""
    # TODO: check the logic.
    if not self._image:
      return
    if not self._image.get_bundles():
      raise Exception("Image doesn't have targets")
    first_target = None
    with self._image.get_root() as target:
      first_target = target
    available = set(first_target.build_cases.get_supported_toolchains())
    if not available:
      logging.warning("First target %s doesn't have build-cases" % target)
      return None
    for target in self._image.get_bundles():
      supported = set(target.build_cases.get_supported_toolchains())
      if not supported:
        logging.warning("%s does not have supported toolchains" % target)
        continue
      old = available
      available = available.intersection(supported)
      if not available:
        print "No common toolchains for an objects were found"
        print "Stoped on target", target
        return None
    return list(available)

  def get_image(self):
    return self._image

  def get_filename(self):
    return md5.md5(str(self.get_image().get_root())).hexdigest()

  def __str__(self):
    return '%s[output_file=%s]' % (self.__class__.__name__, self.get_filename())

  def _set_image(self, image):
    print 'Process image', image
    if not len(image):
      logging.warning("Cannot create a binary for image %s. Image is empty." %
                      image)
      return
    self._image = image

  def use_toolchain(self, toolchain):
    #if not toolchain in self._available_toolchains:
    #  raise Exception('Toolchain %s is not supported' % toolchain)
    self._toolchain = toolchain_manager.new_toolchain(toolchain)

  def get_toolchain(self):
    return self._toolchain

  def _setup_toolchain(self):
    compiler = self._toolchain.compiler
    compiler.verbose = bb.CLI.config.get_option('verbose', 1)
    compiler.set_output_filename(self.get_filename())

  def _build_target(self, target, obj):
    if not target.build_cases:
      return
    #logging.debug("Apply %s to %s" % (target, obj))
    build_case = target.build_cases[self._toolchain.get_name()]
    if not build_case:
      return
    build_script_file = inspect.getsourcefile(build_case.owner)
    build_script_dirname = os.path.dirname(build_script_file)
    for source in build_case['sources']:
      if typecheck.is_function(source):
        source = source(obj)
      # If source is None, skip it
      if not source:
        continue
      if not typecheck.is_string(source):
        raise TypeError("unknown source type: %s" % source)
      if not os.path.exists(source):
        alternative_source = os.path.join(build_script_dirname, source)
        if not os.path.exists(alternative_source):
          logging.warning("File '%s' cannot be found" % source)
          continue
        source = alternative_source
      self._toolchain.add_source(os.path.abspath(source))

  def _build_object(self, obj):
    logging.debug("Build %s" % obj)
    parents = all_subclasses(obj.__class__)
    family = list(parents) + [obj]
    for relative in family:
      if relative.__class__ != bb.Object.__metaclass__ and not issubclass(relative.__class__, bb.Object):
        continue
      with relative as target:
        self._build_target(target, obj)

  def build(self):
    available_toolchains = self.get_available_toolchains()
    print " available toolchains =", available_toolchains
    if not available_toolchains:
      logging.warning("Image doesn't have toolchains for building")
      return
    # TODO(team): provide mechanism how to select a toolchain
    toolchain = available_toolchains[0]
    print " selected toolchain =", toolchain
    self.use_toolchain(toolchain)
    self._build_object(self._image.get_root())
    edges = networkx.dfs_edges(self._image, self._image.get_root())
    for edge in edges:
      parent, obj = edge
      self._build_object(obj)
    self._setup_toolchain()
    self._toolchain.build()

def import_build_scripts():
  if BUILD_SCRIPTS:
    return
  search_pathes = (bb.host_os.path.join(bb.env['BB_PACKAGE_HOME'], 'bb'),
                   bb.host_os.path.join(bb.env['BB_APPLICATION_HOME']))
  for search_path in search_pathes:
    for root, dirnames, filenames in bb.host_os.walk(search_path):
      for filename in fnmatch.filter(filenames, '*_build.py'):
        BUILD_SCRIPTS.append(bb.host_os.path.join(root, filename))
  logging.debug("Found %d build script(s)" % len(BUILD_SCRIPTS))
  for build_script in BUILD_SCRIPTS:
    fullname = pyimport.get_fullname_by_path(build_script)
    logging.debug('Import script: %s as %s' % (build_script, fullname))
    __import__(fullname, globals(), locals(), [], -1)
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
