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
__author__ = "<oleks.sviridenko@gmail.com> Oleksandr Sviridenko"

import time
import random

from bb import OS, Mapping
from bb.hardware.devices.boards import Board

from device import vegimeter_device
if not vegimeter_device:
    print "vegimeter device wasn't defined"
    exit(0)

class UI(OS):
    shmem = None

    def main(self):
        self.shmem = self.kernel.load_module(
            "bb.os.drivers.processors.propeller_p8x32.shmem")
        self.kernel.add_thread(self.kernel.Thread("UI_ID", self.ui_runner))

    def ui_runner(self):
        vegimeter_buttons = int(self.shmem.shmem_read(10, 1)[0])
        if vegimeter_buttons:
            for i in range(8):
                if vegimeter_buttons & 1:
                    print "Button pressed: %d" % i
                vegimeter_buttons >>= 1
        # Zero buttons state
        self.shmem.shmem_write(10, 0)

class ButtonDriver(OS):
    shmem = None # shared memory library

    def main(self):
        self.shmem = self.kernel.load_module(
            "bb.os.drivers.processors.propeller_p8x32.shmem")
        self.kernel.add_thread(self.kernel.Thread("BUTTON_DRIVER",
                                                  self.button_driver_runner))

    def button_driver_runner(self):
        random.seed()
        self.shmem.shmem_write(10, random.randint(1, 8))
        time.sleep(2)

ui = Mapping(name="UI", os_class=UI)
button_driver = Mapping(name="BUTTON_DRIVER", os_class=ButtonDriver)

MAP_COGID_MAPPING = {
    3: ui,
    5: button_driver,
    }

board = vegimeter_device.find_element("QSP1")
if not board:
    print "Board <QSP1> cannot be found!"
    exit(0)
processor = board.find_element("PRCR1")

for cogid, mapping in MAP_COGID_MAPPING.items():
    cog = processor.get_cog(cogid)
    if not cog:
        print "Cannot assign mapping %s to the cog %d" % (mapping, cogid)
        exit(0)
    cog.set_mapping(mapping)
