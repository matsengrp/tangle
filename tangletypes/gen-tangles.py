#!/usr/bin/env sage

import time
from sage.all import *
from collections import Counter
load("../curvature/tree-fun.py")
load("../tangle-fun.py")

for n in (int(a) for a in sys.argv[1:]):
    old_time = time.time()
    trees = enumerate_rooted_trees(n)

    def find_tree(t):
        [t_idx] = filter(lambda i: llt_is_isomorphic(t, trees[i]),
                         range(len(trees)))
        return t_idx

    (map_to_class, _) = equivalence_classes(rooted_is_isomorphic, trees)
    tally = Counter()
    for rep_idx in map_to_class:
        tally[rep_idx] += 1
    isom_count = [tally[map_to_class[i]] for i in range(len(map_to_class))]

    tangles = make_tangles(n, symmetric=True, verbose=False)
    sage.structure.sage_object.save(
        list(saveable_tangle(*x) for x in tangles),
        filename=("tangle"+str(n)))
    with open("tangle"+str(n)+".tre", "w") as f:
        for x in tangles:
            f.write(to_newick_pair(*x)+"\n")
    with open("tangle"+str(n)+".idx", "w") as f:
        for (t1, t2, coset) in tangles:
            t2p = t2.copy()
            t2p.relabel(symmetric_group_dict(t1, t2, representative(coset)))
            t1_idx = find_tree(t1)
            t2p_idx = find_tree(t2p)
            newick_pair_str = "{}\t{}".format(to_newick(t1), to_newick(t2p))
            assert(to_newick_pair(t1, t2, coset) == newick_pair_str)
            f.write("\t".join([str(o) for o in [
                t1_idx,
                t2p_idx,
                newick_pair_str,
                isom_count[t1_idx]
                ]])+"\n")
    print "{}\t{}".format(n, time.time() - old_time)
