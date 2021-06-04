# pysma library

[![Workflow Status](https://github.com/kellerza/pysma/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/kellerza/pysma/actions)
[![Codecov](https://codecov.io/gh/kellerza/pysma/branch/master/graph/badge.svg)](https://codecov.io/gh/kellerza/pysma)
[![Documentation Status](https://readthedocs.org/projects/pysma/badge/?version=latest)](https://pysma.readthedocs.io/en/latest/?badge=latest)

SMA Webconnect library for Python 3. The library was originally created
to integrate SMA with HomeAssistant

See <http://www.sma-solar.com> for more information on the SMA solar
inverters

Currently tested on Sunnyboy 1.5 and various other Webconnect models, If
you can access your SMA via your browser, this might work for you.

Other SMA interfaces include <https://sbfspot.codeplex.com/> and a
Python [adaptation](https://github.com/TD22057/T-Home/)

# Example usage

See [example.py](./example.py) for a basic usage and tests

# Home Assistant

The Home Assistant sma sensor documentation can be found
[here](https://www.home-assistant.io/components/sma)

By default ssl is disabled (Sunnyboy 1.5 WebConnect uses `http://`). If
you access your SMA WebConnect via `https://` you should set both
`ssl: true` and `verify_ssl: false`.

Daily usage is not always available from the SMA WebConnect interface.
It is possible to get around this by using a
[utility meter](https://www.home-assistant.io/components/utility_meter)
