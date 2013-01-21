#!/usr/bin/env python
#
# http://bionicbunny.org/
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
import networkx
import types

import bb
from bb.app.object import Object
from bb.tools.compilers.compiler import Compiler

if networkx.__version__ < "1.5":
  raise ImportError("networkx version %s is found, 1.5 or higher is required."\
                       % networkx.__version__)

class Image(networkx.DiGraph):
  """Base image interface."""

  def __init__(self, root):
    networkx.DiGraph.__init__(self)
    self._root = None
    self._compiler = None
    self._set_root(root)
    self.build_graph()

  def __str__(self):
    return '%s[num_objects=%d]' % (self.__class__.__name__, len(self))

  def build_graph(self):
    raise NotImplementedError()

  def _set_root(self, root):
    self._root = root

  def get_root(self):
    return self._root

  def get_objects(self):
    return self.nodes()

  def remove_object(self, obj):
    self.remove_node(obj)

  def get_common_compilers(self):
    """Analyses all the objects that are in the graph and returns list of common
    compilers supported by all builders for this image.
    """
    if not self.get_objects():
      raise Exception("Image doesn't have objects")
    builder = bb.get_bldr(self.get_root())
    common_compilers = set(builder.get_supported_compilers())
    if not common_compilers:
      logging.warning("First builder %s doesn't have build-cases" % builder)
      return None
    for obj in self.get_objects():
      builder = bb.get_bldr(obj)
      supported_compilers = set(builder.get_supported_compilers())
      if not supported_compilers:
        logging.warning("%s cannot be built, since does not have supported "
                        "compilers. The object will be removed." % obj)
        self.remove_object(obj)
        continue
      common_compilers = common_compilers.intersection(supported_compilers)
      if not common_compilers:
        logging.warning("No common compilers for an objects were found")
        logging.warning("Stoped on %s" % obj)
        return None
    return list(common_compilers)

  def _set_compiler(self, compiler):
    self._compiler = compiler

  def get_compiler(self):
    """Returns compiler instance that will be used to build this image."""
    return self._compiler

  def _build_object(self, obj):
    logging.debug("Build %s" % obj)
    parents = bb.object.get_all_subclasses(obj)
    family = list(parents) + [obj]
    if not Object in family:
      return
    family.remove(Object)
    for relative in family:
      builder = bb.get_bldr(relative)
      if not builder:
        continue
      # TODO: should be skip class that doesn't support compiling
      if not builder.get_supported_compilers():
        continue
      if not builder.select_compiler(self.get_compiler()):
        raise Exception("%s doesn't support %s compiler" \
                          % (builder, self.get_compiler()))
      builder.build(obj)

  def build(self, compiler=None):
    """Builds an image and produces a :class:`Binary`. Returns created binary.

    If `compiler` was not selected, the first one from the list of common
    compilers will be taken.
    """
    compilers = self.get_common_compilers()
    if not compilers:
      logging.critical("No common compilers.")
      return
    logging.debug("Common compilers: %s" % [_.__name__ for _ in compilers])
    if not compilers:
      logging.warning("Image doesn't have common compilers for building")
      return
    if not compiler:
      compiler = compilers[0]()
    if not isinstance(compiler, Compiler):
      raise TypeError("'compiler' must be derived from Compiler.")
    if not compiler.__class__ in compilers:
      logging.warning("Compiler %s is not supported" % compiler)
      return
    logging.info("Select compiler: %s" % compiler.__class__.__name__)
    self._set_compiler(compiler)
    self._build_object(self._root)
    edges = networkx.dfs_edges(self, self.get_root())
    for edge in edges:
      parent, child = edge
      self._build_object(child)
    compiler.set_verbosity_level(3)
    compiler.compile()
