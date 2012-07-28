#!/usr/bin/env python

import bb
from bb import application
from bb.hardware.devices.processors import PropellerP8X32A_Q44

printer = bb.Thread("PRINTER", "do_print")

processor = PropellerP8X32A_Q44()
my_computer = processor

hello_world = bb.Mapping("HELLO_WORLD", processor=my_computer)
hello_world.register_thread(printer)

application.register_mapping(hello_world)
