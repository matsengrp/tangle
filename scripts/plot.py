#!/usr/bin/env python

import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pandas as pd
import re
import seaborn as sns

sns.set_style('ticks')

parser = argparse.ArgumentParser(
    description='Plot tanglegram enumeration.',
    prog='plot.py')

parser.add_argument('counts',
                    type=str, help='Whitespace-delimited table.')
parser.add_argument('-o',
                    type=str, help='Where to save plot.')

args = parser.parse_args()
assert(os.path.exists(args.counts))

df = pd.read_table(args.counts, names=['count', 'path'])
df['n_leaves'] = map(lambda s: int(re.sub(r'[^0-9]', '', s)), df['path'])

mpl.rcParams.update({
    'font.size': 26, 'axes.labelsize': 26, 'xtick.labelsize':20, 'ytick.labelsize':20,
    'font.family': 'Lato',
    'font.weight': 600, 'axes.labelweight': 600})

p = df.plot(
    x='n_leaves',
    y='count')
p.grid(b=None)
sns.despine(offset=10)
p.set_xlabel('leaves')
p.set_ylabel('count')
p.figure.savefig(args.o)
