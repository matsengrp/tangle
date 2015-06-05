from collections import defaultdict
import glob
import os

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

def call_sconscript(dir):
    SConscript('{}/SConscript'.format(dir), exports='gen_tangles check_tangles')

dirs = [
    'rooted-asymmetric',
    'unrooted-asymmetric',
    'rooted-symmetric',
    'unrooted-symmetric']

map(call_sconscript, dirs)
