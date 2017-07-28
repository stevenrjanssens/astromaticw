#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name='SExtractorW',
	version='0.1.2',
	description='A low-level Source Extractor wrapper',
	author='Steven Janssens',
	url='http://github.com/stevenrjanssens/sextractorw',
	packages=find_packages('src'),
	package_dir={'': 'src'},
        package_data={'sextractorw': ['config/*']}
)
