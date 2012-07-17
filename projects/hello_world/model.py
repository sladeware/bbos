#!/usr/bin/env python

import bb
from bb.build import packager
from bb.hardware.devices.processors import PropellerP8X32A_Q44

printer = bb.Thread("PRINTER", "do_print")

@packager.pack(printer, "simulator")
class _(packager.Package):
    FILES = ("hello_world.py",)

processor = PropellerP8X32A_Q44()
my_computer = processor

hello_world = bb.Mapping("HELLO_WORLD", processor=my_computer)
hello_world.register_thread(printer)

print_hello_world = bb.Application([hello_world])
