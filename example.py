#!/usr/bin/env python
"""Basic usage example and testing of pysma."""
# from time import sleep
import asyncio
import logging
import sys
import argparse

import aiohttp

import pysma

# This module will work with Python 3.4+
# Python 3.4+ "@asyncio.coroutine" decorator
# Python 3.5+ uses "async def f()" syntax

_LOGGER = logging.getLogger(__name__)

args = None


@asyncio.coroutine
def main(loop, password, ip):
    """Main loop."""
    session = aiohttp.ClientSession(loop=loop)
    sma = pysma.SMA(session, ip, password=password,
                    group=pysma.GROUP_INSTALLER)
    yield from sma.new_session()
    _LOGGER.info("NEW SID: %s", sma._sma_sid)

    while loop.jk_run:
        res = yield from sma.read([pysma.KEY_CURRENT_CONSUMPTION_W,
                                   pysma.KEY_CURRENT_POWER_W])
        _LOGGER.info(res)
        yield from asyncio.sleep(1)

    yield from sma.close_session()
    yield from session.close()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    parser = argparse.ArgumentParser(
        description='Test the SMA webconnect library.')
    parser.add_argument(
        'ip', type=str, help='IP address of the Webconnect module')
    parser.add_argument(
        'password', help='Installer password')

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    try:
        setattr(loop, "jk_run", True)
        loop.run_until_complete(main(loop, password=args.password, ip=args.ip))
    except KeyboardInterrupt:
        setattr(loop, "jk_run", False)
        loop.run_forever()
        _LOGGER.info('Done (Ctrl-C)')
