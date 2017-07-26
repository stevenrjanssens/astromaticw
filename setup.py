#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name='SExtractorW',
	version='0.1.0',
	description='A low-level Source Extractor wrapper',
	author='Steven Janssens',
	url='http://github.com/stevenrjanssens/sextractorw',
	packages=['sextractorw'],
	package_dir={'sextractorw': 'src/sextractorw'},
        package_data={'sextractorw': ['config/*']}
)
