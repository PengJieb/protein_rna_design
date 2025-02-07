#!/usr/bin/env python2

import gflags as flags
import subprocess
import sys
import os

FLAGS = flags.FLAGS

def setgflags():
    flags.DEFINE_float('lambda', 0.0, "set lambda", short_name='l')
    flags.DEFINE_boolean('verbose', False, "print out more details", short_name='v')
    flags.DEFINE_string('codonusage', 'codon_usage_freq_table_human.csv', "import a Codon Usage Frequency Table", short_name='c')
    argv = FLAGS(sys.argv)

def main():

    lambda_ = str(FLAGS.l)
    verbose_ = '1' if FLAGS.verbose else '0'
    codon_usage = str(FLAGS.codonusage)

    path = os.path.dirname(os.path.abspath(__file__))
    cmd = ["%s/%s" % (path, ('bin/LinearDesign_2D_debug')), lambda_, verbose_, codon_usage]
    subprocess.call(cmd, stdin=sys.stdin)
    
if __name__ == '__main__':
    setgflags()
    main()

