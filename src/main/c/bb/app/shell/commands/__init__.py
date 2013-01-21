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
__all__ = ["build", "help", "load", "init"]

from bb.app.shell.commands.init import init
from bb.app.shell.commands.build import build
from bb.app.shell.commands.help import help
from bb.app.shell.commands.load import load

DEFAULT_COMMANDS = []

def register_default_commands():
  import sys
  for name in __all__:
    klass = getattr(sys.modules["bb.app.shell.commands"], name, None)
    if not klass:
      raise Exception("command cannot be found")
    cmd = klass()
    DEFAULT_COMMANDS.append(cmd)

register_default_commands()
