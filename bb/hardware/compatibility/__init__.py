#!/usr/bin/env python

import getpass

from bb.hardware.compatibility.fritzing import Fritzing

if getpass.getuser() == "d2rk":
    Fritzing.set_home_dir("/opt/fritzing")

vegimeter_device = Fritzing.parse("device.fz")
