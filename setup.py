#!/usr/bin/env python

from distutils.core import setup

setup(
	name='SExtractorW',
	version='0.1.0',
	description='A low-level Source Extractor wrapper',
	author='Steven Janssens',
	url='http://github.com/stevenrjanssens/SExtractorW',
	packages=['sextractorw'],
	package_dir={'sextractorw': 'src/SExtractorW'},
        package_data={'sextractorw': ['config/*']}
)
