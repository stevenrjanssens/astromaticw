#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name='astromaticW',
	version='0.3.0',
	description='Low-level astromatic wrappers',
	author='Steven Janssens',
	url='http://github.com/stevenrjanssens/astromaticw',
	packages=find_packages('src'),
	package_dir={'': 'src'},
        package_data={'astromaticw': ['config/*']}
)
