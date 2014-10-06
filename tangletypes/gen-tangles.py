#!/usr/bin/env sage

import time
from sage.all import *
from itertools import product
load("../curvature/tree-fun.py")
load("../tangle-fun.py")

for i in (int(a) for a in sys.argv[1:]):
    old_time = time.time()
    sage.structure.sage_object.save(
        list(saveable_tangle(*x) for x in
             make_tangles(i, symmetric=False, verbose=False)),
        filename=("tangle"+str(i)))
    print "{}\t{}".format(i, time.time() - old_time)
