#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

#_______________________________________________________________________________

import types
import threading
import multiprocessing
import subprocess
import inspect
import re
import optparse
import sys
import os
import signal
import tempfile
import time
import random

from bb.app.mapping import Mapping, verify_mapping
from bb.app.network import Network
from bb.hardware import Device
from bb.utils.type_check import verify_list, verify_int, verify_string

#_______________________________________________________________________________

SIMULATION_MODE = 'SIMULATION'
DEV_MODE = 'DEVELOPMENT'

def get_mode():
    if is_simulation_mode():
        return SIMULATION_MODE
    return DEV_MODE

def is_simulation_mode():
    return 'bb.simulator' in sys.modules

#_______________________________________________________________________________

class _OutputStream:
    PREFIX_FORMAT = "[%s] "

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        """See number of processes within an application. Do not show process
        identifier if we have less than two processes."""
        prefix = ''
        from bb import simulator
        if not simulator.config.get_option("multiterminal"):
            # We do not use here get_num_processes() since we may have an
            # execution delay between processes. Thus we will use max possible
            # number of processes, which is number of mappings.
            if Application.get_running_instance().get_num_mappings() > 1:
                mapping = Application.get_running_instance().get_active_mapping()
                prefix = self.PREFIX_FORMAT % mapping.name
            if data != "\n":
                # Print prefix only if we have some data
                self.stream.write(prefix)
        self.stream.write(data)

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

class _UnbufferedOutputStream(_OutputStream):
    """This class is a subclass of _OutputStream and handles unbuffered output
    stream. Just do flush() after each write()."""

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        OutputStream.write(self, data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

#_______________________________________________________________________________

class Process(multiprocessing.Process):
    """The process is a one to one mapping and describes a particular CPU core
    and the particular kernel on it. It represents the life of that kernel:
    from its initialization to the point that it stops executing.

    The process is a subclass of multiprocessing.Process()."""

    def __init__(self, mapping):
        self.__mapping = mapping

        def bootstrapper():
            os = mapping.os_class(**mapping.build_params)
            os.main()
            os.kernel.start()
            return os

        multiprocessing.Process.__init__(self, target=bootstrapper)
        from bb import simulator
        if simulator.config.get_option("multiterminal"):
            self.tmpdir = tempfile.mkdtemp()
            self.fname = os.path.join(self.tmpdir, str(id(self)))
            self.fh = open(self.fname, "w")

    def get_mapping(self):
        return self.__mapping

    def get_pid(self):
        return self.pid

    def start(self):
        from bb import simulator
        # Save a reference to the current stdout
        old_stdout = sys.stdout
        if simulator.config.get_option("multiterminal"):
            # hm, gnome-terminal -x ?
            term_cmd = ["xterm",
                        "-T", "Mapping '%s'" % self.__mapping.name,
                        "-e", "tail",
                        "-f", self.fname]
            self.term = subprocess.Popen(term_cmd)
            sys.stdout = _UnbufferedOutputStream(self.fh)
            # Need a small delay
            time.sleep(1)
        else:
            sys.stdout = _OutputStream(sys.stdout)
        # Now the stdout has been redirected. Call initial start().
        multiprocessing.Process.start(self)
        # Normalize stdout stream
        sys.stdout = old_stdout
        if simulator.config.get_option("multiterminal"):
            print "Redirect %d output to %d terminal" % (self.pid, self.term.pid)

    def kill(self):
        from bb import simulator
        if simulator.config.get_option("multiterminal"):
            self.term.terminate()
            self.fh.close()
            os.remove(self.fname)
            os.rmdir(self.tmpdir)
        os.kill(self.pid, signal.SIGTERM)

#_______________________________________________________________________________

class Application(object):
    """This class describes BB application. Note, the only one application can
    be executed per session."""

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

    # Only one running instance
    running_instance = None

    def __init__(self, mappings=[], mappings_execution_interval=0, devices=[]):
        verify_list(mappings)
        self.__network = Network(mappings)
        self.__mappings_execution_interval = 0
        self.set_mappings_execution_interval(mappings_execution_interval)
        # The manager provides a way to share data between different processes
        # (mappings). A manager is strictly internal object, which controls a
        # server oricess which manages shared objects. Other processes can
        # access the shared objects by using proxies.
        import multiprocessing.managers
        self.__manager = multiprocessing.Manager()
        # All the processes will be stored at shared dict object. Thus each
        # process will be able to define the mapping by pid.
        #self.__processes = self.__manager.dict()
        self.__processes = list()
        # Initialize device control. By default if devices were not pass, one
        # will be created and marked as active. Atherwise the last device in
        # the list will be active.
        if not devices:
            devices.append(Device())
        for device in devices:
            self.add_device(device)
        # Register this application instance
        #from bb.app import appmanager
        #appmanager.register_application(self)

    @property
    def network(self):
        return self.__network

    def add_mapping(self, mapping):
        self.network.add_node(mapping)
        return mapping

    def add_mappings(self, mappings):
        self.network.add_nodes(mappings)

    def remove_mapping(self, mapping):
        self.network.remove_node(mapping)

    def get_num_mappings(self):
        """Analyse network and return number of mappings."""
        return len(self.get_mappings())

    def get_mappings(self):
        return self.network.get_nodes()

    def set_mappings_execution_interval(self, value):
        """Set a new value for mappings execution interval."""
        verify_int(value)
        if value < 0:
            raise Exception("Mappings execution interval value can not be less "
                            "than zero: %d" % value)
        self.__mappings_execution_interval = value

    def get_mappings_execution_interval(self):
        return self.__mappings_execution_interval

    def get_active_mapping(self):
        """Return currently running mapping."""
        process = multiprocessing.current_process()
        #print >>sys.stderr, self.__processes
        #if not process in self.__processes:
        #    raise Exception("Cannot identify %d" % process.pid)
        return process.get_mapping()

    def get_num_processes(self):
        return len(self.__processes)

    @classmethod
    def get_running_instance(klass):
        return klass.running_instance

    def start(self):
        print "Start application"
        Application.running_instance = self
        if not self.get_num_mappings():
            raise Exception("Nothing to run. Please, add at least one mapping "
                            "to this application.")
        # First of all, build an execution order of mappings
        execution_order = range(self.get_num_mappings())
        random.shuffle(execution_order)
        # Execute mappings one by one by using execution order. Track keyboard
        # interrupts and system exit.
        try:
            for i in execution_order:
                # Take a random mapping
                mapping = self.get_mappings()[i]
                if not mapping.os_class:
                    raise Exception("Cannot create OS instance.")
                process = Process(mapping)
                process.start()
                print "Start process %d" % process.get_pid()
                self.__processes.append(process)
                # Do we need some delay? If so, sleep for some time before the
                # next mapping will be executed
                time.sleep(self.get_mappings_execution_interval())
            # Wait for each process
            for process in self.__processes:
                process.join()
        except KeyboardInterrupt, e:
            self.stop()
        except SystemExit, e:
            self.stop()

    def stop(self):
        # Very important! We need to terminate all the children in order to
        # close all open pipes. Otherwise we will get
        # "IOError: [Errno 32]: Broken pipe". So look up for workers first
        # and terminate them.
        print "\nStopping application"
        for process in self.__processes:
            if process.is_alive():
                print "Kill process %d" % process.pid
                process.kill()
        Application.running_instance = None

    ### Device management

    def add_device(self, device):
        pass

    def remove_device(self, device):
        pass

    def get_active_device(self, device):
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

