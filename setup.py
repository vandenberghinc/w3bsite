#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='w3bsite',
	version='4.21.2',
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
            #'syst3m>=2.16.7',
            #'dev0s>=2.16.4',
            #'netw0rk>=1.9.3',
            #'ssht00ls>=3.20.8',
        ])