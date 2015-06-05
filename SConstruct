import glob
import os

def gen_tangles(min, max, flags):
    for i in range(min, max+1):
        outs = [s.format(i)
                for s in ['tangle{}.idx', 'tangle{}.sobj', 'tree{}.tre']]
        Command(outs,
            '#/gen-tangles.py',  # '#' means WRT SConstruct directory.
            './$SOURCE {} --outdir {} {}'.format(flags, os.getcwd(), i))

def call_sconscript(dir):
    SConscript('{}/SConscript'.format(dir), exports='gen_tangles')

dirs = [
    'rooted-asymmetric',
    'unrooted-asymmetric',
    'rooted-symmetric',
    'unrooted-symmetric']

map(call_sconscript, dirs)
