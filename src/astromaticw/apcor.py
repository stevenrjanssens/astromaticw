"""apcor.py -- aperture corrections on PSFEx PSFs"""

from __future__ import print_function
import os
import re
import numpy
from photutils import CircularAperture, aperture_photometry

from . import reconstruct_psf

# Sirianni et al. (2005) aperture correction from 1" diameter to infinity
sirianni05_apcor = 0.087

def apcor(xi, yi, psffile, diameter, pixel_scale):
    """
    Aperture correct to an infinite aperture.

    Arguments:
    xi -- pixel coord
    yi -- pixel coord
    psffile -- psfex output
    diameter -- aperture diameter to correct from (in pixels), must be <1"
    pixel_scale -- arcsec per pixel
    
    Notes:
    Corrects to 1" diameter pixel, then applies the Sirianni correction to infinity.
    """
    assert numpy.isscalar(xi) == numpy.isscalar(yi)
    if numpy.isscalar(xi):
        xx = [xi]
        yy = [yi]
    else:
        xx = xi
        yy = yi
    assert len(xx) == len(yy)

    model_EE = []

    for x, y in zip(xx, yy):
        model_psf = reconstruct_psf(psffile, x, y)

        # correct to 1" diameter aperture
        x0, y0 = numpy.unravel_index(numpy.argmax(model_psf, axis=None), model_psf.shape)
        model_apertures = [CircularAperture((x0, y0), r=r) for r in (diameter/2., 0.5/pixel_scale)]
        model_phot_table = aperture_photometry(model_psf, model_apertures)
        EE = model_phot_table[0]['aperture_sum_0'] / model_phot_table[0]['aperture_sum_1']
        model_EE.append(EE)

    model_EE = numpy.array(model_EE)
    apcor = -2.5*numpy.log10(model_EE) + sirianni05_apcor

    if numpy.isscalar(xi):
        return apcor[0]
    else:
        return apcor
