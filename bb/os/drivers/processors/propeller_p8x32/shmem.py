#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.os.kernel import get_running_kernel
from bb.app.application import Application

processor = None

def shmem_write(addr, src):
    global processor
    processor.RAM.write(addr, src)

def shmem_read(addr, n):
    global processor
    return processor.RAM.read(addr, n)

def on_load():
    global processor
    mapping = Application.get_running_instance().get_active_mapping()
    processor = mapping.hardware.get_processor()
    if not processor:
        get_running_kernel().panic("Shared memory requires Propeller P8X32 processor")

def on_unload():
    pass

