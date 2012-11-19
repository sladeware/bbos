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

import logging
import md5

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
    exit(0)
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