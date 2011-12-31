#!/usr/bin/env python

try:
    import networkx
except ImportError:
    print "Please install network"
    exit(0)

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
