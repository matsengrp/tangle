#!/usr/bin/env python

import ggplot as gg
from pandas import DataFrame, melt
import scipy

def n_trees_f(n):
    def aux(k):
        if k > 1:
            return k*aux(k-2)
        else:
            return 1
    return aux(2*n - 3)


def plot_count(symmetry, max_size):
    sizes = range(3, max_size+1)
    n_trees = [n_trees_f(i) for i in sizes]
    n_tangles = []

    for i in sizes:
        with open('../rooted-{0}/tangle{1}.idx'.format(symmetry, i), 'r') as trees:
            n_tangles.append(len(list(trees)))

    df = DataFrame(
        {'sizes': sizes, 'n_tangles': n_tangles, 'n_trees': n_trees})

    if symmetry == 'symmetric':
        df['naive'] = [scipy.special.binom(n, 2) for n in n_trees]
    else:
        df['naive'] = [n*n for n in n_trees]

    molten = melt(df, id_vars=['sizes'])
    print(molten)

    theme = gg.theme_seaborn()
    theme._rcParams['font.size'] = 16
    theme._rcParams['axes.labelsize'] = 'x-large'
    theme._rcParams['legend.fancybox'] = 'False'
    theme._rcParams['xtick.labelsize'] = 'x-large'
    theme._rcParams['ytick.labelsize'] = 'x-large'
    p = gg.ggplot(gg.aes(x='sizes', y='value', color='variable'), data=molten)
    p = p + gg.geom_line() + gg.scale_y_log10() + theme

    gg.ggsave(p, symmetry+'-count.svg')

plot_count('symmetric', 8)
plot_count('asymmetric', 7)
