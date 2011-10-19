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
from bb.hardware import Hardware

SIMULATION_MODE = 'SIMULATION'
DEV_MODE = 'DEVELOPMENT'

def get_mode():
    if is_simulation_mode():
        return SIMULATION_MODE
    return DEV_MODE

def is_simulation_mode():
    return 'bb.simulator' in sys.modules

_active_application = None

class Application(object):
    def __init__(self, mappings=[]):
        self.__mappings = {}
        self.__manager = multiprocessing.Manager()
        self.__processes = self.__manager.dict()
        if len(mappings):
            self.add_mappings(mappings)

    @classmethod
    def get_running_instance(class_):
        global _active_application
        return _active_application    

    def add_mappings(self, mappings):
        verify_list(mappings)
        for mapping in mappings:
            self.add_mapping(mapping)

    def add_mapping(self, mapping):
        if not isinstance(mapping, Mapping):
            raise TypeError("Unknown mapping '%s'. "
                            "Not based on bb.app.Mapping class" % (mapping))
        self.__mappings[id(mapping)] = mapping
        return mapping

    def get_num_mappings(self):
        """Return number of mappings defined within current application."""
        return len(self.get_mappings())

    def get_num_processes(self):
        return len(self.__processes.items())

    def get_mappings(self):
        return self.__mappings.values()

    def get_active_mapping(self):
        pid = multiprocessing.current_process().pid
        if not pid in self.__processes:
            raise Exception("Cannot identify %d" % pid)
        return self.__processes[pid]

    def start(self):
        global _active_application
        _active_application = self
        if not self.get_num_mappings():
            raise Exception("Nothing to run. Please, add at least one mapping.")
        workers = []
        for mapping in self.get_mappings():
            if not mapping.os_class:
                raise Exception("Cannot create OS instance.")
            def bootstrapper():
                os = mapping.os_class()
                os.main()
                os.kernel.start()
                return os
            worker = multiprocessing.Process(target=bootstrapper)
            worker.start()
            self.__processes[worker.pid] = mapping
            workers.append(worker)
        try:
            for worker in workers:
                worker.join()
        except KeyboardInterrupt, e:
            # Very important! We need to terminate all the children in order to
            # close all open pipes. Otherwise we will get
            # "IOError: [Errno 32]: Broken pipe". So look up for workers first 
            # and terminate them.
            for worker in multiprocessing.active_children():
                worker.terminate()
        except SystemExit, e:
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
    def __init__(self, name, os_class=None):
        self.name = name
        self.hardware = Hardware()
        self.os_class = os_class


