"""SMA WebConnect library for Python.

See: http://www.sma.de/en/products/monitoring-control/webconnect.html

Source: http://www.github.com/kellerza/pysma
"""
import asyncio
import json
import logging

import async_timeout
import attr
import jmespath
from aiohttp import client_exceptions

_LOGGER = logging.getLogger(__name__)

USERS = {"user": "usr", "installer": "istl"}

JMESPATH_BASE = "result.*"
JMESPATH_VAL_IDX = '"1"[{}].val'
JMESPATH_VAL = "val"


@attr.s(slots=True)
class Sensor:
    """pysma sensor definition."""

    key = attr.ib()
    name = attr.ib()
    unit = attr.ib()
    factor = attr.ib(default=None)
    path = attr.ib(default=None)
    value = attr.ib(default=None, init=False)
    key_idx = attr.ib(default=0, repr=False, init=False)

    def __attrs_post_init__(self):
        """Init path."""
        idx = 0
        key = str(self.key)
        if key[-2] == "_" and key[-1].isdigit():
            idx = key[-1]
            key = key[:-2]
        self.key = key
        self.key_idx = idx

    def extract_logger(self, result_body):
        """Extract logs from json body."""
        self.value = result_body

    def extract_value(self, result_body):
        """Extract value from json body."""
        try:
            res = result_body[self.key]
        except (KeyError, TypeError):
            _LOGGER.warning("Sensor %s: Not found in %s", self.key, result_body)
            res = self.value
            self.value = None
            return self.value != res

        if not isinstance(self.path, str):
            # Try different methods until we can decode...
            _paths = (
                list(self.path)
                if isinstance(self.path, (list, tuple))
                else [JMESPATH_VAL, JMESPATH_VAL_IDX.format(self.key_idx)]
            )

            while _paths:
                _path = _paths.pop()
                _val = jmespath.search(_path, res)
                if _val is not None:
                    _LOGGER.debug(
                        "Sensor %s: Will be decoded with %s from %s",
                        self.name,
                        _path,
                        res,
                    )
                    self.path = _path
                    break

        # Extract new value
        if isinstance(self.path, str):
            res = jmespath.search(self.path, res)
        else:
            _LOGGER.debug(
                "Sensor %s: No successful value decoded yet: %s", self.name, res
            )
            res = None

        if isinstance(res, (int, float)) and self.factor:
            res /= self.factor
        try:
            return res != self.value
        finally:
            self.value = res


class Sensors:
    """SMA Sensors."""

    def __init__(self, add_default_sensors=True):
        self.__s = []
        if add_default_sensors:
            self.add(
                (
                    # AC side - Grid measurements
                    Sensor("6100_40263F00", "grid_power", "W"),
                    Sensor("6100_00465700", "frequency", "Hz", 100),
                    Sensor("6100_00464800", "voltage_l1", "V", 100),
                    Sensor("6100_00464900", "voltage_l2", "V", 100),
                    Sensor("6100_00464A00", "voltage_l3", "V", 100),
                    Sensor("6100_40465300", "current_l1", "A", 1000),
                    Sensor("6100_40465400", "current_l2", "A", 1000),
                    Sensor("6100_40465500", "current_l3", "A", 1000),
                    Sensor("6100_40464000", "power_l1", "W"),
                    Sensor("6100_40464100", "power_l2", "W"),
                    Sensor("6100_40464200", "power_l3", "W"),
                    # DC side - PV Generation
                    Sensor("6100_0046C200", "pv_power", "W"),
                    Sensor("6380_40251E00_0", "pv_power_a", "W"),
                    Sensor("6380_40251E00_1", "pv_power_b", "W"),
                    Sensor("6380_40451F00", "pv_voltage", "V", 100),
                    Sensor("6380_40451F00_0", "pv_voltage_a", "V", 100),
                    Sensor("6380_40451F00_1", "pv_voltage_b", "V", 100),
                    Sensor("6380_40452100", "pv_current", "A", 1000),
                    Sensor("6380_40452100_0", "pv_current_a", "A", 1000),
                    Sensor("6380_40452100_1", "pv_current_b", "A", 1000),
                    Sensor("6400_0046C300", "pv_gen_meter", "kWh", 1000),
                    Sensor("6400_00260100", "total_yield", "kWh", 1000),
                    Sensor("6400_00262200", "daily_yield", "Wh"),
                    # AC side - Measured values - Grid measurements
                    Sensor("6100_40463600", "grid_power_supplied", "W"),
                    Sensor("6100_40463700", "grid_power_absorbed", "W"),
                    Sensor("6400_00462400", "grid_total_yield", "kWh", 1000),
                    Sensor("6400_00462500", "grid_total_absorbed", "kWh", 1000),
                    # Consumption = Energy from the PV system and grid
                    Sensor("6100_00543100", "current_consumption", "W"),
                    Sensor("6400_00543A00", "total_consumption", "kWh", 1000),
                    # General
                    Sensor(
                        "6180_08214800",
                        "status",
                        "",
                        None,
                        ('"1"[0].val[0].tag', "val[0].tag"),
                    ),
                )
            )

    def __len__(self):
        """Length."""
        return len(self.__s)

    def __contains__(self, key):
        """Check if a sensor is defined."""
        try:
            if self[key]:
                return True
        except KeyError:
            return False

    def __getitem__(self, key):
        """Get a sensor using either the name or key."""
        for sen in self.__s:
            if sen.name == key or sen.key == key:
                return sen
        raise KeyError(key)

    def __iter__(self):
        """Iterator."""
        return self.__s.__iter__()

    def add(self, sensor):
        """Add a sensor, warning if it exists."""
        if isinstance(sensor, (list, tuple)):
            for sss in sensor:
                self.add(sss)
            return

        if not isinstance(sensor, Sensor):
            raise TypeError("pysma.Sensor expected")

        if sensor.name in self:
            old = self[sensor.name]
            self.__s.remove(old)
            _LOGGER.warning("Replacing sensor %s with %s", old, sensor)

        if sensor.key in self and self[sensor.key].key_idx is sensor.key_idx:
            _LOGGER.warning(
                "Duplicate SMA sensor key %s (idx: %s)", sensor.key, sensor.key_idx
            )

        self.__s.append(sensor)


