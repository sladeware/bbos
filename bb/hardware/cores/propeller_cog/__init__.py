#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""Parallax Propeller processor's cog core.

A "cog" is a CPU contained within the Propeller processor. Cogs are designed
to run independently and concurrently within the same silicon die. They have
their own internal memory, configurable counters, video generators and access
to I/O pins as well as the system clock. All the cogs in the processor share
access to global resources sych as the main RAM/ROM, synchronization resources
and specialized monitoring capabilities to know what the other cogs are doing."""

from bb.hardware import Core

class PropellerCog(Core):
    def __init__(self, mapping=None):
        Core.__init__(self, "Propeller Cog", mapping)

