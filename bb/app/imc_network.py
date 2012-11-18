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
__author__ = "Oleksandr Sviridenko"

import networkx

import bb.application
from bb.utils import typecheck

class Network(networkx.MultiDiGraph):

  class Edge(object):
    """This class represents an edge between two nodes in a graph, where each
    node is represented by :class:`bb.application.mapping.Mapping`. Each edge
    has a direction (from `sender` to `receiver`, or back and forth), plus a set
    of attributes such as label (a text associated with it), etc.

    The edge also describes sending device and receiving device. Sending
    device is device used by `sender` to send the data trough this edge to
    `receiver`.

    A sending device initiates the transmission of data, instructions, and
    information while a receiving device accepts the items transmitted.
    """

    KEY_FORMAT = "EDGE_%d"

    def __init__(self, sender, receiver, attributes={}):
      # TODO: do we need to allow selfloops?
      ##if sender is receiver:
      ##    raise Exception("Selfloop is not allowed.")
      self._sender = sender
      self._receiver = receiver
      self._attributes = attributes

    def get_nodes(self):
      """Return the `sender` and `receiver` nodes that this edge connects."""
      return (self.get_sender(), self.get_receiver())

    def get_sender(self):
      return self.__sender

    def get_sending_device(self):
      """Return sending :class:`bb.hardware.devices.device.Device`."""
      raise NotImplemented()

    def set_sending_device(self, device):
      """Set sending :class:`bb.hardware.devices.device.Device`."""
      raise NotImplemented()

    def verify_sending_device(self, device):
      if not self.get_sender().has_device(device):
        raise Exception("Sender %s does not have %s device." % (sender,
                                                                    device))

    def get_receiver(self):
      return self._receiver

    def get_receiving_device(self):
      """Return receiving :class:`bb.hardware.devices.device.Device`."""
      raise NotImplemented()

    def set_receiving_device(self, device):
      """Set receiving :class:`bb.hardware.devices.device.Device`."""
      raise NotImplemented()

    def verify_receiving_device(self, device):
      if not self.get_receiver().has_device(device):
        raise Exception("Receiver %s does not have %s device." % (receiver,
                                                                      device))

    def get_attributes(self):
      """Return all effective attributes on this edge."""
      return self._attributes

    def get_attribute(self, key, default=None):
      """If attribute does not exist, return default value."""
      return self._attributes.get(key, default)

    def set_attribute(self, key, value):
      self._attributes[key] = value

    def __str__(self):
      return "[%s --> %s]" % (self.get_sender().name, \
                                self.get_receiver().name)

  def __init__(self, nodes=[]):
    if not typecheck.is_list(nodes):
      raise TypeError("nodes must be list")
    networkx.MultiDiGraph.__init__(self)
    if len(nodes):
      self.add_nodes(nodes)

  def has_node(self, node):
    """Return whether the requested mapping belongs to the application."""
    if not isinstance(node, bb.application.Mapping):
      raise TypeError("Has to be bb.application.mapping.Mapping")
    return networkx.MultiDiGraph.has_node(self, node)

  def add_node(self, mapping):
    """Add given node to the graph. Return this node."""
    if not self.has_node(mapping):
      networkx.MultiDiGraph.add_node(self, mapping)
    else:
      raise Exception("Mapping %s already in they graph" % mapping)
    return mapping

  def remove_node(self, node):
    if not isinstance(node, bb.application.Mapping):
      raise TypeError("Must be bb.application.mapping.Mapping")
    networkx.MultiDiGraph.remove_node(self, node)

  def neighbors(self, node):
    if not isinstance(node, bb.application.Mapping):
      raise TypeError("Must be bb.application.mapping.Mapping")
    return networkx.MultiDiGraph.neighbors(node)

  def get_edge(self, sender, receiver, key):
    if not self.has_edge(sender, receiver, key):
      return None
    data = self.get_edge_data(sender, receiver, key)
    return NetworkXEdge(sender, receiver, key, data)

  def add_edge(self, sender, receiver, key=None, attr_dict=None, **attrs):
    """Create an edge between sender and receiver. Return an edge
    represented by :class:`NetworkXEdge` instance which is mainly replacing
    a tuple (sender, receiver, key, attrs).

    `sender` and `receiver` can be represented by a tuple of mapping and
    target communication device.

    `key` is an optional hashable identifier. By default it has
    :const:`NetworkXEdge.KEY_FORMAT` format. Note, this key has to be unique
    in order to distinguish multiedges between a pair of nodes. At the same
    time edge's label equals to the key.

    By default label equals to the key value but can be changes by using
    associated data as follows::

      edge = network.add_edge(Mapping("M1"), Mapping("M2"), label="My serial connection")

    or::

      edge = network.add_edge(Mapping("M1"), Mapping("M2"))
      edge.set_label("My serial connection")

    Note, the nodes for sender and receiver mappings will be automatically
    added if they are not already in the graph.
    """

    # Analyse incomming arguments
    if typecheck.is_tuple(sender):
      (sender, sending_device) = sender
    if typecheck.is_tuple(receiver):
      (receiver, receiving_device) = receiver
    # Setup dictionary of attributes
    if attr_dict is None:
      attr_dict = attrs
    if not self.has_node(sender):
      self.add_node(sender)
    if not self.has_node(receiver):
      self.add_node(receiver)
        # Define hashable identifier
    if not key:
      key_format = attr_dict.get("key_format", None) or \
          NetworkXEdge.KEY_FORMAT
      if not typecheck.is_string(key_format):
        raise TypeError("Has to be string")
      key = key_format % self.number_of_edges(sender, receiver)
    else:
      if not typecheck.is_string(key):
        raise TypeError("Has to be string")
      if self.has_edge(sender, receiver, key):
        raise Exception("Edge %s already exists between %s and %s"
                        % (key, sender, receiver))
    # Define edge label
    if not attr_dict.get("label", None):
      attr_dict["label"] = key
    else:
      if not typecheck.is_string(attr_dict.get("label")):
        raise TypeError("Has to be string")
    # Use super method
    networkx.MultiDiGraph.add_edge(self, sender, receiver,
                                   key=key, attr_dict=attr_dict)
    return NetworkXEdge(sender, receiver, key,
                        self.get_edge_data(sender, receiver, key=key))

  # XXX: rename!
  def edges_between(self, node1, node2, data=False, keys=False):
    edges = []
    for edge in self.out_edges_iter(node1, data=data, keys=keys):
      if edge[1] is node2:
        edges.append(edge)
    return edges

