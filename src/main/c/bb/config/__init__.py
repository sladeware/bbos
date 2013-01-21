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

from django.conf import settings
import sys

import bb
import bb.config.compilers.python.builtins
import bb.config.compilers.python.importer # override standard __import__

# Compatibility with Python 2.5 through 2.7.
assert (2, 5) <= sys.version_info < (3, ), """\
This code is meant for
Python 2.5 through 2.7. You might find that the parts you care about
still work in older Pythons or happen to work in newer ones, but
you're on your own -- edit __init__.py if you want to try it.
"""

# We would like to use Django templates without the rest of Django.
settings.configure()
