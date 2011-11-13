#!/usr/bin/env python

from house_sensing import house_sensing

import networkx

G = house_sensing.network
#networkx.draw_graphviz(G, prog='dot', with_labels=True)
#networkx.write_dot(G, "network.dot")
fh = open("network.png", "w")
fh.write(networkx.to_pydot(G).create(format='png'))
fh.close()
