#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import time

from bb import os
from bb import app
from bb.os.hardware.boards import PropellerDemoBoard

def freefall_runner():
  # freefall is defined as an alternative to static variable in C
  freefall_runner.init_complete = getattr(freefall_runner, 'init_complete', False)
  # Waiting for a messages from h48c device driver
  message = os.get_running_kernel().receive_message('FREEFALL')
  if message and message.get_sender() is h48c.get_name():
    if message.get_command() is h48c.find_command('BBOS_DRIVER_OPEN'):
      print "H48C device has been opened"
      freefall_runner.init_complete = True
      return
    elif message.get_command() is h48c.find_command('H48C_FREEFALL'):
        if message.get_data() == 1:
            print "Free fall detected!"
        elif message.get_data() == 0:
            print "No free fall"
  # Initialization is not complete, send a message to open the driver
  if not freefall_runner.init_complete:
    print "Send open-message to accelerometer device driver"
    os.get_running_kernel().send_message(h48c.get_name(), 
      os.Message('FREEFALL', h48c.find_command('BBOS_DRIVER_OPEN'), None))
  os.get_running_kernel().send_message(h48c.get_name(),
    os.Message('FREEFALL', h48c.find_command('H48C_FREEFALL'), None))
  time.sleep(2)

kernel = os.Kernel()
kernel.set_scheduler(os.StaticScheduler())
kernel.add_thread('FREEFALL', freefall_runner)
h48c = kernel.add_module('bb.os.hardware.drivers.accel.h48c')

accel = app.Process("Accel", kernel)
board = PropellerDemoBoard(processes=[accel])

if app.get_mode() is app.SIMULATION_MODE:
    accel.run()

