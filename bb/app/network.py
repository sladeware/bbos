#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.utils.type_check import verify_list, verify_int, verify_string
from bb.app.mapping import Mapping, verify_mapping

try:
    import networkx
except ImportError:
    print >>sys.stderr, "Please install networkx library:", \
        "http://networkx.lanl.gov"
    sys.exit(1)

#_______________________________________________________________________________

class _Connection(object):
    """A sending device initiates the transmission of data, instructions, and
    information while a receiving device accepts the items transmitted."""

    def __init__(self, sender, receiver):
        verify_mapping(sender)
        verify_mapping(receiver)

        # XXX: do we need to allow selfloops?
        #if sender is receiver:
        #    raise Exception("Selfloop is not allowed.")

        self.__sender = sender
        self.__sending_device = None
        self.__receiver = receiver
        self.__receiving_device = None

    def get_sender(self):
        return self.__sender

    def set_sending_device(self, dev_name):
        self.__sending_device = dev_name

    def get_receiver(self):
        return self.__receiver

    def set_receiving_device(self, dev_name):
        pass

    def __str__(self):
        return "[%s --> %s]" % (self.get_sender().name, \
                                    self.get_receiver().name)

def verify_connection(connection):
    if not isinstance(connection, Connection):
        raise TypeError("connection must be subclass of Connection: %s" %
                        connection)

#_______________________________________________________________________________

# NOTE: I think it would be nice to provide own edge class in order to get an
# opportunity for more flexible edge manipulations. networkx uses a simple tuple
# for edge representation.
class _Edge(tuple):
    """Since edges are not specified as NetworkX object, this class provides
    simple interface for manipulations with edge."""

    KEY_FORMAT = "EDGE_%d"

    # Because tuples are immutable, we need to override __new__
    def __new__(cls, *args):
        return tuple.__new__(cls, args)

    def __init__(self, *args):
        (self.__sender, self.__receiver) = args[:2]
        self.__key = None
        if len(args) > 2:
            self.__key = args[2]
        self.__data = None
        if len(args) > 3:
            self.__data = args[3]

    def get_sender(self):
        return self.__sender

    def get_receiver(self):
        return self.__receiver

    def get_key(self):
        return self.__key

    def get_data(self):
        return self.__data

    def get_connection(self):
        return self.__data['object']

    def get_label(self):
        return self.__data['label']

    def set_label(self, label):
        # XXX: do we need to verify the label value?
        self.__data['label'] = label

class Network(networkx.MultiDiGraph):
    """The internal graph of static network topology representation used to
    generate routing decision trees at build time. The routing decisions will
    be generated as static control blocks at build time."""

    def __init__(self, nodes=[]):
        networkx.MultiDiGraph.__init__(self)
        # Provide compatibility with BB interface
        self.add_nodes = self.add_nodes_from
        self.remove_nodes = self.remove_nodes_from
        self.get_neighbors = self.neighbors
        self.get_nodes = self.nodes
        self.get_nodes_iter = self.nodes_iter
        self.get_edges = self.edges
        self.get_edges_iter = self.edges_iter
        # Add default nodes if such was defined
        if len(nodes):
            self.add_nodes(nodes)

    def has_node(self, node):
        """Return whether the requested mapping belongs to the application."""
        verify_mapping(node)
        return networkx.MultiDiGraph.has_node(self, node)

    def add_node(self, mapping):
        """Add given node to the graph. Return this node."""
        if not self.has_node(mapping):
            networkx.MultiDiGraph.add_node(self, mapping)
        else:
            raise Exception("Mapping %s already in they graph" % mapping)
        return mapping

    def remove_node(self, node):
        verify_mapping(node)
        networkx.MultiDiGraph.remove_node(self, node)

    def neighbors(self, node):
        verify_mapping(node)
        return networkx.MultiDiGraph.neighbors(node)

    def connection(self, sender, receiver, name):
        """Return Connection instance."""
        verify_string(name)
        if not self.has_edge(sender, receiver, name):
            return None
        data = self.get_edge_data(sender, receiver, key=name)
        return data['object']

    def connect(self, sender, receiver, name=None, attr_dict=None, **attrs):
        """Connect sender and receiver. Return object attribute (Connection
        instance) that handles connection between these mappings.

        See add_edge()."""
        edge = self.add_edge(sender, receiver, name, attr_dict, **attrs)
        return edge.get_connection()

    def get_edge(self, sender, receiver, key):
        if not self.has_edge(sender, receiver, key):
            return None
        data = self.get_edge_data(sender, receiver, key)
        return _Edge(sender, receiver, key, data)

    def add_edge(self, sender, receiver, key=None, attr_dict=None, **attrs):
        """Create an edge between sender and receiver. Return an edge
        represented by _Edge instance which is mainly replacing a tuple
        (sender, receiver, key, attrs).

        key is an optional hashable identifier. By default it has
        _Edge.KEY_FORMAT format. Note, this key has to be unique in order to
        distinguish multiedges between a pair of nodes. At the same time
        edge's label equals to the key.

        By default label equals to the key value but can be changes by using
        associated data as follows:
        >>> add_edge(Mapping("M1"), Mapping("M2"), label="My serial connection")
        Or
        >>> edge = add_edge(Mapping("M1"), Mapping("M2"))
        >>> edge.set_label("My serial connection")

        Note, the nodes for sender and receiver mappings will be automatically
        added if they are not already in the graph."""
        # Setup dictionary of attributes
        if attr_dict is None:
            attr_dict = attrs
        if not self.has_node(sender):
            self.add_node(sender)
        if not self.has_node(receiver):
            self.add_node(receiver)
        # Define hashable identifier
        if not key:
            key_format = attr_dict.get("key_format", None) or _Edge.KEY_FORMAT
            verify_string(key_format)
            key = key_format % len(self.connections((sender, receiver)))
        else:
            verify_string(key)
            if self.connection(sender, receiver, key):
                raise Exception("Connection %s already exists between %s and %s"
                                % (key, sender, receiver))
        connection = _Connection(sender, receiver)
        # Define edge label
        if not attr_dict.get("label", None):
            attr_dict["label"] = key
        else:
            verify_string(attr_dict.get("label"))
        # Use super method
        networkx.MultiDiGraph.add_edge(self, connection.get_sender(),
                                       connection.get_receiver(),
                                       key=key, attr_dict=attr_dict,
                                       object=connection)
        return _Edge(sender, receiver, key,
                     self.get_edge_data(sender, receiver, key=key))

    # XXX: rename!
    def edges_between(self, node1, node2, data=False, keys=False):
        edges = []
        for edge in self.out_edges_iter(node1, data=data, keys=keys):
            if edge[1] is node2:
                edges.append(edge)
        return edges

    # XXX: rename!
    def connections_between(self, node1, node2):
        """Return a list of connections between node1 and node2."""
        connections = []
        for (_, _, data) in self.edges_between(node1, node2, data=True):
            connections.append(data['object'])
        return connections

    def connections(self, nodes=None):
        """Returns the list of connections that are adjacent to any node in
        nodes, or a list of all connections if list of nodes was not
        specified."""
        connections = []
        for _, _, data in self.edges_iter(nbunch=nodes, data=True):
            connections.append(data["object"])
        return connections
