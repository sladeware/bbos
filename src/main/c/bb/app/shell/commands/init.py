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

from bb import host_os
from bb.app.shell.commands.command import Command

class init(Command):

  USAGE = "%prog init"
  SHORT_DESC = "Initialize new application"
  USES_BASEPATH = False

  def run(self):
    if host_os.path.exists(".bb"):
      print "Application was already initialized"
      exit(0)
    print "Initialize application"
    host_os.mkdir(".bb")
