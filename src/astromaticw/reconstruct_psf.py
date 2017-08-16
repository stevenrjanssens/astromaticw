"""reconstruct_psf.py -- creates PSF images at specified location

Usage:
    python psf.py <psffile>...

Notes:
    Run this as a script to inspect PSFs.
"""

from __future__ import print_function
import os
import sys
import numpy
import warnings
from astropy.io import fits
from astropy.utils.exceptions import AstropyWarning

def reconstruct_psf(psffile, x_image, y_image, outfits, overwrite=False):
    """Reconstruct PSF at (x, y) with polynom degree 3 variation in (x, y)."""
    with fits.open(psffile) as hdulist:
        chi2 = hdulist[1].header['CHI2']
        polzero1 = hdulist[1].header['POLZERO1']
        polscal1 = hdulist[1].header['POLSCAL1']
        polzero2 = hdulist[1].header['POLZERO2']
        polscal2 = hdulist[1].header['POLSCAL2']
        psf_fwhm = hdulist[1].header['PSF_FWHM']
        psf_vector = hdulist[1].data[0][0]

    x = (x_image - polzero1) / polscal1
    y = (y_image - polzero2) / polscal2
    xx = x * x
    xxx = x * x * x
    xy = x * y
    xxy = x * x * y
    yy = y * y
    xyy = x * y * y
    yyy = y * y * y

    psf = psf_vector[0] + x*psf_vector[1] + xx*psf_vector[2] +\
            xxx*psf_vector[3] + y*psf_vector[4] + xy*psf_vector[5] +\
            xxy*psf_vector[6] + yy*psf_vector[7] + xyy*psf_vector[8] +\
            yyy*psf_vector[9]

    newhdu = fits.PrimaryHDU(psf)
    newhdu.header.set('PSFEX', psffile, "PSFEx .psf file")
    newhdu.header.set('X_IMAGE', x_image, "X coord of PSF reconstruction")
    newhdu.header.set('Y_IMAGE', y_image, "Y coord of PSF reconstruction")
    newhdu.header.set('CHI2', chi2, "Final Chi2")
    newhdu.header.set('PSF_FWHM', psf_fwhm, "Mean PSF FWHM")
    newhdu.header.add_comment(" Keywords from PSFEx PSF model file", after="Y_IMAGE")
    # ignore comment truncation warning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", AstropyWarning)
        newhdu.writeto(outfits, overwrite=overwrite)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)

    test_coords = ((1667, 4943), (5509, 1881), (8403, 5672), (4367, 9017), (4786, 5089))

    for psffile in sys.argv[1:]:
        for i, coord in enumerate(test_coords):
            outfits = os.path.splitext(os.path.basename(psffile))[0] + '_pos{}.fits'.format(i)
            reconstruct_psf(psffile, coord[0], coord[1], outfits)
