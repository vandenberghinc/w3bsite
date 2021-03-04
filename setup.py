#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='w3bsite',
	version='4.13.6',
	description='Some description.',
	url='http://github.com/vandenberghinc/w3bsite',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[
            'syst3m>=2.13.2',
            'cl1>=1.11.8',
            'fil3s>=2.12.8',
            'r3sponse>=2.8.6',
            'netw0rk>=1.7.5',
            'ssht00ls>=3.18.6',
        ])