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

import bb
from bb import networking
from bb.lib.utils import typecheck

class Application(object):
    def __init__(self, mappings=[]):
        self._network = networking.Network()
        if mappings:
            self.register_mappings(mappings)

    @property
    def network(self):
        return self.get_network()

    def get_network(self):
        return self._network

    def register_mappings(self, mappings):
        if not typecheck.is_list(mappings):
            raise TypeError("Must be list")
        for mapping in mappings:
            self.register_mapping(mapping)

    def get_mappings(self):
        return self.network.get_nodes()

    def get_num_mappings(self):
        return len(self.get_mappings())

    def is_registered_mapping(self, mapping):
        if not isinstance(mapping, bb.Mapping):
            raise TypeError("Must be bb.Mapping")
        return self.network.has_node(mapping)

    def register_mapping(self, mapping):
        if self.is_registered_mapping(mapping):
            return False
        self.network.add_node(mapping)
