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

import fnmatch
import logging
import math
import sys
import types

import bb
from bb.lib.utils import typecheck
from bb.lib.utils import pyimport
from bb.lib.build import toolchain_manager
from bb.builder.rule import Rule
from bb.builder.image import Image

class _Builder(object):

  def __init__(self):
    self._class_rules = {}
    self._instance_rules = {}
    self._toolchain_for_image = {}
    self.context = {}
    self._import_build_scripts_done = False

  def _import_build_scripts(self):
    search_pathes = (bb.host_os.path.join(bb.env['BB_PACKAGE_HOME'], 'bb'),
                     bb.host_os.path.join(bb.env['BB_APPLICATION_HOME']))
    build_scripts = []
    for search_path in search_pathes:
      for root, dirnames, filenames in bb.host_os.walk(search_path):
        for filename in fnmatch.filter(filenames, '*_build.py'):
          build_scripts.append(bb.host_os.path.join(root, filename))
    logging.debug("Found %d build script(s)" % len(build_scripts))
    for _ in range(len(build_scripts)):
      fullname = pyimport.get_fullname_by_path(build_scripts[_])
      __import__(fullname, globals(), locals(), [], -1)
    self._import_build_scripts_done = True

  def _select_toolchain(self, image):
    first_rule = self.get_rule_by_target(image.get_targets()[0])
    available_toolchains = set(first_rule.get_supported_toolchains())
    for target in image.get_targets():
      rule = self.get_rule_by_target(target)
      supported_toolchains = set(rule.get_supported_toolchains())
      if not supported_toolchains:
        print "Rule", rule, "does not have supported toolchains"
        return False
      available_toolchains = available_toolchains.intersection(supported_toolchains)
      if not available_toolchains:
        print "No common toolchains for an objects were found"
        return None
    available_toolchains = list(available_toolchains)
    toolchain = toolchain_manager.new_toolchain(available_toolchains[0])
    print "Use toolchain", toolchain, "for image", image
    self._toolchain_for_image[image] = toolchain

  def set_application_class(self, application_class):
    self._application_class = application_class

  def get_application(self):
    return self._application

  def prepare(self):
    self._application = self._application_class()
    self._application.build_images()

  def build(self):
    if not self._import_build_scripts_done:
      self._import_build_scripts()
    print 'Initialization'
    self.prepare()
    for image in self._application.get_images():
      self.build_image(image)

  def build_image(self, image):
    print 'Build image', image, 'with', len(image.get_targets()), 'target(s)'
    if not len(image.get_targets()):
      print "Nothing to build for this image"
      sys.exit(1)
    self._select_toolchain(image)
    output_filename = image.get_name()
    toolchain = self._toolchain_for_image[image]
    toolchain.compiler.set_output_filename(output_filename)
    #toolchain.compiler.dry_run = CLI.config.options.dry_run
    toolchain.compiler.verbose = bb.CLI.config.options.verbose
    self._apply_rules(image)
    try:
      toolchain.build()
    except Exception, e:
      print e
      exit(1)

  def _apply_rules(self, image):
    toolchain = self._toolchain_for_image[image]
    for target in image.get_targets():
      rule = self.get_rule_by_target(target)
      if not rule:
        print "WARNING: Don't have a rule for target", target
    for target in image.get_targets():
      for match_target_class, rule in self._class_rules.items():
        if isinstance(target, match_target_class):
          rule.apply(target, toolchain)
    for target in image.get_targets():
      rule = self._instance_rules.get(target, None)
      if rule:
        rule.apply(target, toolchain)

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
    # Ignore rule if there are no targets
    if not targets:
      return
    owner = caller(2)
    return self.add_rule(targets, Rule(build_cases=(cases, owner)))

  def get_rules(self):
    return self._class_rules.values() + self._instance_rules.values()

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
    logging.debug("Add rule for target '%s'. Supported toolchains: %s" % (target, rule.get_supported_toolchains()))
    return rule

Builder = _Builder()
