# pysma library

[![Workflow Status](https://github.com/kellerza/pysma/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/kellerza/pysma/actions)
[![Codecov](https://codecov.io/gh/kellerza/pysma/branch/master/graph/badge.svg)](https://codecov.io/gh/kellerza/pysma)
[![Documentation Status](https://readthedocs.org/projects/pysma/badge/?version=latest)](https://pysma.readthedocs.io/en/latest/?badge=latest)

SMA Webconnect library for Python 3. The library was created
to integrate SMA inverters with HomeAssistant

See <http://www.sma-solar.com> for more information on the SMA solar
inverters

Other SMA interfaces include [SBFspot](https://github.com/SBFspot/SBFspot/) and a
Python [adaptation](https://github.com/TD22057/T-Home/)

## Example usage

See [example.py](./example.py) for a basic usage and tests

# Home Assistant

The Home Assistant sma sensor documentation can be found
[here](https://www.home-assistant.io/components/sma)

> ---
>
> **This library uses Webconnect.** ~Modbus~ is not supported
> 
> **If you can access your SMA via your browser, this might work for you.**
>
> ---

If you access your SMA WebConnect via `https://` you should set both
`ssl: true` and `verify_ssl: false`.

Daily usage is not always available from the SMA WebConnect interface.
It is possible to get around this by using a
[utility meter](https://www.home-assistant.io/components/utility_meter)
or more recently from the Energy management feature in Home Assistant

### How to debug this addon

1. Ensure you can access your SMA from your browser

To enable detailed logging in Home Assistant, you can add the following to your configuration

```yaml
logger:
  default: info
  logs:
    homeassistant.components.sma: debug
    pysma: debug
```

## Energy Meter

This library can read the second version of the emnergy meter, there is a seperate Home Assistant OS Addon that could also read older Energy Meters directly. See [Energy Meter](https://github.com/kellerza/hassio-sma-em)
