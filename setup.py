#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='w3bsite',
	version='4.19.0',
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
            'psycopg2-binary',
            'xmltodict',
            'stripe',
            'syst3m>=2.14.4',
            'cl1>=1.11.9',
            'fil3s>=2.13.0',
            'r3sponse>=2.8.7',
            'netw0rk>=1.7.6',
            'ssht00ls>=3.19.0',
        ])