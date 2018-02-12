#!/usr/bin/env python
"""pysma library setup."""
from setuptools import setup

setup(name='pysma',
      version='0.2.0',
      description='Library to interface an SMA Solar WebConnect module',
      url='https://github.com/kellerza/pysma',
      download_url='https://github.com/kellerza/pysma/tarball/0.2',
      author='Johann Kellerman',
      author_email='kellerza@gmail.com',
      license='MIT',
      packages=['pysma'],
      install_requires=['aiohttp>2,<3', 'async_timeout>2,<3'],
      zip_safe=True)