URL_LOGIN = "/dyn/login.json"
URL_LOGOUT = "/dyn/logout.json"
URL_VALUES = "/dyn/getValues.json"
URL_LOGGER = "/dyn/getLogger.json"
URL_DASH_LOGGER = "/dyn/getDashLogger.json"
URL_DASH_VALUES = "/dyn/getDashValues.json"


class SMA:
    """Class to connect to the SMA webconnect module and read parameters."""

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

        self.device_info_sensors = Sensors(False)
        self.device_info_sensors.add(Sensor("6800_00A21E00", "serial_number", ""))
        self.device_info_sensors.add(Sensor("6800_10821E00", "device_name", ""))
        self.device_info_sensors.add(
            Sensor(
                "6800_08822000",
                "device_type_id",
                "",
                None,
                ('"1"[0].val[0].tag', "val[0].tag"),
            )
        )
        self.device_info_sensors.add(
            Sensor(
                "6800_08822B00",
                "device_manufacturer_id",
                "",
                None,
                ('"1"[0].val[0].tag', "val[0].tag"),
            )
        )

    async def _fetch_json(self, url, payload):
        """Fetch json data for requests."""
        params = {
            "data": json.dumps(payload),
            "headers": {"content-type": "application/json"},
            "params": {"sid": self.sma_sid} if self.sma_sid else None,
        }
        for _ in range(3):
            try:
                with async_timeout.timeout(10):
                    res = await self._aio_session.post(self._url + url, **params)
                    return (await res.json()) or {}
            except (asyncio.TimeoutError, client_exceptions.ClientError):
                continue
        return {"err": "Could not connect to SMA at {} (timeout)".format(self._url)}

    async def _read_l10n(self, lang="en-US"):
        """Read device language file."""
        res = await self._aio_session.get(f"{self._url}/data/l10n/{lang}.json")
        return (await res.json()) or {}

    async def _read_body(self, url, payload):
        if self.sma_sid is None and self._new_session_data is not None:
            await self.new_session()
            if self.sma_sid is None:
                return None
        body = await self._fetch_json(url, payload=payload)

        # On the first error we close the session which will re-login
        err = body.get("err")
        if err is not None:
            _LOGGER.warning(
                "%s: error detected, closing session to force another login attempt, got: %s",
                self._url,
                body,
            )
            await self.close_session()
            return None

        if not isinstance(body, dict) or "result" not in body:
            _LOGGER.warning("No 'result' in reply from SMA, got: %s", body)
            return None

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
        body = await self._fetch_json(URL_LOGIN, self._new_session_data)
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
        return False

    async def close_session(self):
        """Close the session login."""
        if self.sma_sid is None:
            return
        try:
            await self._fetch_json(URL_LOGOUT, {})
        finally:
            self.sma_sid = None

    async def read(self, sensors):
        """Read a set of keys."""
        if self._new_session_data is None:
            payload = {"destDev": [], "keys": []}
            result_body = await self._read_body(URL_DASH_VALUES, payload)
        else:
            payload = {"destDev": [], "keys": list({s.key for s in sensors})}
            result_body = await self._read_body(URL_VALUES, payload)
        if not result_body:
            return False

        notfound = []
        for sen in sensors:
            if sen.key in result_body:
                sen.extract_value(result_body)
                continue

            notfound.append(f"{sen.name} [{sen.key}]")

        if notfound:
            _LOGGER.warning(
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
        fallback_device_info = {
            "manufacturer": "SMA",
            "name": "SMA Device",
            "type": "",
            "serial": "9999999999",
        }

        values = await self.read(self.device_info_sensors)
        if not values:
            return False

        device_info = {
            "serial": self.device_info_sensors["serial_number"].value
            or fallback_device_info["serial"],
            "name": self.device_info_sensors["device_name"].value
            or fallback_device_info["senamerial"],
            "type": self.l10n.get(str(self.device_info_sensors["device_type_id"].value))
            or fallback_device_info["type"],
            "manufacturer": self.l10n.get(
                str(self.device_info_sensors["device_manufacturer_id"].value)
            )
            or fallback_device_info["manufacturer"],
        }

        return device_info
