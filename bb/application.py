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

"""This module describes BB application. An application is defined by a BB model
and is comprised of a set of processes running on a particular system topology
to perform work meeting the application's requirements. Each process correnspond
to the appropriate :class:`bb.mapping.Mapping` instance from `mappings`.

It combines all of the build systems of all of the defined processes. Therefore
the application includes the models of processes, their communication, hardware
description, simulation and build specifications. At the same time the processes
inside of an application can be segmented into `clusters`, or a group of CPUs.

The application also controls the hardware or devices that will be managed
by mappings.
"""

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import bb
from bb import networking
from bb.lib.utils import typecheck

_network = networking.Network()

def get_network():
  global _network
  return _network

def get_mappings():
  return get_network().get_nodes()

def get_num_mappings():
  return len(get_mappings())

def is_registered_mapping(mapping):
  if not isinstance(mapping, bb.Mapping):
    raise TypeError("Must be bb.Mapping")
  return get_network().has_node(mapping)

def register_mapping(mapping):
  if is_registered_mapping(mapping):
    return False
  get_network().add_node(mapping)

def register_mappings(mappings):
  if not typecheck.is_list(mappings):
    raise TypeError("Must be list")
  for mapping in mappings:
    register_mapping(mapping)

def get_mapping(name):
  if not typecheck.is_string(name):
    raise TypeError("must be a string")
  # Search for the mapping with specified name in the network
  for mapping in get_mappings():
    if mapping.get_name() == name:
      return mapping
  return None
