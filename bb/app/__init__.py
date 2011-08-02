#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import types
import threading
import optparse
import sys

from bb.utils.type_check import verify_list

SIMULATION_MODE = 0x1
DEV_MODE = 0x3

MODE = DEV_MODE

def select_mode(new_mode):
    global MODE
    MODE = new_mode

def get_mode():
    global MODE
    return MODE

class Config(object):
    """Class to wrap application-script functionality.

    Attributes:
    parser: An instnace of optparse.OptionParser
    argv: The original command line as a list.
    args: The positional command lie args left over after parsing the options.
    raw_input_fn: Function used for getting raw user input.
    error_fh: Unexpected errors are printer to this file handle.
    """

    def __init__(self, argv, parser_class=optparse.OptionParser,
                 raw_input_fn=raw_input,
                 out_fh=sys.stdout,
                 error_fh=sys.stderr):
        self.argv = argv
        self.parser_class = parser_class
        self.raw_input_fn = raw_input_fn
        self.out_fh = out_fh
        self.error_fh = error_fh
        self.parser = self._get_option_parser()
        self.options, self.args = self.parser.parse_args(argv[1:])
        if self.options.help:
            self._print_help_and_exit()

    def _print_help_and_exit(self, exit_code=2):
        self.parser.print_help()
        sys.exit(exit_code)

    def _get_option_parser(self):
        class Formatter(optparse.IndentedHelpFormatter):
            def format_description(self, description):
                return description, '\n'

        parser = self.parser_class(usage='%prog [Options]',
                                   formatter=Formatter(),
                                   conflict_handler='resolve')
        parser.add_option('-h', '--help', action='store_true',
                          dest='help', help='Show the help message and exit.')
        parser.add_option('-s','--simulation', action='store_true',
                          dest='simulation', help='Run in simulation mode.')
        return parser

config = Config(sys.argv)

if config.options.simulation:
    select_mode(SIMULATION_MODE)

def new_application(*args, **kargs):
    return Application(*args, **kargs)

def new_process(*args, **kargs):
    return Process(*args, **kargs)

class Process:
    def __init__(self, name, kernel=None):
        from bb import os
        self.__name = name
        self.__hardware = os.Hardware()
        self.__kernel = kernel

    def get_hardware(self):
        return self.__hardware

    def select_kernel(self, kernel):
        self.__kernel = kernel
        return kernel

    def get_kernel(self):
        return self.__kernel

    def run(self):
        self.__kernel.start()

class Application:
    def __init__(self):
        self.__processes = {}

    def add_process(self, name):
        process = Process(name)
        self.__processes[name] = process
        return process

    def run(self):
        for (name, process) in self.__processes.items():
            __import__(name)

import bb.app.setup

