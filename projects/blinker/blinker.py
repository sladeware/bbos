#!/usr/bin/env python

import bb
from bb.hardware.devices.boards import P8X32A_QuickStartBoard

blinking_device = P8X32A_QuickStartBoard()
# Note, on P8X32A QuickStartBoard schematic the processor is marked as U1.
blinker = bb.Mapping('Blinker', processor=blinking_device.find_element('U1'))
blinker.register_thread(bb.Thread('BLINKER', 'blinker_runner'))
