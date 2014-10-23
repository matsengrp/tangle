#!/bin/sh

# Normalize Newick strings for tangles via nw_order.


for i in $@; do
    sed -e 's/\t/\n/' $i | nw_order - | paste -s -d'\t\n' > $(basename $i .tre).order.tre
done
