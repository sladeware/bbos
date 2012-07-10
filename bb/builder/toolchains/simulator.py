#!/usr/bin/env python

"""Simulation toolchain."""

__author__ = "<oleks.sviridenko@gmail.com> Alexander Sviridenko"
__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.builder import toolchain_manager
from bb.builder.toolchains.toolchain import Toolchain

@toolchain_manager.toolchain
class SimulationToolchain(Toolchain):
    """This toolchain provides simulation support."""
    def build(self, *args, **kargs):
        print "Start simulation"

