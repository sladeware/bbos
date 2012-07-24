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

from bb.lib.utils import typecheck

class Thread(object):
    """The thread is an atomic unit action within the BB operating system, which
    describes application specific actions wrapped into a single context of
    execution.
    """

    NAME = None
    RUNNER = None

    def __init__(self, name=None, runner=None):
        self._name = None
        self._runner = None
        # Initialize thread name
        if name:
            self.set_name(name)
        elif hasattr(self, "NAME"):
            self.set_name(getattr(self, "NAME"))
        else:
            raise Exception("Name wasn't provided")
        # Initialize thread runner
        if runner:
            self.set_runner(runner)
        elif hasattr(self, "RUNNER"):
            self._runner = self.RUNNER
        else:
            raise Exception("Runner wasn't provided")

    def set_runner(self, runner):
        if not typecheck.is_string(runner):
            raise TypeError("Must be string")
        self._runner = runner

    def get_runner(self):
        return self._runner

    def set_name(self, name):
        if not typecheck.is_string(name):
            raise TypeError("Must be string")
        self._name = name

    def get_name(self):
        return self._name

    def __str__(self):
        return "Thread:%s[%s]" % (self.get_name(), self.get_runner())
