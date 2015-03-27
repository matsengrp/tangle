#!/usr/bin/env sage

import argparse
from sage.all import *
load("all-hail-sage/tree-fun.py")
load("tangle-fun.py")

parser = argparse.ArgumentParser(description='Count labeled tangles',
                                 prog='count-ltangles.py')

parser.add_argument('n_max', type=int, help='Max number of leaves')
parser.add_argument('--asymmetric', action='store_true',
                    help='Generate tangles without exchange symmetry.')
parser.add_argument('--verbose', action='store_true')

args = parser.parse_args()

with open("n_ltangles_to_{}.tsv".format(args.n_max), "w") as f:
    for n in range(2, args.n_max+1):
        f.write("\t".join([
            str(n),
            str(count_labeled_tangles(n, not args.asymmetric, args.verbose))]) + "\n")
