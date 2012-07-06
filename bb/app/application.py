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
import re
import sys
import types

import bb
from bb.app.mapping import Mapping, verify_mapping
from bb.app.network import Network
from bb.hardware import Device
from bb.utils.type_check import verify_list, verify_int, verify_string

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
            self.__mode = None

        @classmethod
        def simulation_method(cls, target):
            """Mark method as method available only for simulation purposes."""
            def simulate(self, *args, **kargs):
                if not self.__mode:
                    self.__mode = bb.get_mode()
                    if self.__mode is bb.SIMULATION_MODE:
                        return target(self, *args, **kargs)
                    self.__mode = None
                else:
                    if self.__mode == bb.SIMULATION_MODE:
                        return target(self, *args, **kargs)
            return simulate

    # Only one running instance is allowed
    running_instance = None

    def __init__(self, mappings=[], mappings_execution_interval=0, devices=[]):
        self.__mappings = list()
        self.__network = Network(mappings)
        self.__mappings_execution_interval = 0
        self.__devices = dict()
        self.__active_device = None
        # The manager provides a way to share data between different processes
        # (mappings). A manager is strictly internal object, which controls a
        # server oricess which manages shared objects. Other processes can
        # access the shared objects by using proxies.
        self.__manager = multiprocessing.Manager()
        # All the processes will be stored at shared dict object. Thus each
        # process will be able to define the mapping by pid.
        #self.__processes = self.__manager.dict()
        self.__processes = list()
        # Initialization
        self.add_mappings(mappings)
        self.set_mappings_execution_interval(mappings_execution_interval)
        # Initialize device control management
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
        verify_list(mappings)
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

