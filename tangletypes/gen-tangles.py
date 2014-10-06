#!/usr/bin/env sage

import time
from sage.all import *
from itertools import product
load("../curvature/tree-fun.py")
load("../tangle-fun.py")


def _mkdir(newdir):
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError
    else:
        os.mkdir(newdir)


for i in range(7, 8):
    old_time = time.time()
    sage.structure.sage_object.save(
        list(saveable_tangle(*x) for x in
            make_tangles(i, symmetric=False, verbose=False)),
        filename=("tangle"+str(i)))
    print "{}\t{}".format(i, time.time() - old_time)
