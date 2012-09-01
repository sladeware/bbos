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
__author__ = 'Oleksandr Sviridenko'

import logging

import bb
from bb.cli.command_line_interface import CLI
from bb.cli.commands.command import Command
from bb.tools import builder

BUILD_SCRIPT_FILENAME = 'build.py'

def set_verbose_level(option, opt_str, value, parser):
  logger = logging.getLogger()
  logger.setLevel(value * 10)
  setattr(parser.values, option.dest, value)

class build(Command):
  USAGE = '%prog build'
  SHORT_DESC = 'Build an application'
  USES_BASEPATH = False

  def function(self):
    builder.build()

  def options(self, config, optparser):
    optparser.add_option('--list-toolchains',
                         dest='list_toolchains',
                         action='store_true',
                         help='List supported toolchains.')
    optparser.add_option('--verbose',
                         dest='verbose',
                         type='int',
                         default=0,
                         action="callback",
                         callback=set_verbose_level,
                         help='Verbose level.')
    optparser.add_option('--dry-run',
                         action='store_true',
                         dest='dry_run',
                         help='Show only messages that would be printed in a ' \
                           'real run.')
