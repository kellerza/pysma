#!/usr/bin/env python
"""Basic usage example and testing of pysma."""

import argparse
import asyncio
import logging
import signal
import sys
from typing import Any

import aiohttp
import attrs

from pysma import exceptions, sma_webconnect

# This example will work with Python 3.12+

_LOG = logging.getLogger(__name__)

VAR = {}


def print_table(sensors: sma_webconnect.Sensors) -> None:
    """Print sensors formatted as table."""
    for sen in sensors:
        if sen.value is None:
            print(f"{sen.name:>25}")
        else:
            print(f"{sen.name:>25}{sen.value!s:>15} {sen.unit}")


async def main_loop(password: str, user: str, url: str) -> None:
    """Run main loop."""
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        VAR["sma"] = sma_webconnect.SMAWebConnect(
            session, url, password=password, group=user
        )

        try:
            await VAR["sma"].new_session()
        except exceptions.SmaAuthenticationException:
            _LOG.warning("Authentication failed!")
            return
        except exceptions.SmaConnectionException:
            _LOG.warning("Unable to connect to device at %s", url)
            return

        # We should not get any exceptions, but if we do we will close the session.
        try:
            VAR["running"] = True  # type: ignore[assignment]
            cnt = 5
            sensors = await VAR["sma"].get_sensors()
            device_info = await VAR["sma"].device_info()

            for name, value in attrs.asdict(device_info).items():
                print(f"{name:>15}{value:>25}")

            # enable all sensors
            for sensor in sensors:
                sensor.enabled = True

            while VAR.get("running"):
                await VAR["sma"].read(sensors)
                print_table(sensors)
                cnt -= 1
                if cnt == 0:
                    break
                await asyncio.sleep(2)
        finally:
            _LOG.info("Closing Session...")
            await VAR["sma"].close_session()


async def main() -> None:
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

    def _shutdown(*_: Any) -> None:
        VAR["running"] = False  # type: ignore[assignment]

    signal.signal(signal.SIGINT, _shutdown)

    await main_loop(user=args.user, password=args.password, url=args.url)


if __name__ == "__main__":
    asyncio.run(main())
