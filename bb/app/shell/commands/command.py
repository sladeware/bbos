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

class Command(object):

  USAGE = None
  SHORT_DESC = None
  LONG_DESC = ''
  ERROR_DESC = None
  USES_BASEPATH = True
  HIDDEN = False

  def __init__(self):
    self.usage = self.USAGE
    self.short_desc = self.SHORT_DESC
    self.long_desc = self.LONG_DESC
    self.error_desc = self.ERROR_DESC
    self.uses_basepath = self.USES_BASEPATH
    self.hidden = self.HIDDEN

  def __call__(self, *args, **kwargs):
    return self.run(*args, **kwargs)

  def options(self, config, optparser):
    pass

  def run(self):
    raise NotImplementedError()

  def get_descriptions(self):
    """Returns a formatted string containing the short_descs for all commands.
    """
    command_names = klass.action_register.keys()
    action_names.sort()
    desc = ''
    for action_name in action_names:
      if not klass.action_register[action_name].hidden:
        desc += '  %s: %s\n' % (action_name,
                                klass.action_register[action_name].short_desc)
    return desc
