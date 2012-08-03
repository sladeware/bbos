#!/usr/bin/env python

import bb
from bb.hardware.devices.processors import PropellerP8X32A_Q44

hello_world = bb.Mapping("HELLO_WORLD", processor=PropellerP8X32A_Q44())
hello_world.register_thread(bb.Thread("PRINTER", "printer_runner"))
