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

from __future__ import absolute_import

import os as host_os

from bb import config # sorry, bus this goes first
from bb.object import Object
from bb import application
from bb import os
from bb.mapping import Mapping
from bb.cli import CommandLineInterface, CLI

STAGE_INIT_TIME  = 0
STAGE_BUILD_TIME = 1
STAGE_LOAD_TIME  = 2
STAGE_RUN_TIME   = 3

_CURRENT_STAGE = STAGE_INIT_TIME

def get_current_stage():
  return _CURRENT_STAGE

def next_stage():
  global _CURRENT_STAGE
  _CURRENT_STAGE += 1

def is_build_time_stage():
  return get_current_stage() == STAGE_BUILD_TIME

def is_load_time_stage():
  return get_current_stage() == STAGE_LOAD_TIME
