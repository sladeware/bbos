#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import types
import threading
import inspect
import re
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

class Traceable(object):
    __table = {}

    def __new__(klass):
        for _, method in inspect.getmembers(klass, inspect.ismethod):
            # Avoid recursion. Do not wrap special methods such as: __new__,
            # __init__, __str__, __repr__, etc.            
            if re.match('^__(.+?)__$', method.__name__):
                continue
            # On this moment we will also avoid classmethod's.
            if method.im_self is not None:
                continue
            setattr(klass, method.__name__, Traceable.__wrap(method))
        return super(Traceable, klass).__new__(klass)

    @classmethod
    def find_running_instance(klass, the_klass):
        tid = threading.current_thread().ident
        if not tid in klass.__table:
            return None
        if not the_klass.__name__ in klass.__table[tid]:
            return None
        self, counter = klass.__table[tid][the_klass.__name__][-1]
        return self

    @classmethod
    def __wrap(klass, method):
        def dummy(self, *args, **kargs):
            tid = threading.current_thread().ident
            the_klass = self.__class__
            # Whether the current thread was registered
            if not tid in klass.__table:
                klass.__table[tid] = {}
            if not the_klass.__name__ in klass.__table[tid]:
                klass.__table[tid][the_klass.__name__] = []
            if not len(klass.__table[tid][the_klass.__name__]):
                klass.__table[tid][the_klass.__name__] = [(self, 1)]
            else:
                last_self, counter = klass.__table[tid][the_klass.__name__].pop()
                if last_self is self:
                    counter += 1
                else:
                    klass.__table[tid][the_klass.__name__].append((last_self, counter))
                    last_self = self
                klass.__table[tid][the_klass.__name__].append((last_self, counter))
            # Pass an arguments to the target method and 
            # catch return value
            ret = method(self, *args, **kargs)
            self, counter = klass.__table[tid][the_klass.__name__].pop()
            counter -= 1
            if counter:
                klass.__table[tid][the_klass.__name__].append((self, counter))
            return ret
        return dummy

class Object(object):
    """This class handle application object activity in order to provide 
    management of simulation and building modes.

    Just for internal use for each object the global mode value will 
    be copied and saved as the special attribute. Thus the object will be 
    able to recognise environment's mode it which it was initially started."""

    def __init__(self):
        self.mode = None

    @classmethod
    def sim_method(cls, target):
        def simulation(self, *args, **kargs):
            if not self.mode:
                self.mode = get_mode()
                if self.mode is SIMULATION_MODE:
                    return target(self, *args, **kargs)
                self.mode = None
            else:
                if self.mode is SIMULATION_MODE:
                    return target(self, *args, **kargs)
        return simulation

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

