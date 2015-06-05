#!/usr/bin/env sage

import argparse
from sys import stdout
from sage.all import *
load(os.path.dirname(os.path.realpath(__file__))+'/all-hail-sage/phylogeny.py')
load(os.path.dirname(os.path.realpath(__file__))+'/tangle-fun.py')

parser = argparse.ArgumentParser(description='Generate tangles',
                                 prog='gen-tangles.py')

parser.add_argument('n', type=int, help='How many leaves')
parser.add_argument('--asymmetric', action='store_true',
                    help='Generate tanglegrams without exchange symmetry.')
parser.add_argument('--unrooted', action='store_true',
                    help='Generate unrooted tanglegrams.')

args = parser.parse_args()
n = args.n

rooted = not args.unrooted
symmetric = not args.asymmetric
tangles_extras = make_tangles_extras(n, symmetric=symmetric, rooted=rooted)
tangles = [extra[0] for extra in tangles_extras]
tangle_base = "tangle{}".format(n)
sage.structure.sage_object.save(
    [saveable_tangle(*x) for x in tangles],
    filename=tangle_base)
newick_set = set(to_newick_pair(*x) for x in tangles)
newick_list = list(to_newick_pair(*x) for x in tangles)
assert(len(tangles) == len(newick_set))
with open(tangle_base+".idx", "w") as f:
    print "-"*len(tangles)
    for (x, t1_idx, t2p_idx) in tangles_extras:
        f.write("\t".join([str(o) for o in [
            t1_idx,
            t2p_idx,
            to_newick_pair(*x),
            "".join(str(x[2]).split())  # Cosets with no whitespace.
            ]])+"\n")
        stdout.write("*")
        stdout.flush()
    print ""
# Print an enumeration of trees so we can make sense of the .idx file
trees = enumerate_bifurcating_trees(n, rooted=rooted)
with open("tree{}.tre".format(n), "w") as f:
    for t in trees:
        f.write(t.to_newick() + "\n")
