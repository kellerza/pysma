"""SMA WebConnect library for Python.

See: http://www.sma.de/en/products/monitoring-control/webconnect.html

Source: http://www.github.com/kellerza/pysma
"""
import copy
import json
import logging

import jmespath  # type: ignore
from aiohttp import ClientTimeout, client_exceptions, hdrs

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
    def __init__(self, session, url, password=None, group="user", uid=None):
        """Init SMA connection."""
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
        self.sma_sid = None
        self.sma_uid = uid
        self.l10n = {}
        self.devclass = None
        self.device_info_sensors = Sensors(definitions.sensor_map[DEVICE_INFO])

    async def _request_json(self, method, url, **kwargs):
        """Request json data for requests."""
        if self.sma_sid:
            kwargs.setdefault("params", {})
            kwargs["params"]["sid"] = self.sma_sid

        _LOGGER.debug("Sending %s request to %s: %s", method, url, kwargs)

        try:
            res = await self._aio_session.request(
                method,
                self._url + url,
                timeout=ClientTimeout(total=DEFAULT_TIMEOUT),
                **kwargs,
            )
        except client_exceptions.ClientError as exc:
            raise SmaConnectionException(
                f"Could not connect to SMA at {self._url}"
            ) from exc

        try:
            res_json = await res.json()
        except (client_exceptions.ContentTypeError, json.decoder.JSONDecodeError):
            _LOGGER.warning("Request to %s did not return a valid json.", url)
            return {}

        return res_json or {}

    async def _get_json(self, url):
        """Get json data for requests."""
        return await self._request_json(hdrs.METH_GET, url)

    async def _post_json(self, url, payload=None):
        """Post json data for requests."""
        params = {}
        if payload is not None:
            params["data"] = json.dumps(payload)
            params["headers"] = {"content-type": "application/json"}

        return await self._request_json(hdrs.METH_POST, url, **params)

    async def _read_l10n(self, lang="en-US"):
        """Read device language file."""
        return await self._get_json(f"/data/l10n/{lang}.json")

    async def _read_body(self, url, payload):
        if self.sma_sid is None and self._new_session_data is not None:
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

        if self.sma_uid is None:
            # Get the unique ID
            self.sma_uid = next(iter(body["result"].keys()), None)

        result_body = body["result"].pop(self.sma_uid, None)
        if body != {"result": {}}:
            _LOGGER.warning(
                "Unexpected body %s, extracted %s",
                json.dumps(body),
                json.dumps(result_body),
            )

        return result_body

    async def new_session(self):
        """Establish a new session."""
        self.l10n = await self._read_l10n()
        body = await self._post_json(URL_LOGIN, self._new_session_data)
        self.sma_sid = jmespath.search("result.sid", body)
        if self.sma_sid:
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

    async def close_session(self):
        """Close the session login."""
        if self.sma_sid is None:
            return
        try:
            await self._post_json(URL_LOGOUT)
        finally:
            self.sma_sid = None

    async def read(self, sensors):
        """Read a set of keys."""
        if self._new_session_data is None:
            payload = {"destDev": [], "keys": []}
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
        for sen in sensors:
            if sen.enabled:
                if sen.key in result_body:
                    sen.extract_value(result_body, self.l10n, devclass)
                    continue

                notfound.append(f"{sen.name} [{sen.key}]")

        if notfound:
            _LOGGER.info(
                "No values for sensors: %s. Response from inverter: %s",
                ",".join(notfound),
                result_body,
            )

        return True

    async def read_logger(self, sensors=None, start=None, end=None):
        """Read a logging key and return the results."""
        if self._new_session_data is None:
            payload = {"destDev": [], "key": []}
            result_body = await self._read_body(URL_DASH_LOGGER, payload)
        else:
            payload = {
                "destDev": [],
                "key": int(sensors[0].key),
                "tStart": start,
                "tEnd": end,
            }
            result_body = await self._read_body(URL_LOGGER, payload)
        if not result_body:
            return False

        for sen in sensors:
            sen.extract_logger(result_body)

        return True

    async def device_info(self):
        """Read device info and return the results."""
        await self.read(self.device_info_sensors)

        device_info = {
            "serial": self.device_info_sensors["serial_number"].value
            or FALLBACK_DEVICE_INFO["serial"],
            "name": self.device_info_sensors["device_name"].value
            or FALLBACK_DEVICE_INFO["name"],
            "type": self.device_info_sensors["device_type"].value
            or FALLBACK_DEVICE_INFO["type"],
            "manufacturer": self.device_info_sensors["device_manufacturer"].value
            or FALLBACK_DEVICE_INFO["manufacturer"],
            "sw_version": version_int_to_string(
                self.device_info_sensors["device_sw_version"].value
            ),
        }

        return device_info

    async def get_devclass(self, result_body=None):
        """Get the device class."""
        if self.devclass:
            return self.devclass

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

            self.devclass = devclass_keys[0]
            _LOGGER.debug("Found device class %s", self.devclass)

        return self.devclass

    async def get_sensors(self):
        """Get the sensors based on the device class."""
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
