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

import time
import random

import bb
from bb.os.drivers.gpio.button_driver import ButtonDriver

from device import vegimeter_device

if not vegimeter_device:
  print "vegimeter device wasn't defined"
  exit(0)

board = None
if vegimeter_device.get_designator() == 'QSP1':
  board = vegimeter_device
else:
  board = vegimeter_device.find_element('QSP1')
if not board:
  print "Board <QSP1> cannot be found!"
  exit(0)

vegimeter = bb.Mapping('Vegimeter', board=board)
#vegimeter.register_thread(bb.os.Thread('UI', 'ui_runner'))
vegimeter.register_thread(bb.os.Thread('BUTTON_DRIVER', 'button_driver_runner'))
vegimeter.register_driver(ButtonDriver())
