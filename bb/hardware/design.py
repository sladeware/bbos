#!/usr/bin/env python

try:
    import networkx
except ImportError:
    print >>sys.stderr, "Please install networkx library:", \
        "http://networkx.lanl.gov"
    sys.exit(1)

class Network(object):
    g = networkx.DiGraph()

    @classmethod
    def add_node(cls, node):
        cls.g.add_node(node)

    def get_graph(self):
        return g

class Design(object):

    def get_network(cls):
        return Network
