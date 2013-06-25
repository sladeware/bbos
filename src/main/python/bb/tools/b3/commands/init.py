# Copyright (c) 2012-2013 Sladeware LLC
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
#
# Author: Oleksandr Sviridenko

"""The init command allows you to initialize a new application directory, once
this is done you can start create an application. Suppose you would like to
start a new BB application `my_app`::

  $ cd my_app/
  $ b3 init

From this point BB will automatically manage all the object inside of an
:class:`~bb.app.app.Application` instance. Now you can start working on
application and BUILD scripts.
"""

import os

from command import Command

class Init(Command):
  """This class represents init command."""

  def setup_parser(self, parser, args):
    parser.set_usage("\n"
                     "  %prog init\n")
    parser.disable_interspersed_args()
    parser.epilog = "Initialize new BB application"

  def execute(self):
    if os.path.exists(".bbapp"):
      print "Application was already initialized"
      exit(0)
    print "Initialize application"
    os.mkdir(".bbapp")
