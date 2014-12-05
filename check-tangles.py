#!/usr/bin/env sage

import os
from sage.all import *
from itertools import combinations

load("all-hail-sage/tree-fun.py")
load("tangle-fun.py")


print "leaves\tclasses\ttotal"

for i in range(3, 8):
    fname = "rooted-symmetric/tangle{}.sobj".format(i)
    if not os.path.exists(fname):
        print "Skipping", fname
        continue
    tangles = load_tangles(fname)
    # Note that these are _symmetric_ tangles.
    graphs = list(graph_of_tangle(*tangle) for tangle in tangles)
    dirty = False

    for (x1, g1), (x2, g2) in combinations(zip(tangles, graphs), 2):
        # edge_labels=True ensure that leaves map to leaves
        if g1.is_isomorphic(g2, edge_labels=True):
                dirty = True
                print "\tIsomorphic tangles:"
                print_tangle(*x1)
                print_tangle(*x2)

    total_tangles = sum(size(c) for (_, _, c) in tangles)
    print "{}\t{}\t{}".format(i, len(tangles), total_tangles)

if not dirty:
    print "\nAll tangles are graph-distinct."
