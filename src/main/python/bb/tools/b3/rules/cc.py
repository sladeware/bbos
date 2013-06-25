# -*- coding: utf-8 -*-
#
# CC-like rules
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko <info@bionicbunny.org>

from __future__ import print_function

import sys

from bb.tools.b3 import buildfile
from bb.tools.b3.rules.binary import Binary
from bb.tools.b3.rules.library import Library
from bb.tools.b3.rules.fileset import Fileset
from bb.tools.compilers import GCC
from bb.utils import typecheck
from bb.utils import logging

logger = logging.get_logger("bb")

class CCLikeRule(object):

  properties = (("programming_language", "c"),)

  def __init__(self, includes=[], copts=[]):
    self._includes = []
    self._copts = []
    if includes:
      self.set_includes(includes)
    if copts:
      self.set_copts(copts)

  def set_includes(self, includes):
    if not typecheck.is_list(includes):
      raise TypeError()
    self._includes = includes

  def get_includes(self):
    return self._includes

  def set_copts(self, copts):
    if not typecheck.is_list(copts):
      raise TypeError()
    self._copts = copts

  def get_copts(self):
    return self._copts

class CCLibrary(Library, CCLikeRule):

  def __init__(self, target=None, name=None, srcs=[], deps=[], **kwargs):
    Library.__init__(self, target=target, name=name, srcs=srcs, deps=deps)
    CCLikeRule.__init__(self, **kwargs)

class CCBinary(Binary, CCLikeRule):

  is_language_dependent = True
  properties = (("programming_language", "c"),)

  def __init__(self, target=None, name=None, srcs=[], deps=[],
               compiler_class=None, **kwargs):
    if not compiler_class:
      compiler_class = GCC
    Binary.__init__(self, target=target, name=name, srcs=srcs, deps=deps,
                    compiler_class=compiler_class)
    CCLikeRule.__init__(self, **kwargs)

  def execute(self):
    print("Build cc binary '%s' with '%s'" %
          (self.get_name(), self.compiler.__class__.__name__))
    buildfile.dependency_graph.resolve_forks()
    # NOTE: this has to be fixed
    self.compiler.add_include_dir(self.get_build_dir())
    for src in self.get_sources():
      if typecheck.is_string(src):
        self.compiler.add_file(src)
      elif isinstance(src, Fileset):
        self.compiler.add_files(src.get_sources())
    for dep in self.get_dependencies():
      if isinstance(dep, CCLibrary):
        self.compiler.add_files(dep.get_sources())
        self.compiler.add_include_dirs(dep.get_includes())
    if not self.compiler.get_files():
      print("No source files", file=sys.stderr)
      exit(0)
    self.compiler.add_include_dirs(self.get_includes())
    self.compiler.set_output_filename(self.get_name())
    try:
      self.compiler.compile()
    except Exception, e:
      logger.error(e)
