#!/usr/bin/env python
"""pysma library setup."""

from setuptools import setup

setup(name='pysma',
      version='0.1',
      description='Library to interface an SMA webconnect module',
      url='https://github.com/kellerza/pysma',
      author='Johann Kellerman',
      author_email='kellerza@gmail.com',
      license='MIT',
      packages=['pysma'],
      install_requires=['aiothttp', 'async_timeout'],
      zip_safe=True)
