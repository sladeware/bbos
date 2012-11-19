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

read_temp_msg = bb.os.Message("READ_TEMPERATURE", [("dq_pin", 2)],
                              [("value", 2)])

class DS18B20Driver(bb.os.Driver):

  NAME = "DS18B20_DRIVER"
  RUNNER = "ds18b20_driver_runner"
  MESSAGE_HANDLERS = {
    read_temp_msg: "ds18b20_read_temperature"
  }
