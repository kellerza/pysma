#!/usr/bin/env python
"""pysma library setup."""
from setuptools import setup

setup(name='pysma',
      version='0.1.3',
      description='Library to interface an SMA Solar WebConnect module',
      url='https://github.com/kellerza/pysma',
      download_url = 'https://github.com/kellerza/pysma/tarball/0.1',
      author='Johann Kellerman',
      author_email='kellerza@gmail.com',
      license='MIT',
      packages=['pysma'],
      install_requires=['aiohttp>=1.1.6,<2', 'async_timeout>=1.1.0,<2'],
      zip_safe=True)
