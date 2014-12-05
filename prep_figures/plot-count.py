#!/usr/bin/env python

import ggplot as gg
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
    with open('../rooted-symmetric/tangle{}.idx'.format(i), 'r') as trees:
        n_tangles.append(len(list(trees)))

df = DataFrame({'sizes': sizes, 'n_tangles': n_tangles, 'n_trees': n_trees})

molten = melt(df, id_vars=['sizes'])
print(molten)


theme = gg.theme_seaborn()
theme._rcParams['axes.labelsize'] = 'x-large'
theme._rcParams['legend.fancybox'] = 'False'
theme._rcParams['xtick.labelsize'] = 'x-large'
theme._rcParams['ytick.labelsize'] = 'x-large'
p = gg.ggplot(gg.aes(x='sizes', y='value', color='variable'), data=molten)
p = p + gg.geom_line() + gg.scale_y_log10() + theme

gg.ggsave(p, 'count.svg')
