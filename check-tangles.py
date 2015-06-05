#!/usr/bin/env sage

import argparse
from itertools import combinations
import os
import sys
from sage.all import *

load(os.path.dirname(os.path.realpath(__file__))+'/all-hail-sage/phylogeny.py')
load(os.path.dirname(os.path.realpath(__file__))+'/tangle-fun.py')

parser = argparse.ArgumentParser(description='Checks to make sure that tangles are graph-distinct',
                                 prog='check-tangles.py')

parser.add_argument('sobj_path')
parser.add_argument('--asymmetric', action='store_true',
                    help='Check tangles without exchange symmetry.')
parser.add_argument('--unrooted', action='store_true',
                    help='Check unrooted tangles.')
args = parser.parse_args()

assert(os.path.exists(args.sobj_path))
tangles = load_tangles(args.sobj_path)
graphs = [graph_of_tangle(*tangle, symmetric=(not args.asymmetric))
          for tangle in tangles]
dirty = False

for (x1, g1), (x2, g2) in combinations(zip(tangles, graphs), 2):
    # edge_labels=True ensure that leaves map to leaves
    if g1.is_isomorphic(g2, edge_labels=True):
            dirty = True
            print "\tIsomorphic tangles:"
            print_tangle(*x1)
            print_tangle(*x2)

if dirty:
    sys.exit(1)

total_tangles = sum(size(c) for (_, _, c) in tangles)
print "Tangles in {} are graph-distinct: {} tangles with total count {}."\
    .format(args.sobj_path, len(tangles), total_tangles)

