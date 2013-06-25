# -*- coding: utf-8; -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC

"""The build command allows you to build your application as follows::

   $ b3 build [:target]

, where ``:target`` is a label name inside your BUILD script.
"""

from __future__ import print_function

import sys
import os
import traceback

import bb.config
from bb.tools.b3.commands.command import Command
from bb.tools.b3 import buildfile
from bb.utils import path_utils
from bb.utils import logging

DEFAULT_TARGET = ":all"

logger = logging.get_logger("bb")

class Build(Command):
  """This class represents build command."""

  def __init__(self, root_dir, parser, argv):
    Command.__init__(self, root_dir, parser, argv)
    if not self.args:
      self.args = [DEFAULT_TARGET]
    self.rules = []
    addresses = []
    # TODO: the following injection has to be fixed
    if os.path.exists(bb.config.user_settings.get("bbos", "homedir")):
      bbos_src = path_utils.join(bb.config.user_settings.get("bbos", "homedir"),
                                 "src", "main")
      bbos_buildfile = buildfile.BuildFile(bbos_src, ".")
      buildfile.Context(bbos_buildfile).parse()
    #
    for target in self.args[0:]:
      try:
        address = buildfile.get_address(root_dir, target)
      except:
        self.error("Problem parsing target %s: %s" %
                   (target, traceback.format_exc()))
      if not address:
        print("Cannot find BUILD file for", target, file=sys.stderr)
        continue
      addresses.append(address)
    for address in addresses:
      try:
        print(buildfile.get_rule(address))
        rule = buildfile.get_rule(address)
      except:
        self.error("Problem parsing BUILD rule %s: %s" %
                   (address, traceback.format_exc()))
      if not rule:
        self.error("Rule %s does not exist" % address)
      self.rules.append(rule)

  def setup_parser(self, parser, args):
    parser.set_usage("\n"
                     "  %prog build (options) [target] (build args)\n"
                     "  %prog build (options) [target]... -- (build args)")
    parser.disable_interspersed_args()
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet",
                      default=False, help="Don't output result of empty rules")
    parser.add_option("--list-rules", action="store_true", dest="list_rules",
                      default=False, help="List existed rules")
    parser.epilog = "Builds the specified rule(s). Currently any additional" \
        "arguments are passed straight through to the ant build" \
        "system."

  def execute(self):
    if self.options.list_rules:
      print("List supported rules:")
      for rule in self.rules:
        print("\t", rule.name)
      return
    for rule in self.rules:
      logger.debug("Execute %s" % rule)
      rule.execute()
