#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='w3bsite',
	version='4.19.9',
	description='Some description.',
	url='http://github.com/vandenberghinc/w3bsite',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[
            'wheel',
            'asgiref',
            'certifi',
            'chardet',
            'Django',
            'idna',
            'requests',
            'sqlparse',
            'urllib3',
            'gunicorn',
            'whitenoise',
            'psutil',
            'uwsgi',
            'gunicorn',
            'whitenoise',
            'django',
            'xmltodict',
            'stripe',
            'syst3m>=2.16.1',
            'cl1>=1.13.1',
            'fil3s>=2.15.4',
            'r3sponse>=2.10.2',
            'netw0rk>=1.8.9',
            'ssht00ls>=3.20.2',
        ])