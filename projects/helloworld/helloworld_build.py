#!/usr/bin/env python

@packager.pack(printer, "simulator")
class _(packager.Package):
    FILES = ("hello_world.py",)
