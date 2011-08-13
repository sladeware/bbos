#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import types
import threading
import multiprocessing
import inspect
import re
import optparse
import sys

from bb.utils.type_check import verify_list

SIMULATION_MODE = 0x1
DEV_MODE = 0x2

class Config(object):
    """Class to wrap build-script functionality.

    Attributes:
    optparser: An instnace of optparse.OptionParser
    argv: The original command line as a list.
    args: The positional command line args left over after parsing the options.
    raw_input_fn: Function used for getting raw user input.
    error_fh: Unexpected errors are printer to this file handle.
    """

    def __init__(self, optparser_class=optparse.OptionParser,
                 raw_input_fn=raw_input,
                 out_fh=sys.stdout,
                 error_fh=sys.stderr):
        self.argv = None
        self.optparser_class = optparser_class
        self.raw_input_fn = raw_input_fn
        self.out_fh = out_fh
        self.error_fh = error_fh
        self.args = {}
        self.options = optparse.Values()
        self.optparser = self._get_optparser()

    def parse_command_line(self, argv=sys.argv):
        self.options, self.args = self.optparser.parse_args(argv[1:])
        if self.options.help:
            self._print_help_and_exit()

    def get_option(self, name, default=None):
        value = getattr(self.options, name, default)
        return value

    def _print_help_and_exit(self, exit_code=2):
        self.optparser.print_help()
        sys.exit(exit_code)

    def _get_optparser(self):
        class Formatter(optparse.IndentedHelpFormatter):
            def format_description(self, description):
                return description, '\n'
        parser = self.optparser_class(usage='%prog [Options]',
                                      formatter=Formatter(),
                                      conflict_handler='resolve')
        parser.add_option('-h', '--help', action='store_true', dest='help',
                          help='Show the help message and exit.')
        def _select_simulation_mode(option, opt_str, value, parser):
            setattr(parser.values, 'mode', SIMULATION_MODE)
        parser.add_option('-s','--simulation', action='callback',
                          callback=_select_simulation_mode,
                          help='Run in simulation mode.')
        return parser

config = Config()

class Object(object):
    """This class handle application object activity in order to provide
    management of simulation and development modes.

    Just for internal use for each object the global mode value will
    be copied and saved as the special attribute. Thus the object will be
    able to recognise environment's mode in which it was initially started."""

    def __init__(self):
        self.mode = None

    @classmethod
    def sim_method(cls, target):
        def simulation(self, *args, **kargs):
            if not self.mode:
                self.mode = config.get_option('mode')
                if self.mode is SIMULATION_MODE:
                    return target(self, *args, **kargs)
                self.mode = None
            else:
                if self.mode is SIMULATION_MODE:
                    return target(self, *args, **kargs)
        return simulation

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
        tid = multiprocessing.current_process().ident #threading.current_thread().ident
        if not tid in klass.__table:
            return None
        if not the_klass.__name__ in klass.__table[tid]:
            return None
        self, counter = klass.__table[tid][the_klass.__name__][-1]
        return self

    @classmethod
    def __wrap(klass, method):
        def dummy(self, *args, **kargs):
            tid = multiprocessing.current_process().ident #threading.current_thread().ident
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
            # Pass an arguments to the target method and catch return value
            ret = method(self, *args, **kargs)
            self, counter = klass.__table[tid][the_klass.__name__].pop()
            counter -= 1
            if counter:
                klass.__table[tid][the_klass.__name__].append((self, counter))
            return ret
        return dummy

class Mapping(object):
    def __init__(self, kernel=None):
        from bb.os.hardware import Hardware
        self.__hardware = Hardware()
        self.__kernel = None
        if kernel:
            self.set_kernel(kernel)

    def get_hardware(self):
        return self.__hardware

    def set_kernel(self, kernel):
        from bb.os import Kernel
        if not isinstance(kernel, Kernel):
            raise TypeError("Kernel '%s' should based on "
                            "bb.os.kernel.Kernel class." % kernel)
        self.__kernel = kernel
        return kernel

    def get_kernel(self):
        return self.__kernel

    def start(self):
        """Start the kernel."""
        if self.get_kernel():
            self.get_kernel().start()
        else:
            raise Exception("Kernel was not defined.")

    def stop(self):
        pass

class Application(object):
    def __init__(self, processes=[]):
        self.__processes = {}
        if len(processes):
            self.add_processes(processes)

    # Process management

    def add_processes(self, processes):
        for process in processes:
            self.add_process(process)

    def add_process(self, process):
        if not isinstance(process, Mapping):
            raise TypeError("Unknown process '%s'. "
                            "Not based on bb.app.Mapping class" % (process))
        self.__processes[id(process)] = process
        return process

    def get_num_processes(self):
        """Return number of processes defined within current application."""
        return len(self.__processes)

    def get_processes(self):
        return self.__processes

    # Control management

    def start(self):
        if not self.get_num_processes():
            raise Exception("Nothing to run. Please, add at least one process.")
        workers = []
        for (name, process) in self.get_processes().items():
            worker = multiprocessing.Process(target=process.start)
            worker.start()
            workers.append(worker)
        try:
            for worker in workers:
                worker.join()
        except KeyboardInterrupt, SystemExit:
            pass

import bb.app.setup
