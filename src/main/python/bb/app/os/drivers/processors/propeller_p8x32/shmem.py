# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko

from bb.app.os.drivers.driver import Driver

class ShMemDriver(Driver):

  name_format = 'SHMEM_DRIVER_%d'
  runner = 'shmem_driver_runner'
