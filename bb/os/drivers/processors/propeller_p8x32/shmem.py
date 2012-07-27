#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.os.kernel import Module, get_running_kernel
from bb.app.application import Application

class shmem(Module):
    processor = None

    def shmem_write(self, addr, src):
        self.processor.RAM.write(addr, src)

    def shmem_read(self, addr, n):
        return self.processor.RAM.read(addr, n)

    def on_load(self):
        self.processor = None
        mapping = Application.get_running_instance().get_active_mapping()
        self.processor = mapping.hardware.get_processor()
        if not self.processor:
            get_running_kernel().panic("Shared memory requires Propeller P8X32 processor")

    def on_unload(self):
        pass

