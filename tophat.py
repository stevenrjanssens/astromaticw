#!/usr/bin/env python

"""tophat.py -- create a SExtractor tophat filter of specified diameter

Usage:
    tophat.py [options] <diameter>

"""

from __future__ import print_function
import docopt
import numpy
from photutils.geometry import circular_overlap_grid

def tophat(diameter):
    """Create a tophat filter of specified diameter"""
    size = numpy.ceil(diameter)
    if size % 2 == 0:
        size += 1
    if size < 3:
        size = 3
    tophatfilter = circular_overlap_grid(-1, 1, -1, 1, size, size, r=float(diameter)/size, use_exact=0, subpixels=10)
    print('CONV NORM')
    print('# {:1.0f}x{:1.0f} convolution mask of a top-hat PSF with diameter = {:3.1f} pixels.'.format(size, size, diameter))
    for row in tophatfilter:
        print(' '.join(['{:8.6f}'.format(val) for val in row]))

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    tophat(float(arguments['<diameter>']))
