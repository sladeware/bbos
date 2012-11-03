#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import logging
import networkx
if networkx.__version__ < "1.5":
  raise RuntimeError("networkx version %s is found, 1.5 or higher is required."\
                       % networkx.__version__)

import bb
import bb.object
from bb.application import Object
from bb.tools.compilers.compiler import Compiler

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

  def get_common_compilers(self):
    """Returns list of common compilers supported by all builders for this
    image.
    """
    if not self.get_objects():
      raise Exception("Image doesn't have objects")
    builder = self.get_root().get_builder()
    common_compilers = set(builder.get_supported_compilers())
    if not common_compilers:
      logging.warning("First builder %s doesn't have build-cases" % builder)
      return None
    for object_ in self.get_objects():
      builder = object_.get_builder()
      supported_compilers = set(builder.get_supported_compilers())
      if not supported_compilers:
        logging.warning("%s does not have supported compilers" % object_)
        continue
      common_compilers = common_compilers.intersection(supported_compilers)
      if not common_compilers:
        logging.warning("No common compilers for an objects were found")
        logging.warning("Stoped on %s" % object_)
        return None
    return list(common_compilers)

  def _set_compiler(self, compiler):
    self._compiler = compiler

  def get_compiler(self):
    return self._compiler

  def _build_object(self, object_):
    logging.debug("Build %s" % object_)
    parents = bb.object.get_all_subclasses(object_.__class__)
    family = list(parents) + [object_]
    if not Object.Buildable in family:
      return
    family.remove(Object)
    for relative in family:
      if relative.__class__ != Object.__metaclass__ and \
            not issubclass(relative.__class__, Object):
        continue
      builder = relative.get_builder()
      print builder, self.get_compiler()
      #builder.select_compiler(self.get_compiler())
      #print builder.get_compiler_params()

  def build(self, compiler=None):
    """Builds an image an produces a Binary."""
    compilers = self.get_common_compilers()
    logging.info("Common compilers: %s" % [_.__name__ for _ in compilers])
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
    logging.info("Selected compiler: %s" % compiler.__class__.__name__)
    self._set_compiler(compiler)
    self._build_object(self._root)
    edges = networkx.dfs_edges(self, self.get_root())
    for edge in edges:
      parent, child = edge
      self._build_object(child)
