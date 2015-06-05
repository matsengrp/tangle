import glob
import os

sobj = {}

def gen_tangles(min, max, flags):
    for i in range(min, max+1):
        outs = [s.format(i)
                for s in ['tangle{}.idx', 'tangle{}.sobj', 'tree{}.tre']]
        sobj[i] = Command(outs,
            '#/gen-tangles.py',  # '#' means WRT SConstruct directory.
            './$SOURCE {} --outdir {} {}'.format(flags, os.getcwd(), i))[1]

def check_tangles(min, max, flags):
    for i in range(min, max+1):
        Command('tangle{}.check.txt'.format(i),
            ['#/check-tangles.py', sobj[i]],
            './${SOURCES[0]} ${SOURCES[1]} '+flags+' > $TARGET')

def call_sconscript(dir):
    SConscript('{}/SConscript'.format(dir), exports='gen_tangles check_tangles')

dirs = [
    'rooted-asymmetric',
    'unrooted-asymmetric',
    'rooted-symmetric',
    'unrooted-symmetric']

map(call_sconscript, dirs)
