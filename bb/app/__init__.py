#!/usr/bin/env python

"""An BB application is defined using one BB's core application component. This
application component is Mapping."""

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import types
import threading
import multiprocessing
import inspect
import re
import optparse
import sys

from bb.utils.type_check import verify_list

SIMULATION_MODE = 'SIMULATION'
DEV_MODE = 'DEVELOPMENT'

def get_mode():
    if is_simulation_mode():
        return SIMULATION_MODE
    return DEV_MODE

def is_simulation_mode():
    return 'bb.simulator' in sys.modules

class Application:
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
            print ">>>", worker.ident
            worker = multiprocessing.Process(target=process.start)
            worker.start()
            workers.append(worker)
        try:
            for worker in workers:
                worker.join()
        except KeyboardInterrupt, SystemExit:
            pass

class Traceable(object):
    """The Traceable interface allows you to track Object activity within an
    application."""
    __table = {}

    def __new__(klass, *args, **kargs):
        for _, method in inspect.getmembers(klass, inspect.ismethod):
            # Avoid recursion. Do not wrap special methods such as: __new__,
            # __init__, __str__, __repr__, etc.
            if re.match('^__(.+?)__$', method.__name__):
                continue
            # On this moment we will also avoid classmethod's.
            if method.im_self is not None:
                continue
            setattr(klass, method.__name__, Traceable.__wrap(method))
        return super(Traceable, klass).__new__(klass, *args, **kargs)

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

class Context:
    def __init__(self):
        self.__context = {}

    def add(self, name, obj):
        self.__context[name] = obj
        return obj

    def find(self, name):
        return self.__context[name]
        
    def remove(self, name):
        obj = self.__context[name]
        del self.__context[name]
        return obj

class Object(object):
    """This class handles application object activity in order to provide
    management of simulation and development modes.

    Just for internal use for each object the global mode value will
    be copied and saved as the special attribute. Thus the object will be
    able to recognise environment's mode in which it was initially started."""

    def __init__(self):
        self.mode = None

    @classmethod
    def simulation_method(cls, target):
        """Mark method as method only for simulation purposes."""
        def simulate(self, *args, **kargs):
            if not self.mode:
                self.mode = get_mode()
                if self.mode is SIMULATION_MODE:
                    return target(self, *args, **kargs)
                self.mode = None
            else:
                if self.mode == SIMULATION_MODE:
                    return target(self, *args, **kargs)
        return simulate

class Mapping(object):
    def __init__(self, kernel=None):
        from bb.os.hardware import Hardware
        self.hardware = Hardware()
        self.kernel = None
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

import bb.app.setup

