#!/usr/bin/env sage

from sage.all import *
from itertools import product

load("../curvature/tree-fun.py")
load("../tangle-fun.py")


for i in range(4, 5):
    fname = "tangle{}.sobj".format(i)
    print ("Checking "+fname)
    tangles = load_tangles(fname)
    gl = list(graph_of_tangle(*tangle) for tangle in tangles)

    (map_to_class, certs) = equivalence_classes(
        lambda x, y: x.is_isomorphic(y, certify=True, edge_labels=True),
        gl)

    if map_to_class == range(len(map_to_class)):
        print "\tAll tangles are graph-distinct."
    else:
        for j in range(len(map_to_class)):
            if j != map_to_class[j]:
                print "\tIsomorphic tangles:"
                print_tangle(*(tangles[map_to_class[j]]))
                print_tangle(*(tangles[j]))
                print certs[j]

    total_tangles = sum(len(orbit) for (_, _, orbit) in tangles)
    print "There are {} tangles (standardized T_1) with {} leaves.".format(total_tangles, i)
