#!/usr/bin/env sage

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


for i in range(4, 6):
    sage.structure.sage_object.save(
        list(saveable_tangle(*x) for x in make_tangles(i, symmetric=False)),
        filename=("tangle"+str(i)))
