#!/usr/bin/env python

import bb.os as bbos


kernel = bbos.Kernel()
kernel.add_module('bb.os.hardware.drivers.serial')
