#!/usr/bin/env python

"""This module provides support for BSTL loader. BSTL is the command
line loader which can be found here
http://www.fnarfbargle.com/bst.html

This little application simply allows to load pre-compiled ``.binary``
and ``.eeprom`` files into your propeller. It is a command line
application that takes optional parameters and a file name."""

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.utils.spawn import spawn
from bb.builder.errors import *
from bb.builder.loaders import Loader

class BSTLLoader(Loader):
    """This class represents BSTL loader.

    By default `device_filename` is ``None``, which forces BSTL to use
    ``/dev/ttyUSB0`` device. You can change device manually later by
    using :func:`BSTLLoader.set_device_filename`.
    """

    executables = {
        'loader' : ['bstl']
        }

    class Modes:
        """This class contains available program modes:

        ===================  =====
        Mode                 Value
        ===================  =====
        RAM_ONLY             1
        EEPROM_AND_SHUTDOWN  2
        EEPROM_AND_RUN       3
        ===================  ====="""
        RAM_ONLY            = 1
        EEPROM_AND_SHUTDOWN = 2
        EEPROM_AND_RUN      = 3

    DEFAULT_MODE = Modes.RAM_ONLY
    """Represents default loader mode, which is
    :const:`BSTLLoader.Modes.RAM_ONLY`."""

    def __init__(self, verbose=False,
                 device_filename=None,
                 mode=None):
        Loader.__init__(self, verbose)
        self.__mode = mode or self.DEFAULT_MODE
        self.__device_filename = device_filename

    def set_mode(self, mode):
        """Set program mode. See :class:`BSTLLoader.Modes`."""
        self.__mode = mode

    def get_mode(self):
        """Return current program mode."""
        return self.__mode

    def set_device_filename(self, filename):
        """Set serial device to use."""
        self.__device_filename = filename

    def get_device_filename(self):
        """Return device filename to use."""
        return self.__device_filename

    def _load(self, filename, device_filename=None, program_mode=1):
        loader = self.executables['loader']
        flags = []
        if device_filename:
            self.set_device_filename(device_filename)
        # Add device flag
        if self.get_device_filename():
            flags.extend(['-d', self.get_device_filename()])
        # Add mode flag
        flags.extend(['-p', self.get_mode()])
        # Spawn!
        try:
            spawn(loader + flags + [filename],
                  verbose=self.verbose)
        except BuilderExecutionError, msg:
            raise LoaderError, msg