# Create an aliases in order to provide compatibility for Network with
# networkx.MultiDiGraph
Network.add_nodes = networkx.MultiDiGraph.add_nodes_from
Network.remove_nodes = networkx.MultiDiGraph.remove_nodes_from
Network.get_neighbors = networkx.MultiDiGraph.neighbors
Network.get_nodes = networkx.MultiDiGraph.nodes
Network.get_nodes_iter = networkx.MultiDiGraph.nodes_iter
Network.get_edges = networkx.MultiDiGraph.edges
Network.get_edges_iter = networkx.MultiDiGraph.edges_iter
# Aliases
Network.connect = Network.add_edge

class NetworkXEdge(Network.Edge, tuple):
  """Since edges are not specified as NetworkX object, this class provides
  simple interface for manipulations with an edge within NetworkX library.

  NetworkX uses a simple tuple for edge representation.
  """

  # Because tuples are immutable, we need to override __new__
  def __new__(cls, *args):
    return tuple.__new__(cls, args)

  def __init__(self, *args):
    (sender, receiver) = args[:2]
    self._key = None
    if len(args) > 2: self.__key = args[2]
    attributes = {}
    if len(args) > 3: attributes = args[3]
    Network.Edge.__init__(self, sender, receiver, attributes)

  def get_key(self):
    return self._key

  def get_sending_device(self):
    return self.get_attribute('sending_device')

  def set_sending_device(self, device):
    self.set_attribute('sending_device', device)

  def get_receiving_device(self):
    return self.get_attribute('receiving_device')
