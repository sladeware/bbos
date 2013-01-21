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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import logging
import os

import bb
from bb.app.shell.commands.command import Command

def set_verbose_level(option, opt_str, value, parser):
  logger = logging.getLogger()
  logger.setLevel(value * 10)
  logging.basicConfig(format="[%(levelname)s] %(message)s")
  logging.captureWarnings(True)
  setattr(parser.values, option.dest, value)

class build(Command):

  USAGE = '%prog build'
  SHORT_DESC = 'Build an application'
  USES_BASEPATH = False

  def run(self, name=None):
    app = bb.get_app()
    if not app:
      print "Application cannot be identified."
      exit(0)
    if not name:
      (_, name) = os.path.split(app.get_home_dir())
    name = list(os.path.split(name))
    if not name[0]:
      name.pop(0)
    (name[-1], _) = os.path.splitext(name[-1])
    name = ".".join(name)
    try:
      home = __import__("bb.app.home", globals(), locals(), [name], -1)
    except ImportError, e:
      print "Cannot build application."
      print e
      exit(0)
    mod = getattr(home, name)
    app.build()

  def options(self, config, optparser):
    #optparser.add_option('--list-compilers',
    #                     action="callback",
    #                     callback=list_compilers,
    #                     help='List supported compilers.')
    optparser.add_option('--verbose',
                         dest='verbose',
                         type='int',
                         default=0,
                         action="callback",
                         callback=set_verbose_level,
                         help='Verbose level.')
    optparser.add_option("--dry-run",
                         action='store_true',
                         dest="dry_run",
                         help="Show only messages that would be printed in a " \
                           "real run.")
