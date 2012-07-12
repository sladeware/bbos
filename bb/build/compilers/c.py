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

"""This module provides support for C-like compilers.
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Alexander Sviridenko"

import os
import os.path
import re
import sys
import string
import time
from types import *

from bb.builder.compilers.compiler import Compiler
from bb.builder.errors import *
from bb.utils.host_os.path import mkpath
from bb.utils.spawn import which, ExecutionError
