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

"""
Simple way to define *_build.py build-script that will build all the targets
with base class bb.Thread:

  from bb import builder

  builder.rule('bb.Thread', cases={
    'simulator' : {
      'srcs' : ("f1.py", "f2.py", "f3.py"),
      'lstn' : ("l1"),
    }
    ('propgcc', 'catalina') : {
      'srcs' : ("f1.c", "f2.c")
    }
  })

The case when developer needs to build a thread printer defined in
helloworld.py:

  from bb import builder
  from bb.buildtime.application import helloworld

  builder.rule(helloworld.printer, cases={
    'simulator' : {
      'srcs' : ("printer.py",)
    }
    ('propgcc', 'catalina') : {
      'srcs' : ("printer.c",)
    }
  })

"""

import inspect
import math
import fnmatch
import imp

import bb
from bb import application as bbapp
from bb.config import host_os
from bb.lib.utils import typecheck
from bb.lib.build import toolchain_manager

_targets = []
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
    args = self._cases.get(toolchain.__class__.__name__, None)
    if 'srcs' in args:
      toolchain.add_sources(args['srcs'])

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
    self._fix_args(args, owner)
    self._cases[name] = args

  def _fix_args(self, args, owner):
    build_script_file = inspect.getsourcefile(owner)
    build_script_dirname = host_os.path.dirname(build_script_file)
    if 'srcs' in args:
      if typecheck.is_tuple(args['srcs']):
        args['srcs'] = list(args['srcs'])
      for i in range(len(args['srcs'])):
        src = args['srcs'][i]
        if not host_os.path.exists(src):
          alternative_src = host_os.path.join(build_script_dirname, src)
          if not host_os.path.exists(alternative_src):
            print "WARNING: file '%s' cannot be found" % src
            return
          args['srcs'][i] = alternative_src

class Listener(object):
  pass

def _get_rule_by_target(target):
  global _class_rules
  global _instance_rules
  if typecheck.is_string(target):
    return _class_rules.get(target, None)
  elif isinstance(target, object):
    return _instance_rules.get(target, None)
  else:
    raise TypeError("Unknown target type")

def rule(targets, cases):
  owner = bb.config.builtins.caller(2)
  if not typecheck.is_list(targets) or not typecheck.is_tuple(targets):
    targets = (targets,)
  for target in targets:
    #print target
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
  rule = _get_rule_by_target(target)
  if not rule:
    rule = Rule()
  rule.add_build_cases(owner, cases)
  if typecheck.is_string(target):
    _class_rules[target] = rule
  elif isinstance(target, object):
    _instance_rules[target] = rule
  else:
    raise TypeError("Unknown target type %s" % target)
  print owner.__name__, ":", "add rule for target '%s'" % target

def _add_targets(targets):
  for target in targets:
    _add_target(target)

def _add_target(target):
  global _targets
  if not isinstance(target, object):
    raise TypeError("Must be object instance")
  rule = _get_rule_by_target(target) \
      or _get_rule_by_target(target.__class__.__name__)
  if not rule:
    print "WARNING: Don't have a rule for target", target
    return
  _targets.append(target)

def _get_targets():
  global _targets
  return _targets

def _import_build_scripts():
  root = host_os.path.join(bb.env['BB_PACKAGE_HOME'], 'bb')
  build_scripts = []
  for root, dirnames, filenames in host_os.walk(root):
    for filename in fnmatch.filter(filenames, '*_build.py'):
      build_scripts.append(host_os.path.join(root, filename))
  print "Found %d build script(s)" % len(build_scripts)
  for _ in range(len(build_scripts)):
    imp.load_source("bs%d" % _, build_scripts[_])

# TODO: move the function
def default_thread_distribution(threads, cores):
  step = int(math.ceil(float(len(threads)) / float(len(cores))))
  return [threads[x : x + step] for x in xrange(0, len(threads), step)]

def _analyse_application():
  _print_header('Analyse application')
  mappings = bbapp.get_mappings()
  for mapping in mappings:
    if not isinstance(mapping, bb.Mapping):
      raise Exception("Must be Mapping")
    _add_target(mapping)
    print "Analyse mapping '%s'" % mapping.get_name()
    if not mapping.get_num_threads():
      logging.error("Mapping", mapping.get_name(), "doesn't have threads")
      return
    print "*", "number of threads", "=", mapping.get_num_threads()
    processor = mapping.get_processor()
    if not processor:
      print "Mapping", mapping.get_name(), "doesn't connected to any processor"
      return
    print "*", "processor", "=", str(processor)
    cores = processor.get_cores()
    # Some cores can be disabled or not defined
    active_cores = list()
    for core_id in range(len(cores)):
      if cores[core_id]:
        active_cores.append(core_id)
    if not active_cores:
      print "Processor does not have active cores"
      return
    threads_per_core = default_thread_distribution(mapping.get_threads(), active_cores)
    print "Thread distribution:"
    for i in range(len(threads_per_core)):
      if not threads_per_core[i]:
        continue
      print "\t", str(processor.get_core(i)), ":", [str(_) for _ in threads_per_core[i]]
    os_class = mapping.get_os_class()
    for i in range(len(threads_per_core)):
      core_id = active_cores[i]
      core = cores[core_id]
      os = os_class(threads_per_core[core_id])
      _add_target(os)
      print "Assemble OS"
      _add_target(os.microkernel)
      _add_targets(os.microkernel.get_threads())

def _print_header(title):
  print '-' * 70
  print title
  print '-' * 70

def _init():
  _print_header('Initialization')
  _import_build_scripts()

def _apply_rules():
  global _class_rules
  global _instance_rules
  for target, rule in _class_rules.items():
    rule.apply(target, _get_toolchain())
  for target, rule in _instance_rules.items():
    rule.apply(target, _get_toolchain())

def build():
  _init()
  _analyse_application()
  print len(_get_targets()), "target(s) to build"
  if not len(_get_targets()):
    print "Nothing to build"
    exit(1)
  _print_header("Building")
  _select_toolchain()
  _apply_rules()
  _toolchain.build()

def _select_toolchain():
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
  print "Available toolchains:", list(available_toolchains)
  _set_toolchain(toolchain_manager.new_toolchain(
      list(available_toolchains).pop(0)))
  print "Use toolchain:", _get_toolchain().__class__.__name__
