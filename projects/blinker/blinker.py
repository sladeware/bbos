#!/usr/bin/env python

import bb
from bb.hardware.devices.boards import P8X32A_QuickStartBoard

blinking_device = P8X32A_QuickStartBoard()
# Note, on P8X32A QuickStartBoard schematic the processor is marked as U1.
blinker = bb.Mapping('Blinker', board=blinking_device)
blinker.register_threads([bb.os.Thread('B0', 'b0_runner'),
                          bb.os.Thread('B1', 'b1_runner')])
