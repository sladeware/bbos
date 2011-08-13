#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.builder import config
from bb.builder.projects import CatalinaProject

from led_serial import create_receiver

def build():
    project = CatalinaProject("LedSerial", [create_receiver()])
    for filename in ("led_serial.c",):
        project.add_source("./" + filename)
    project.build()

if __name__=='__main__':
    config.parse_command_line()
    build()
