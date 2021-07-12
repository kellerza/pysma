#!/usr/bin/env python
"""pysma library setup."""
from pathlib import Path

from setuptools import setup

VERSION = "0.6.3"
URL = "https://github.com/kellerza/pysma"

setup(
    name="pysma",
    version=VERSION,
    description="Library to interface an SMA Solar WebConnect module",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url=URL,
    download_url="{}/tarball/{}".format(URL, VERSION),
    author="Johann Kellerman",
    author_email="kellerza@gmail.com",
    license="MIT",
    packages=["pysma"],
    install_requires=["aiohttp>3.3,<4", "attrs>18", "jmespath<2"],
    zip_safe=True,
)
