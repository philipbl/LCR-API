#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

VERSION = 'v0.3.0'
PACKAGE_NAME = 'lcr-api'
HERE = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_URL = ('https://github.com/philipbl/LCR-API/archive/'
                '{}.zip'.format(VERSION))

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

REQUIRES = [
    'requests>=2,<3',
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    license='MIT License',
    download_url=DOWNLOAD_URL,
    author='Philip Lundrigan',
    author_email='philiplundrigan@gmail.com',
    description='An API for the LDS churches Leader and Clerk Resources (LCR),',
    url='https://github.com/philipbl/LCR-API',
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=REQUIRES,
    test_suite='tests',
)
