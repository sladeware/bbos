#!/usr/bin/env python

from bb import builder

builder.rule('bb.hardware.devices.processors.propeller_p8x32.PropellerP8X32A', {
    'PropellerToolchain' : {
      }
})
