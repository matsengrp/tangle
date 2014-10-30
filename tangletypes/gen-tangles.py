#!/usr/bin/env sage

from subprocess import check_output
from sys import stdout
from sage.all import *
load("../curvature/tree-fun.py")
load("../tangle-fun.py")

for n in (int(a) for a in sys.argv[1:]):
    tangles_extras = make_tangles_extras(n, symmetric=True, verbose=False)
    tangles = [extra[0] for extra in tangles_extras]
    tangle_base = "tangle{}".format(n)
    sage.structure.sage_object.save(
        [saveable_tangle(*x) for x in tangles],
        filename=tangle_base)
    with open(tangle_base+".tre", "w") as f:
        for x in tangles:
            f.write(to_newick_pair(*x)+"\n")
    dups = check_output("sort "+tangle_base+".tre | uniq -d", shell=True)
    if dups != "":
        print "Duplicates found:"
        print dups
        assert(False)
    with open(tangle_base+".idx", "w") as f:
        print "-"*len(tangles)
        for (x, t1_idx, t2p_idx, isom_count) in tangles_extras:
            f.write("\t".join([str(o) for o in [
                t1_idx,
                t2p_idx,
                to_newick_pair(*x),
                isom_count
                ]])+"\n")
            stdout.write("*")
            stdout.flush()
        print ""
    # Print an enumeration of trees so we can make sense of the .idx file
    trees = enumerate_rooted_trees(n)
    with open("tree{}.tre".format(n), "w") as f:
        for t in trees:
            f.write(to_newick(t) + "\n")
