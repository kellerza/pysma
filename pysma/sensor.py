"""Sensor classes for SMA WebConnect library for Python. """
import logging

import attr
import jmespath

from .const import JMESPATH_VAL, JMESPATH_VAL_IDX

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class SensorDefinition:  # pylint: disable=too-few-public-methods
    """pysma sensor definition."""

    key = attr.ib()
    name = attr.ib()
    unit = attr.ib(default="")
    factor = attr.ib(default=None)
    path = attr.ib(default=None)
    enabled = attr.ib(default=True)
    l10n_translate = attr.ib(default=False)

    def create_sensor(self):
        """Create a Sensor from this SensorDefinition."""
        return Sensor(
            key=self.key,
            name=self.name,
            unit=self.unit,
            factor=self.factor,
            path=self.path,
            enabled=self.enabled,
            l10n_translate=self.l10n_translate,
        )


@attr.s(slots=True)
class Sensor(SensorDefinition):
    """pysma sensor."""

    value = attr.ib(default=None, init=False)
    key_idx = attr.ib(default="0", repr=False, init=False)

    def __attrs_post_init__(self):
        """Init path."""
        key = str(self.key)
        skey = key.split("_")
        if len(skey) > 2 and skey[2].isdigit():
            self.key = f"{skey[0]}_{skey[1]}"
            self.key_idx = skey[2]

    def extract_logger(self, result_body):
        """Extract logs from json body."""
        self.value = result_body

    def extract_value(self, result_body, l10n=None, devclass="1"):
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
                [sens_path.format(devclass, self.key_idx) for sens_path in self.path]
                if isinstance(self.path, (list, tuple))
                else [
                    JMESPATH_VAL,
                    JMESPATH_VAL_IDX.format(devclass, self.key_idx),
                ]
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

        if self.l10n_translate and isinstance(l10n, dict):
            res = l10n.get(
                str(res),
                res,
            )

        try:
            return res != self.value
        finally:
            self.value = res


class Sensors:
    """SMA Sensors."""

    def __init__(self, sensors=None):
        self.__s = []

        if sensors:
            self.add(sensors)

    def __len__(self):
        """Length."""
        return len(self.__s)

    # pylint: disable=R1710
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
            if key in (sen.name, sen.key):
                return sen
        raise KeyError(key)

    def __iter__(self):
        """Iterator."""
        return self.__s.__iter__()

    def add(self, sensor):
        """Add a sensor, warning if it exists."""
        if isinstance(sensor, list):
            for sss in sensor:
                self.add(sss)
            return

        # pylint: disable=unidiomatic-typecheck
        # We do not want to match Sensor here.
        if type(sensor) is SensorDefinition:
            self.add(sensor.create_sensor())
            return

        if not isinstance(sensor, Sensor):
            raise TypeError("pysma.Sensor expected")

        if sensor.name in self:
            old = self[sensor.name]
            self.__s.remove(old)
            _LOGGER.warning("Replacing sensor %s with %s", old, sensor)

        if sensor.key in self and self[sensor.key].key_idx == sensor.key_idx:
            _LOGGER.warning(
                "Duplicate SMA sensor key %s (idx: %s)", sensor.key, sensor.key_idx
            )

        self.__s.append(sensor)
