#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander"

from bbos.kernel.module import Module

class SerialCore(Module):
    def __init__(self, kernel):
        Module.__init__(self, "Standard serial driver")
        
    def get_commands(self):
        return ["SERIAL_SEND_BYTE", "SERIAL_RECEIVE_BYTE"]

