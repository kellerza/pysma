#!/usr/bin/env python
"""pysma library setup."""
from setuptools import setup

VERSION = '0.3.1'
URL = 'https://github.com/kellerza/pysma'

setup(
    name='pysma',
    version=VERSION,
    description="Library to interface an SMA Solar WebConnect module",
    url=URL,
    download_url="{}/tarball/{}".format(URL, VERSION),
    author='Johann Kellerman',
    author_email='kellerza@gmail.com',
    license='MIT',
    packages=['pysma'],
    install_requires=[
        'aiohttp>3,<4',
        'async_timeout>3,<4',
        'attrs>18',
        'jmespath<2',
    ],
    zip_safe=True,
)
