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

import bb
from bb.app.os import Driver, Message

class ButtonDriver(Driver):

  NAME_FORMAT = 'BUTTON_DRIVER_%d'
  RUNNER = 'button_driver_runner'
  MESSAGE_HANDLERS = {
    Message("IS_BUTTON_PRESSED", [("pin", 1)]): "is_button_pressed",
    Message("ARE_BUTTONS_PRESSED", [("mask", 2)]): "are_buttons_pressed"
  }
