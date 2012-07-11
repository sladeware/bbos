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

import bb
#from bb.modeling import networking
from bb.hardware import Device

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

        def __init__(self):
            pass

    def __init__(self, mappings=[], devices=[]):
        self._mappings = list()
        #self._network = networking.Network(mappings)
        self._devices = dict()
        self.register_mappings(mappings)
        if not devices:
            devices.append(Device())
        self.register_devices(devices)

    def get_network(self):
        return self._network

    @property
    def network(self):
        return self.get_network()

    def register_mapping(self, mapping):
        self.network.add_node(mapping)
        return mapping

    def register_mappings(self, mappings):
        verify_list(mappings)
        self.network.add_nodes(mappings)

    def unregister_mapping(self, mapping):
        self.network.remove_node(mapping)

    def get_num_mappings(self):
        return len(self.get_mappings())

    def get_mappings(self):
        return self.network.get_nodes()

    def register_device(self, device):
        self._devices[id(device)] = device
        return device

    def register_devices(self, devices):
        for device in devices:
            self.register_device(device)

    def unregister_device(self, device):
        del self._devices[id(device)]
