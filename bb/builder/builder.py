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

import math
import types
import sys
import logging

import bb
from bb.application_build import Application
from bb.lib.utils import typecheck

from bb.builder.rule import Rule
from bb.builder.image import Image

class _Builder(object):

  def __init__(self):
    self._class_rules = {}
    self._instance_rules = {}

  def build(self, application=Application()):
    print 'Initialization'
    #self._build_target_tree(target)

  def _build_target_tree(self, target):
    rule = self.get_rule_by_target(target)
    print rule, target
    leafs = rule.extract_dependencies()
    print target, rule, leafs

  def get_rule_by_target(self, target, class_only=False):
    # What if target is derived from a several target classes?
    if type(target) == types.TypeType:
      return self._class_rules.get(target, None)
    if not isinstance(target, object):
      raise TypeError("Unknown target type")
    if not class_only:
      rule = self._instance_rules.get(target, None)
      if rule:
        return rule
    for target_class, rule in self._class_rules.items():
      if isinstance(target, target_class):
        return rule
    return None

  def rule(self, targets, cases=None):
    owner = caller(2)
    return self.add_rule(targets, Rule(build_cases=(cases, owner)))

  def add_rule(self, targets, rule):
    if not typecheck.is_list(targets) or not typecheck.is_tuple(targets):
      targets = (targets,)
    for target in targets:
      existed_rule = self.get_rule_by_target(target)
      if existed_rule:
        print "The old rule will be updated"
        existed_rule.add_build_cases(rule.get_build_cases())
        rule = existed_rule
      for target in targets:
        self._register_target(target, rule)

  def _register_target(self, target, rule):
    if typecheck.is_string(target):
      target = eval(target)
    elif not isinstance(target, object):
      raise TypeError('Target must be class name or instance')
    if type(target) == types.TypeType:
      self._class_rules[target] = rule
    elif isinstance(target, object):
      self._instance_rules[target] = rule
    else:
      raise TypeError("Unknown target type %s" % target)
    logging.debug("Add rule for target '%s'" % target)
    return rule

Builder = _Builder()

"""

_class_rules = {}
_instance_rules = {}

# Toolchain instance used for building
_toolchain = None

class Application(object):
  def __init__(self):
    self._projects = []

  def add_project(self, project):
    self._projects.append(project)
    return project

  def analyse(self):
    pass

  def get_projects(self):
    return self._projects

def _get_toolchain():
  global _toolchain
  return _toolchain

def _set_toolchain(toolchain):
  global _toolchain
  _toolchain = toolchain
  return _toolchain

class Listener(object):
  pass

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

_projects = list()

def _add_project(os):
  global _projects
  _projects.append(os)

def _get_projects():
  global _projects
  return _projects

class Image(object):

  class Component(object):
    def __init__(self):
      self._targets = []

    def add_targets(self, targets):
      for target in targets:
        self.add_target(target)

    def add_target(self, target):
      if not isinstance(target, object):
        raise TypeError("Must be object instance")
      self._targets.append(target)

    def get_targets(self):
      return self._targets

  def __init__(self):
    self._components = []

  def get_name(self):
    return None

  def add_component(self, component):
    self._components.append(component)

  def remove_component(self, component):
    del self._components[component]

  def get_components(self):
    return self._components

def select_toolchain(self, image):
  for component in image.get_components():
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

_application = None

def set_application(self, application):
  global _application
  _application = application

def get_application(self):
  global _application
  return _application

def build():
  _init()
  application = Application()
  set_application(application)
  application.build_images()
  for image in application.get_images():
    print 'Build image', image, 'with', len(image.get_targets()), 'target(s)'
    if not len(image.get_targets()):
      print "Nothing to build for this image"
      sys.exit(1)
    _select_toolchain(image)
  if bb.CLI.config.options.list_toolchains:
    _print_available_toolchains_and_exit()
  _print_header("Building")
  for image in application.get_images():
    _build_image(image)

def _build_image(image):
  output_filename = image.get_name()
  project.toolchain.compiler.set_output_filename(output_filename)
  project.toolchain.compiler.dry_run = CLI.config.options.dry_run
  project.toolchain.compiler.verbose = CLI.config.options.verbose
  for component in image.get_components():
    _apply_rules(project.targets, project.toolchain)
  try:
    project.toolchain.build()
  except Exception, e:
    print e
    _stop_build_process()

def _stop_build_process():
  print "Stop"

def _print_available_toolchains_and_exit():
  for project in _get_projects():
    print project.os
    print "Available toolchains:", project.available_toolchains
  sys.exit(0)

_project = None

def _set_project(project):
  global _project
  _project = project

def get_project():
  global _project
  return _project
"""
