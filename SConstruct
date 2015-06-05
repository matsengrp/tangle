from collections import defaultdict
import envoy
import glob
import os
from SCons.Script import Command, Environment

env = Environment(ENV=os.environ)

def gen_tangles(tangles, min_leaves, max_leaves, flags):
    for i in range(min_leaves, max_leaves+1):
        outs = [s.format(i)
                for s in ['tangle{}.idx', 'tangle{}.sobj', 'tree{}.tre']]
        tangles[i] = Command(outs,
            '#/gen-tangles.py',  # '#' means WRT SConstruct directory.
            './$SOURCE {} --outdir {} {}'.format(flags, os.getcwd(), i))

def check_tangles(tangles, min_leaves, max_leaves, flags):
    for i in range(min_leaves, max_leaves+1):
        Command('tangle{}.check.txt'.format(i),
            ['#/check-tangles.py', tangles[i][1]],  # [1] is the .sobj file
            './${SOURCES[0]} ${SOURCES[1]} '+flags+' > $TARGET')

def count(tangles):
    counts = Command('counts.txt',
        map(lambda x: x[0], tangles.values()),
        'wc -l $SOURCES | head -n -1 | column -t | sed "s/[ ][ ]*/\\t/g" > $TARGET')


def call_sconscript(dir):
    SConscript(
        '{}/SConscript'.format(dir),
        exports='gen_tangles check_tangles count')

dirs = [
    'rooted-asymmetric',
    'unrooted-asymmetric',
    'rooted-symmetric',
    'unrooted-symmetric']

map(call_sconscript, dirs)
