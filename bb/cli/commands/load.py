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

import imp
import os
import sys
import traceback
import logging

import bb
from bb.cli.commands.command import Command
from bb.tools import builder
from bb.tools import uploader

class load(Command):
  USAGE = '%prog load'
  SHORT_DESC = 'Load a binary'
  USES_BASEPATH = False

  def function(self):
    builder.build()
    uploader.upload()

  def options(self, config, optparser):
    optparser.add_option('--verbose',
                         dest='verbose',
                         type='int',
                         default=0,
                         help='Verbose level.')
