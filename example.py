#!/usr/bin/env python
"""Basic usage example and testing of pysma."""
import argparse
import asyncio
import logging
import signal
import sys

import aiohttp

import pysma

# This module will work with Python 3.5+
# Python 3.4+ "@asyncio.coroutine" decorator
# Python 3.5+ uses "async def f()" syntax

_LOGGER = logging.getLogger(__name__)

VAR = {}


def print_table(sensors):
    """Print sensors formatted as table."""
    for sen in sensors:
        if sen.value is None:
            print("{:>25}".format(sen.name))
        else:
            print("{:>25}{:>15} {}".format(sen.name, str(sen.value), sen.unit))


async def main_loop(loop, password, user, url):
    """Run main loop."""
    async with aiohttp.ClientSession(
        loop=loop, connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        VAR["sma"] = pysma.SMA(session, url, password=password, group=user)

        try:
            await VAR["sma"].new_session()
        except pysma.exceptions.SmaAuthenticationException:
            _LOGGER.warning("Authentication failed!")
            return
        except pysma.exceptions.SmaConnectionException:
            _LOGGER.warning("Unable to connect to device at %s", url)
            return

        # We should not get any exceptions, but if we do we will close the session.
        try:
            VAR["running"] = True
            cnt = 5
            sensors = await VAR["sma"].get_sensors()
            device_info = await VAR["sma"].device_info()

            for name, value in device_info.items():
                print("{:>15}{:>25}".format(name, value))

            while VAR.get("running"):
                await VAR["sma"].read(sensors)
                print_table(sensors)
                cnt -= 1
                if cnt == 0:
                    break
                await asyncio.sleep(2)
        finally:
            _LOGGER.info("Closing Session...")
            await VAR["sma"].close_session()


def main():
    """Run example."""
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="Test the SMA webconnect library.")
    parser.add_argument(
        "url",
        type=str,
        help="Web address of the Webconnect module (http://ip-address or https://ip-address)",
    )
    parser.add_argument("user", choices=["user", "installer"], help="Login username")
    parser.add_argument("password", help="Login password")

    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    def _shutdown(*_):
        VAR["running"] = False
        # asyncio.ensure_future(sma.close_session(), loop=loop)

    signal.signal(signal.SIGINT, _shutdown)
    # loop.add_signal_handler(signal.SIGINT, shutdown)
    # signal.signal(signal.SIGINT, signal.SIG_DFL)
    loop.run_until_complete(
        main_loop(loop, user=args.user, password=args.password, url=args.url)
    )


if __name__ == "__main__":
    main()
