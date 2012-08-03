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

from bb import OS, Mapping
from bb.builder.toolchains import propgcc
from bb.os.kernel import Thread
from bb.hardware.devices.boards import Board

from device import vegimeter_device

if not vegimeter_device:
    print "vegimeter device wasn't defined"
    exit(0)

class UI(Thread):
    NAME = "UI"
    RUNNER = "ui_runner"

@propgcc.PropGCCToolchain.pack(UI)
class UICPackage(propgcc.PropGCCToolchain.Package):
    FILES = ('ui.c',)

    def on_unpack(self):
        propgcc.PropGCCToolchain.Package.on_unpack(self)
        compiler = self.get_toolchain().compiler
        compiler.define_macro("BB_CONFIG_OS_H", '"ui_config.h"')
        compiler.add_include_dir(".")

class ButtonDriver(Thread):
    NAME = "BUTTON_DRIVER"
    RUNNER = "button_driver_runner"

@propgcc.PropGCCToolchain.pack(ButtonDriver)
class ButtonDriverPackage(propgcc.PropGCCToolchain.Package):
    FILES = ('button_driver.c',)

    def on_unpack(self):
        propgcc.PropGCCToolchain.Package.on_unpack(self)
        compiler = self.get_toolchain().compiler
        compiler.define_macro("BB_CONFIG_OS_H", '"button_driver_config.h"')
        compiler.add_include_dir(".")

vegimeter = Mapping("Vegimeter")
vegimeter.add_threads([UI(), ButtonDriver()])

board = vegimeter_device.find_element("QSP1")
if not board:
    print "Board <QSP1> cannot be found!"
    exit(0)
processor = board.find_element("PRCR1")
processor.set_mapping(vegimeter)
