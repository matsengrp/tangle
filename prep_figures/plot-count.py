#!/usr/bin/env python

from ggplot import ggplot, ggsave, aes, geom_line, scale_y_log10
from pandas import DataFrame, melt


def n_trees_f(n):
    def aux(k):
        if k > 1:
            return k*aux(k-2)
        else:
            return 1
    return aux(2*n - 3)

sizes = range(3, 9)

n_tangles = []
n_trees = [n_trees_f(i) for i in sizes]

for i in sizes:
    with open('../tangletypes/tangle{}.tre'.format(i), 'r') as trees:
        n_tangles.append(len(list(trees)))

df = DataFrame({'sizes': sizes, 'n_tangles': n_tangles, 'n_trees': n_trees})

molten = melt(df, id_vars=['sizes'])
print(molten)

p = ggplot(aes(x='sizes', y='value', color='variable'), data=molten)
p = p + geom_line() + scale_y_log10()

ggsave(p, "count.svg")
