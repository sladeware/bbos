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

import os.path
import fnmatch
import logging
import networkx
from networkx import bfs_edges
import inspect

import bb
from bb.lib.utils import pyimport
from bb.lib.utils import typecheck
from bb.tools import toolchain_manager

_BUILD_SCRIPTS = list()
_IMAGES = list()

class Binary(object):

  def __init__(self, image):
    self._image = image
    self._toolchain = None
    self._available_toolchains = list()
    self._detect_available_toolchains()

  def use_toolchain(self, toolchain):
    if not toolchain in self._available_toolchains:
      raise Exception('Toolchain %s is not supported' % toolchain)
    self._toolchain = toolchain_manager.new_toolchain(toolchain)

  def get_toolchain(self):
    return self._toolchain

  def get_available_toolchains(self):
    return self._available_toolchains

  def _setup_toolchain(self):
    compiler = self._toolchain.compiler
    compiler.verbose = bb.CLI.config.get_option('verbose', 1)
    compiler.set_output_filename('a.out')

  def _build_object(self, obj):
    print "Build '%s'" % obj
    with obj as bundle:
      if not bundle.build_cases:
        return
      build_case = bundle.build_cases[self._toolchain.get_name()]
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
            print "WARNING: file '%s' cannot be found" % source
            return
          source = alternative_source
        self._toolchain.add_source(os.path.abspath(source))

  def build(self):
    print 'Process image', self._image, 'with', len(self._image), 'bundle(s)'
    if not len(self._image):
      print "Image is empty. Skip image."
      return
    print " available toolchains =", self.get_available_toolchains()
    if not self.get_available_toolchains():
      print "Not available toolchains to build the image."
      return
    toolchain = self.get_available_toolchains()[0]
    self.use_toolchain(toolchain)
    print " selected toolchain =", toolchain
    self._build_object(self._image.get_root())
    edges = bfs_edges(self._image, self._image.get_root())
    for edge in edges:
      parent, obj = edge
      self._build_object(obj)
    self._setup_toolchain()
    self._toolchain.build()

  def _detect_available_toolchains(self):
    if not self._image.get_bundles():
      raise Exception("Image doesn't have bundles")
    first_bundle = self._image.get_bundles()[0]
    available_toolchains = set(first_bundle.build_cases.get_supported_toolchains())
    for bundle in self._image.get_bundles():
      supported_toolchains = set(bundle.build_cases.get_supported_toolchains())
      if not supported_toolchains:
        logging.warning("Bundle of '%s' does not have supported toolchains" % bundle)
        continue
      available_toolchains = available_toolchains.intersection(supported_toolchains)
      if not available_toolchains:
        print "No common toolchains for an objects were found"
        return None
    self._available_toolchains = list(available_toolchains)

class _Image(networkx.Graph):
  def __init__(self, gozer):
    networkx.Graph.__init__(self)
    self._root = gozer
    # Build the image graph
    def _extract_dependencies(node, parent=None):
      with node as bundle:
        self.add_node(node)
        if parent:
          self.add_edge(parent, node)
        if bundle.decomposer:
          children = bundle.decomposer(node)
          if not children:
            return
          for child in children:
            _extract_dependencies(child, node)
    _extract_dependencies(self._root)

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
      logging.warning('Mapping', mapping.get_name(), "doesn't have threads."
                      'Skip this mapping.')
      continue
    print ' number of threads =', mapping.get_num_threads()
    print ' board =', str(mapping.get_board())
    print 'Generate OS'
    oses = mapping.gen_oses()
    for os in oses:
      print ' *', os
      _IMAGES.append(_Image(os))

def build():
  bb.next_stage()
  _import_build_scripts()
  _process_application()
  print '%d image(s) to build' % len(_IMAGES)
  for image in _IMAGES:
    binary = Binary(image)
    binary.build()
