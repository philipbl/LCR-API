#!/usr/bin/env python3
import os
from setuptools import setup, find_packages
from lcr import __version__

PACKAGE_NAME = 'lcr'
HERE = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_URL = ('https://github.com/philipbl/LCR-API/archive/'
                '{}.zip'.format(__version__))

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

REQUIRES = [
    'requests>=2,<3',
]

setup(
    name=PACKAGE_NAME,
    version=__version__,
    license='MIT License',
    download_url=DOWNLOAD_URL,
    author='Philip Lundrigan',
    author_email='philiplundrigan@gmail.com',
    description='API for LCR',
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=REQUIRES,
    test_suite='tests',
)
