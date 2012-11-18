#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.os.drivers.driver import Driver

class ShMemDriver(Driver):
  NAME = 'SHMEM_DRIVER'
  RUNNER = 'shmem_driver_runner'
