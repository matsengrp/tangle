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

parser.add_argument('counts', nargs='+',
                    type=str, help='Whitespace-delimited tables.')
parser.add_argument('-o',
                    type=str, help='Where to save plot.')

args = parser.parse_args()

def df_of_counts(path):
    df_in = pd.read_table(path, names=['count', 'path'])
    df = pd.DataFrame()
    df['n_leaves'] = map(lambda s: int(re.sub(r'[^0-9]', '', s)), df_in['path'])
    df[re.sub('-', ' ', re.sub(r'/.*', '', path))] = df_in['count']
    return df

df = pd.DataFrame({'n_leaves' : [2]})
for new_df in map(df_of_counts, args.counts):
    df = df.merge(new_df, how='outer')
df.sort(axis=1, inplace=True)  # Sort columns alphabetically.

mpl.rcParams.update({
    'font.size': 18, 'axes.labelsize': 18,
    'xtick.labelsize':16, 'ytick.labelsize':16,
    'legend.fontsize':16,
    'font.family': 'Lato',
    'font.weight': 600, 'axes.labelweight': 600})

p = df.plot(x='n_leaves', logy=True)
p.grid(b=None)
sns.despine(offset=10)
p.set_xlabel('leaves')
p.set_ylabel('count')
p.figure.savefig(args.o)
