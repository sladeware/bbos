#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Alexander Sviridenko"

import multiprocessing
import multiprocessing.managers
import inspect
import optparse
import os
import re
import signal
import subprocess
import sys
import threading
import tempfile
import time
import types
import random

from bb.app.mapping import Mapping, verify_mapping
from bb.app.network import Network
from bb.hardware import Device
from bb.utils.type_check import verify_list, verify_int, verify_string

SIMULATION_MODE = 'SIMULATION'
DEV_MODE = 'DEVELOPMENT'

def get_mode():
    if is_simulation_mode():
        return SIMULATION_MODE
    return DEV_MODE

def is_simulation_mode():
    return 'bb.simulator' in sys.modules

class _OutputStream:
    PREFIX_FORMAT = "[%s] "

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        """See number of processes within an application. Do not show process
        identifier if we have less than two processes.
        """
        prefix = ''
        from bb import simulator
        if not simulator.config.get_option("multiterminal"):
            # We do not use here get_num_processes() since we may have an
            # execution delay between processes. Thus we will use max possible
            # number of processes, which is number of mappings.
            if Application.get_running_instance().get_num_mappings() > 1:
                mapping = Application.get_running_instance().get_active_mapping()
                prefix = self.PREFIX_FORMAT % mapping.get_name()
            if data != "\n":
                # Print prefix only if we have some data
                self.stream.write(prefix)
        self.stream.write(data)

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

class _UnbufferedOutputStream(_OutputStream):
    """This class is a subclass of _OutputStream and handles unbuffered output
    stream. It just does flush() after each write().
    """

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        _OutputStream.write(self, data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

class Process(multiprocessing.Process):
    """The process is a one to one mapping, which describes a particular CPU
    core and the particular kernel on it. It represents the life of that kernel:
    from its initialization to the point that it stops executing.

    The process is a subclass of :class:`multiprocessing.Process`.
    """

    def __init__(self, mapping):
        self.__mapping = mapping

        def bootstrapper():
            os_class = mapping.get_os_class()
            os = os_class(**mapping.get_build_params())
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
        """Return :class:`bb.app.application.Process` instance that runs under
        this process.
        """
        return self.__mapping

    def get_pid(self):
        """Return process PID."""
        return self.pid

    def start(self):
        """Start the process."""
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
        """Kill this process. See also :func:`os.kill`."""
        from bb import simulator
        if simulator.config.get_option("multiterminal"):
            self.term.terminate()
            self.fh.close()
            os.remove(self.fname)
            os.rmdir(self.tmpdir)
        os.kill(self.pid, signal.SIGTERM)

class Application(object):
    """This class describes BB application. An application is defined by a BB
    model and is comprised of a set of processes running on a particular system
    topology to perform work meeting the application's requirements. Each
    process correnspond to the appropriate :class:`Mapping` instance from
    `mappings`.

    It combines all of the build systems of all of the defined
    processes. Therefore the application includes the models of processes, their
    communication, hardware description, simulation and build specifications. At
    the same time the processes inside of an application can be segmented into
    `clusters`, or a group of CPUs.

    The application also controls the hardware or devices that will be managed
    by mappings. By default if `devices` were not pass, one will be created and
    marked as active root device. Atherwise the last device in the list will be
    active.
    """

    class Object(object):
        """This class handles application object activity in order to provide
        management of different modes.

        Just for internal use for each object the global mode value will
        be copied and saved as the special attribute. Thus the object will be
        able to recognise environment's mode in which it was initially started.
        """

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
        self.__manager = multiprocessing.Manager()
        # All the processes will be stored at shared dict object. Thus each
        # process will be able to define the mapping by pid.
        #self.__processes = self.__manager.dict()
        self.__processes = list()
        # Initialize device control management
        self.__devices = dict()
        self.__active_device = None
        if not devices:
            devices.append(Device())
        self.add_devices(devices)
        # Register this application instance
        #from bb.app import appmanager
        #appmanager.register_application(self)

    def get_network(self):
        """Return :class:`bb.app.network.Network` instance that represents a
        network of all :class:`bb.app.mapping.Mapping` instances under this
        application.
        """
        return self.__network

    @property
    def network(self):
        return self.get_network()

    def add_mapping(self, mapping):
        """Add :class:`bb.app.mapping.Mapping` instance to the network. Return
        added mapping.
        """
        self.network.add_node(mapping)
        return mapping

    def add_mappings(self, mappings):
        """Add a list of :class:`bb.app.mapping.Mapping` instances to the
        network.
        """
        self.network.add_nodes(mappings)

    def remove_mapping(self, mapping):
        """Remove :class:`bb.app.mapping.Mapping` instance from the network."""
        self.network.remove_node(mapping)

    def get_num_mappings(self):
        """Analyse network and return number of mappings."""
        return len(self.get_mappings())

    def get_mappings(self):
        """Return list of :class:`bb.app.mapping.Mapping` instances that
        belong to this application. This can be also done by analysing
        application network (see also :func:`get_network`).
        """
        return self.network.get_nodes()

    def set_mappings_execution_interval(self, value):
        """Set a new value for mappings execution interval."""
        verify_int(value)
        if value < 0:
            raise Exception('Mappings execution interval value can not be less '
                            'than zero: %d' % value)
        self.__mappings_execution_interval = value

    def get_mappings_execution_interval(self):
        """Return time interval (delay) between mappings execution. See also
        :func:`set_mappings_execution_interval`.
        """
        return self.__mappings_execution_interval

    def get_active_mapping(self):
        """Return currently running :class:`bb.app.mapping.Mapping` instance."""
        process = multiprocessing.current_process()
        #print >>sys.stderr, self.__processes
        #if not process in self.__processes:
        #    raise Exception("Cannot identify %d" % process.pid)
        return process.get_mapping()

    def get_num_processes(self):
        """Return number of running processes."""
        return len(self.__processes)

    @classmethod
    def get_running_instance(klass):
        """Return currently running :class:`Application` instance."""
        return klass.running_instance

    def start(self):
        """Launch the application. Application will randomly execute mappings
        one by one with specified delay (see
        :func:`set_mappings_execution_interval`).

        .. note::

           The only one application can be executed per session.
        """
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
                if not mapping.get_os_class():
                    raise Exception("Cannot create OS instance.")
                process = Process(mapping)
                self.__processes.append(process)
                process.start()
                print "Start process %d" % process.get_pid()
                # Check for delay. Sleep for some time before the
                # next mapping will be executed.
                time.sleep(self.get_mappings_execution_interval())
            # Wait for each process
            for process in self.__processes:
                process.join()
        except KeyboardInterrupt, e:
            self.stop()
        except SystemExit, e:
            self.stop()

    def stop(self):
        """Stop application."""
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

    def add_device(self, device):
        """Add :class:`bb.hardware.devices.device.Device` instance to the list
        of devices controled by this application. Return device instance for
        further work. The device will be marked as `active` device.
        """
        self.__devices[id(device)] = device
        self.set_active_device(device)
        return device

    def set_active_device(self, device):
        """Set device, that is already controled by this application, as active
        device, so all the hardware operations and manipulation will apply to
        this device instance.
        """
        self.__active_device = device

    def add_devices(self, devices):
        """Add a set of devices. See :func:`add_device`."""
        for device in devices:
            self.add_device(device)

    def remove_device(self, device):
        """Return device."""
        del self.__devices[id(device)]

    def get_active_device(self, device):
        """Return active device."""
        return self.__active_device

class Traceable(object):
    """The Traceable interface allows you to track Object activity within an
    application.
    """
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

