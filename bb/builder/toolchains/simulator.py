#!/usr/bin/env python

"""Simulation toolchain."""

__author__ = "<oleks.sviridenko@gmail.com> Alexander Sviridenko"
__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.builder.toolchains.toolchain import Toolchain

class SimulationToolchain(Toolchain):
    def build(self):
        pass
