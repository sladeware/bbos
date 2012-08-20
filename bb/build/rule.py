#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import inspect

import bb
from bb.lib.utils import typecheck
from bb.lib.build import toolchain_manager
from bb.lib.build.compilers import CustomCCompiler

class Rule(object):
  def __init__(self, build_cases=None):
    self._toolchains = dict()
    self._build_cases = {}
    if build_cases:
      cases, owner = build_cases
      if cases:
        self.add_build_cases(cases, owner)

  def get_supported_toolchains(self):
    return self._build_cases.keys()

  def apply(self, target, toolchain):
    owner, args = self._build_cases.get(toolchain.__class__.__name__, None)
    if 'srcs' in args:
      for src in self._get_srcs(args['srcs'], owner, target):
        toolchain.add_source(src)

  def _get_srcs(self, sources, owner, target):
    srcs = []
    build_script_file = inspect.getsourcefile(owner)
    build_script_dirname = bb.host_os.path.dirname(build_script_file)
    if typecheck.is_tuple(sources):
      sources = list(sources)
    for src in sources:
      if typecheck.is_function(src):
        src = src(target)
      # If source is None, skip it
      if not src:
        continue
      if not typecheck.is_string(src):
        raise TypeError("unknown source type: %s" % src)
      if not bb.host_os.path.exists(src):
        alternative_src = bb.host_os.path.join(build_script_dirname, src)
        if not bb.host_os.path.exists(alternative_src):
          print "WARNING: file '%s' cannot be found" % src
          return
        srcs.append(alternative_src)
      else:
        srcs.append(src)
    return srcs

  def add_build_cases(self, cases, owner):
    if not typecheck.is_dict(cases):
      raise TypeError("Must be dict: %s" % cases)
    for toolchains, args in cases.items():
      if typecheck.is_tuple(toolchains):
        for toolchain in toolchains:
          self.add_build_case(owner, toolchain, args)
      else:
        self.add_build_case(owner, toolchains, args)

  def add_build_case(self, owner, name, args):
    if not toolchain_manager.is_supported_toolchain(name):
      raise Exception("Toolchain '%s' is not supported." % name)
    self._build_cases[name] = (owner, args)
