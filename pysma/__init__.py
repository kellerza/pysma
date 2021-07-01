"""SMA WebConnect library for Python.

See: http://www.sma.de/en/products/monitoring-control/webconnect.html

Source: http://www.github.com/kellerza/pysma
"""
import copy
import json
import logging
from typing import Any, Dict, Optional

import jmespath  # type: ignore
from aiohttp import ClientSession, ClientTimeout, client_exceptions, hdrs

from . import definitions
from .const import (
    DEFAULT_TIMEOUT,
    DEVCLASS_INVERTER,
    DEVICE_INFO,
    ENERGY_METER_VIA_INVERTER,
    FALLBACK_DEVICE_INFO,
    OPTIMIZERS_VIA_INVERTER,
    URL_DASH_LOGGER,
    URL_DASH_VALUES,
    URL_LOGGER,
    URL_LOGIN,
    URL_LOGOUT,
    URL_VALUES,
    USERS,
)
from .exceptions import (
    SmaAuthenticationException,
    SmaConnectionException,
    SmaReadException,
)
from .helpers import version_int_to_string
from .sensor import Sensors

_LOGGER = logging.getLogger(__name__)


class SMA:
    """Class to connect to the SMA webconnect module and read parameters."""

    # pylint: disable=too-many-instance-attributes
    _aio_session: ClientSession
    _new_session_data: Optional[dict]
    _url: str
    _sid: Optional[str]
    _uid: Optional[str]
    _l10n: Optional[dict]
    _devclass: Optional[str]
    _device_info_sensors: Sensors

    def __init__(
        self,
        session: ClientSession,
        url: str,
        password: Optional[str] = None,
        group: str = "user",
        uid: Optional[str] = None,
    ):
        """Init SMA connection.

        Args:
            session (ClientSession): aiohttp client session
            url (str): Url or IP address of device
            password (str, optional): Password to use during login. Defaults to None.
            group (str, optional): Username to use during login. Defaults to "user".
            uid (str, optional): uid used for data extraction. Defaults to None.

        Raises:
            KeyError: User was not in USERS
        """
        # pylint: disable=too-many-arguments
        if group not in USERS:
            raise KeyError("Invalid user type: {}".format(group))
        if password is not None and len(password) > 12:
            _LOGGER.warning("Password should not exceed 12 characters")
        if password is None:
            self._new_session_data = None
        else:
            self._new_session_data = {"right": USERS[group], "pass": password}
        self._url = url.rstrip("/")
        if not url.startswith("http"):
            self._url = "http://" + self._url
        self._aio_session = session
        self._sid = None
        self._uid = uid
        self._l10n = None
        self._devclass = None
        self._device_info_sensors = Sensors(definitions.sensor_map[DEVICE_INFO])

    async def _request_json(
        self, method: str, url: str, **kwargs: Dict[str, Any]
    ) -> dict:
        """Request json data for requests.

        Args:
            method (str): HTTP method to use
            url (str): URL to do request to

        Raises:
            SmaConnectionException: Connection to device failed

        Returns:
            dict: json returned by device
        """
        if self._sid:
            kwargs.setdefault("params", {})
            kwargs["params"]["sid"] = self._sid

        _LOGGER.debug("Sending %s request to %s: %s", method, url, kwargs)

        max_retries = 2
        for retry in range(max_retries):
            try:
                async with self._aio_session.request(
                    method,
                    self._url + url,
                    timeout=ClientTimeout(total=DEFAULT_TIMEOUT),
                    **kwargs,
                ) as res:
                    return await res.json() or {}
            except (client_exceptions.ContentTypeError, json.decoder.JSONDecodeError):
                _LOGGER.warning("Request to %s did not return a valid json.", url)
                break
            except client_exceptions.ServerDisconnectedError as exc:
                if (retry + 1) < max_retries:
                    # For some reason the SMA device sometimes raises a server disconnected error
                    # If this happens we will retry up to `max_retries` times
                    # This prevents errors in Home Assistant
                    _LOGGER.debug("ServerDisconnectedError, will retry connection.")
                    continue

                raise SmaConnectionException(
                    f"Server at {self._url} disconnected {max_retries+1} times."
                ) from exc
            except client_exceptions.ClientError as exc:
                raise SmaConnectionException(
                    f"Could not connect to SMA at {self._url}: {exc}"
                ) from exc

        return {}

    async def _get_json(self, url: str) -> dict:
        """Get json data for requests.

        Args:
            url (str): URL to do GET request to

        Returns:
            dict: json returned by device
        """
        return await self._request_json(hdrs.METH_GET, url)

    async def _post_json(self, url: str, payload: Optional[dict] = None) -> dict:
        """Post json data for requests.

        Args:
            url (str): URL to do POST request to
            payload (dict, optional): payload to send to device. Defaults to None.

        Returns:
            dict: json returned by device
        """
        params: Dict[str, Any] = {}
        if payload is not None:
            params["data"] = json.dumps(payload)
            params["headers"] = {"content-type": "application/json"}

        return await self._request_json(hdrs.METH_POST, url, **params)

    async def _read_l10n(self, lang: str = "en-US") -> dict:
        """Read device language file. Returns cached value on subsequent calls.

        Args:
            lang (str, optional): Language code of file to retrieve. Defaults to "en-US".

        Returns:
            dict: json returned by device
        """
        if self._l10n is None:
            self._l10n = await self._get_json(f"/data/l10n/{lang}.json")
        return self._l10n

    async def _read_body(self, url: str, payload: dict) -> dict:
        """Parse the json returned by the device and extract result.

        Args:
            url (str): URL to reqquest data from
            payload (dict): payload to send to device
        Raises:
            SmaReadException: The json returned by the device was in an unexpected format

        Returns:
            dict: json result
        """
        if self._sid is None and self._new_session_data is not None:
            await self.new_session()
        body = await self._post_json(url, payload)

        # On the first error we close the session which will re-login
        err = body.get("err")

        if err is not None:
            _LOGGER.warning(
                "%s: error detected, closing session to force another login attempt, got: %s",
                self._url,
                body,
            )
            await self.close_session()
            raise SmaReadException("Error detected while reading")

        if "result" not in body:
            _LOGGER.warning("No 'result' in reply from SMA, got: %s", body)
            raise SmaReadException("No 'result' in reply from SMA")

        if self._uid is None:
            # Get the unique ID
            self._uid = next(iter(body["result"].keys()), None)

        result_body = body["result"].pop(self._uid, None)
        if body != {"result": {}}:
            _LOGGER.warning(
                "Unexpected body %s, extracted %s",
                json.dumps(body),
                json.dumps(result_body),
            )

        return result_body

    async def new_session(self) -> bool:
        """Establish a new session.

        Raises:
            SmaAuthenticationException: Authentication failed

        Returns:
            bool: authentication successful
        """
        body = await self._post_json(URL_LOGIN, self._new_session_data)
        self._sid = jmespath.search("result.sid", body)
        if self._sid:
            _LOGGER.debug("New SID: %s", self._sid)
            return True

        err = body.pop("err", None)
        msg = "Could not start session, %s, got {}".format(body)

        if err:
            if err == 503:
                _LOGGER.error(msg, "Max amount of sessions reached")
            else:
                _LOGGER.error(msg, err)
        else:
            _LOGGER.error(msg, "Session ID expected [result.sid]")

        raise SmaAuthenticationException()

    async def close_session(self) -> None:
        """Close the session login."""
        if self._sid is None:
            return
        try:
            await self._post_json(URL_LOGOUT)
        finally:
            self._sid = None

    async def read(self, sensors: Sensors) -> bool:
        """Read a set of keys.

        Args:
            sensors (Sensors): Sensors object containing Sensor objects to read

        Returns:
            bool: reading was successful
        """
        if self._new_session_data is None:
            payload: Dict[str, Any] = {"destDev": [], "keys": []}
            result_body = await self._read_body(URL_DASH_VALUES, payload)
        else:
            payload = {
                "destDev": [],
                "keys": list({s.key for s in sensors if s.enabled}),
            }
            result_body = await self._read_body(URL_VALUES, payload)
        if not result_body:
            return False

        notfound = []
        devclass = await self.get_devclass(result_body)
        l10n = await self._read_l10n()
        for sen in sensors:
            if sen.enabled:
                if sen.key in result_body:
                    sen.extract_value(result_body, l10n, str(devclass))
                    continue

                notfound.append(f"{sen.name} [{sen.key}]")

        if notfound:
            _LOGGER.info(
                "No values for sensors: %s. Response from inverter: %s",
                ",".join(notfound),
                result_body,
            )

        return True

    async def read_dash_logger(self) -> dict:
        """Read the dash loggers.

        Returns:
            dict: Dictionary containing loggers returned by device.
        """
        return await self._read_body(URL_DASH_LOGGER, {"destDev": [], "key": []})

    async def read_logger(self, log_id: int, start: int, end: int) -> list:
        """Read a logging key and return the results.

        Args:
            log_id (int): The ID of the log to read.
                totWhOut5min: 28672
                totWhOutDaily: 28704
                GridMsTotWhOutDaily: 28752
                GridMsTotWhInDaily: 28768
                ObjLogBatCha: 28816
                totWhIn5min: 28736
                totWhInDaily: 28768
                ObjLogBatChrg: 29344
                ObjLogBatDsch: 29360
            start (int): Start timestamp in seconds.
            end (int): End timestamp in seconds.

        Returns:
            list: The log entries returned by the device
        """
        payload = {
            "destDev": [],
            "key": log_id,
            "tStart": start,
            "tEnd": end,
        }
        result_body = await self._read_body(URL_LOGGER, payload)
        if not isinstance(result_body, list):
            raise SmaReadException("List of log entries expected.")

        return result_body

    async def device_info(self) -> dict:
        """Read device info and return the results.

        Returns:
            dict: dict containing serial, name, type, manufacturer and sw_version
        """
        await self.read(self._device_info_sensors)

        device_info = {
            "serial": self._device_info_sensors["serial_number"].value
            or FALLBACK_DEVICE_INFO["serial"],
            "name": self._device_info_sensors["device_name"].value
            or FALLBACK_DEVICE_INFO["name"],
            "type": self._device_info_sensors["device_type"].value
            or FALLBACK_DEVICE_INFO["type"],
            "manufacturer": self._device_info_sensors["device_manufacturer"].value
            or FALLBACK_DEVICE_INFO["manufacturer"],
            "sw_version": version_int_to_string(
                self._device_info_sensors["device_sw_version"].value
            ),
        }

        return device_info

    async def get_devclass(self, result_body: Optional[dict] = None) -> Optional[str]:
        """Get the device class.

        Args:
            result_body (dict, optional): result body to extract device class from.
                Defaults to None.

        Raises:
            KeyError: More than 1 device class key is not supported

        Returns:
            str: The device class identifier, or None if no identifier was found
        """
        if self._devclass:
            return self._devclass

        if not result_body or not isinstance(result_body, dict):
            # Read the STATUS_SENSOR.
            # self.read will call get_devclass and update self.devclass
            await self.read(Sensors(definitions.status))
        else:
            sensor_values = list(result_body.values())
            devclass_keys = list(sensor_values[0].keys())
            if len(devclass_keys) == 0:
                return None
            if len(devclass_keys) > 1:
                raise KeyError("More than 1 device class key is not supported")
            if devclass_keys[0] == "val":
                return None

            self._devclass = devclass_keys[0]
            _LOGGER.debug("Found device class %s", self._devclass)

        return self._devclass

    async def get_sensors(self) -> Sensors:
        """Get the sensors based on the device class.

        Returns:
            Sensors: Sensors object containing Sensor objects
        """
        # Fallback to DEVCLASS_INVERTER if devclass returns None
        devclass = await self.get_devclass() or DEVCLASS_INVERTER

        _LOGGER.debug("Loading sensors for device class %s", devclass)
        device_sensors = Sensors(definitions.sensor_map.get(devclass))

        if devclass == DEVCLASS_INVERTER:
            em_sensor = copy.copy(definitions.energy_meter)
            payload = {
                "destDev": [],
                "keys": [
                    em_sensor.key,
                    definitions.optimizer_serial.key,
                ],
            }
            result_body = await self._read_body(URL_VALUES, payload)

            if not result_body:
                return device_sensors

            # Detect and add Energy Meter sensors
            em_sensor.extract_value(result_body)

            if em_sensor.value:
                _LOGGER.debug(
                    "Energy Meter with serial %s detected. Adding extra sensors.",
                    em_sensor.value,
                )
                device_sensors.add(
                    [
                        sensor
                        for sensor in definitions.sensor_map[ENERGY_METER_VIA_INVERTER]
                        if sensor not in device_sensors
                    ]
                )

            # Detect and add Optimizer Sensors
            optimizers = result_body.get(definitions.optimizer_serial.key)
            if optimizers:
                serials = optimizers.get(DEVCLASS_INVERTER)

                for idx, serial in enumerate(serials or []):
                    if serial["val"]:
                        _LOGGER.debug(
                            "Optimizer %s with serial %s detected. Adding extra sensors.",
                            idx,
                            serial,
                        )
                        for sensor_definition in definitions.sensor_map[
                            OPTIMIZERS_VIA_INVERTER
                        ]:
                            new_sensor = copy.copy(sensor_definition)
                            new_sensor.key_idx = idx
                            new_sensor.name = f"{sensor_definition.name}_{idx}"
                            device_sensors.add(new_sensor)

        return device_sensors
