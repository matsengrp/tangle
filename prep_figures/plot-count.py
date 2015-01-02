#!/usr/bin/env python

from pandas import DataFrame
from scipy.special import binom
import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.rcParams['font.size'] = 15


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
        df['naive'] = [binom(n, 2) for n in n_trees]
    else:
        df['naive'] = [n*n for n in n_trees]

    p = df.plot(x='sizes', logy=True)
    p.get_figure().savefig(symmetry+'-count.svg')

plot_count('symmetric', 8)
plot_count('asymmetric', 7)
