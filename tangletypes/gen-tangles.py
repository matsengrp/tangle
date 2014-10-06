#!/usr/bin/env sage

import time
from sage.all import *
from itertools import product
load("../curvature/tree-fun.py")
load("../tangle-fun.py")

for i in (int(a) for a in sys.argv[1:]):
    old_time = time.time()
    tangles = make_tangles(i, symmetric=False, verbose=False)
    sage.structure.sage_object.save(
        list(saveable_tangle(*x) for x in tangles),
        filename=("tangle"+str(i)))
    with open("tangle"+str(i)+".tre", "w") as f:
        for x in tangles:
            f.write(to_newick_pair(*x)+"\n")
    print "{}\t{}".format(i, time.time() - old_time)
