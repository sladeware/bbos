#!/usr/bin/env python

import os.path
import getpass

from bb.hardware.compatibility import Fritzing
from bb.utils import module

if getpass.getuser() == "d2rk":
    Fritzing.set_home_dir("/opt/fritzing")
    Fritzing.add_search_path(os.path.join(module.get_dir(), "parts"))

vegimeter_device = Fritzing.parse("device.fz")
