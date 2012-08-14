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

import inspect
import math
import imp
import types
import sys

import bb
from bb.cli import CLI
from bb import application as bbapp
from bb.lib.utils import typecheck
from bb.lib.build import toolchain_manager
from bb.lib.build.compilers import CustomCCompiler

_class_rules = {}
_instance_rules = {}

# Toolchain instance used for building
_toolchain = None

def _get_toolchain():
  global _toolchain
  return _toolchain

def _set_toolchain(toolchain):
  global _toolchain
  _toolchain = toolchain
  return _toolchain

class Rule(object):
  def __init__(self):
    self._toolchains = dict()
    self._cases = {}

  def get_supported_toolchains(self):
    return self._cases.keys()

  def apply(self, target, toolchain):
    owner, args = self._cases.get(toolchain.__class__.__name__, None)
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

  def add_build_cases(self, owner, cases):
    if not typecheck.is_dict(cases):
      raise TypeError("Must be dict")
    for toolchains, args in cases.items():
      if typecheck.is_tuple(toolchains):
        for toolchain in toolchains:
          self.add_build_case(owner, toolchain, args)
      else:
        self.add_build_case(owner, toolchains, args)

  def add_build_case(self, owner, name, args):
    if not toolchain_manager.is_supported_toolchain(name):
      raise Exception("Toolchain '%s' is not supported." % name)
    self._cases[name] = (owner, args)

class Listener(object):
  pass

def _get_rule_by_target(target, class_only=False):
  """What if target is derived from a several target classes?"""
  global _class_rules
  global _instance_rules
  if type(target) == types.TypeType:
    return _class_rules.get(target, None)
  if not isinstance(target, object):
    raise TypeError("Unknown target type")
  if not class_only:
    rule = _instance_rules.get(target, None)
    if rule:
      return rule
  for target_class, rule in _class_rules.items():
    if isinstance(target, target_class):
      return rule
  return None

def rule(targets, cases):
  owner = bb.config.builtins.caller(2)
  if not typecheck.is_list(targets) or not typecheck.is_tuple(targets):
    targets = (targets,)
  for target in targets:
    _add_rule(target, cases, owner)

def _get_class_rules():
  global _class_rules
  return _class_rules.values()

def _get_instance_rules():
  global _instance_rules
  return _instance_rules.values()

def _get_rules():
  return _get_class_rules() + _get_instance_rules()

def _add_rule(target, cases, owner):
  global _class_rules
  global _instance_rules
  if typecheck.is_string(target):
    target = eval(target)
  elif not isinstance(target, object):
    raise TypeError("Target must be class name or instance")
  rule = _get_rule_by_target(target)
  if not rule:
    rule = Rule()
  rule.add_build_cases(owner, cases)
  if type(target) == types.TypeType:
    _class_rules[target] = rule
  elif isinstance(target, object):
    _instance_rules[target] = rule
  else:
    raise TypeError("Unknown target type %s" % target)
  print owner.__name__, ":", "add rule for target '%s'" % target

def _print_header(title):
  print "=>", title

def _init():
  _print_header('Initialization')

def _apply_rules(targets, toolchain):
  global _class_rules
  global _instance_rules
  for target in targets:
    rule = _get_rule_by_target(target)
    if not rule:
      print "WARNING: Don't have a rule for target", target
  for target in targets:
    for match_target_class, rule in _class_rules.items():
      if isinstance(target, match_target_class):
        rule.apply(target, toolchain)
  for target in targets:
    rule = _instance_rules.get(target, None)
    if rule:
      rule.apply(target, toolchain)

def _analyse_application():
  _print_header('Analyse application')
  mappings = bbapp.get_mappings()
  for mapping in mappings:
    print "Analyse mapping '%s'" % mapping.get_name()
    if not mapping.get_num_threads():
      logging.error("Mapping", mapping.get_name(), "doesn't have threads")
      return
    print "*", "number of threads", "=", mapping.get_num_threads()
    board = mapping.get_board()
    if not board:
      print "Mapping", mapping.get_name(), "doesn't connected to a board"
      return
    os_class = mapping.get_os_class()
    thread_distributor = mapping.get_thread_distributor()
    print "*", "board", "=", str(board)
    # TODO: verify board; maybe this board doesn't have the processors.
    print "Thread distribution:"
    thread_distribution = thread_distributor(mapping.get_threads(),
                                             board.get_processors())
    for processor in board.get_processors():
      print ' ', str(processor)
      project = Project(mapping)
      for core, threads in thread_distribution[processor].items():
        if not threads:
          continue
        print '  ', str(core), ':', [str(_) for _ in threads]
        os = os_class(core=core, threads=threads)
        project.oses.append(os)
      project.extract_targets()
      _add_project(project)

_projects = list()

def _add_project(os):
  global _projects
  _projects.append(os)

def _get_projects():
  global _projects
  return _projects

class Project(object):
  def __init__(self, mapping):
    self.mapping = mapping
    self.oses = []
    self.targets = list()

  def extract_targets(self):
    for os in self.oses:
      self.add_target(os)
      self.add_target(os.kernel)
      self.add_targets(os.kernel.get_threads())
      self.add_target(os.kernel.get_scheduler())
      self.add_target(os.core.get_processor())

  def add_targets(self, targets):
    for target in targets:
      self.add_target(target)

  def add_target(self, target):
    if not isinstance(target, object):
      raise TypeError("Must be object instance")
    self.targets.append(target)

  def get_targets(self):
    return self.targets

  def select_toolchain(self):
    first_rule = _get_rules()[0]
    available_toolchains = set(first_rule.get_supported_toolchains())
    for rule in _get_rules():
      supported_toolchains = set(rule.get_supported_toolchains())
      if not supported_toolchains:
        print "Rule", rule, "does not have supported toolchains"
        return False
      available_toolchains = available_toolchains.intersection(supported_toolchains)
      if not available_toolchains:
        print "No common toolchains for an objects were found"
        return None
    self.available_toolchains = list(available_toolchains)
    self.toolchain = toolchain_manager.new_toolchain(self.available_toolchains[0])
    #print "Use toolchain:", self.toolchain.__class__.__name__

def build():
  _init()
  _analyse_application()
  for project in _get_projects():
    print len(project.get_targets()), "target(s) to build"
    if not len(project.get_targets()):
      print "Nothing to build"
      exit(1)
    project.select_toolchain()
  if bb.CLI.config.options.list_toolchains:
    _print_available_toolchains_and_exit()
  _start_build_process()

def _print_available_toolchains_and_exit():
  for project in _get_projects():
    print project.os
    print "Available toolchains:", project.available_toolchains
  sys.exit(0)

def _start_build_process():
  _print_header("Building")
  for project in _get_projects():
    output_filename = "%s" % project.mapping.get_name()
    project.toolchain.compiler.set_output_filename(output_filename)
    project.toolchain.compiler.dry_run = CLI.config.options.dry_run
    project.toolchain.compiler.verbose = CLI.config.options.verbose
    _apply_rules(project.targets, project.toolchain)
    try:
      project.toolchain.build()
    except Exception, e:
      print e
      _stop_build_process()

def _stop_build_process():
  print "Stop"
