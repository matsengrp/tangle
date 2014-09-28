from sage.all import *
from itertools import product
load("curvature/tree-fun.py")
load("tangle-fun.py")


def _mkdir(newdir):
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError
    else:
        os.mkdir(newdir)

_mkdir("_tangles")


for i in [4,5]:
    sage.structure.sage_object.save(make_tangles(i), filename=("_tangles/tangle"+str(i)))
