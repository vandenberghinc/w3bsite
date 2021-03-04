#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='w3bsite',
	version='4.13.1',
	description='Some description.',
	url='http://github.com/vandenberghinc/w3bsite',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[
            'syst3m>=2.13.1',
            'cl1>=1.11.7',
            'fil3s>=2.12.7',
            'r3sponse>=2.8.5',
            'netw0rk>=1.7.4',
            'ssht00ls>=3.18.4',
        ])