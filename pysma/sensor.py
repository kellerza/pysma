"""Sensor classes for SMA WebConnect library for Python."""
import copy
import logging
from typing import Any, Iterator, List, Optional, Union

import attr
import jmespath  # type: ignore

from .const import JMESPATH_VAL, JMESPATH_VAL_IDX, JMESPATH_VAL_STR

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class Sensor:
    """pysma sensor."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    key: str = attr.ib()
    name: str = attr.ib()
    unit: str = attr.ib(default="")
    factor: int = attr.ib(default=None)
    path: Union[list, tuple] = attr.ib(default=None)
    enabled: bool = attr.ib(default=True)
    l10n_translate: bool = attr.ib(default=False)
    value: Any = attr.ib(default=None, init=False)
    key_idx: int = attr.ib(default=0, repr=False, init=False)

    def __attrs_post_init__(self) -> None:
        """Post init Sensor."""
        key = str(self.key)
        skey = key.split("_")
        if len(skey) > 2 and skey[2].isdigit():
            self.key = f"{skey[0]}_{skey[1]}"
            self.key_idx = int(skey[2])

    def extract_value(
        self, result_body: dict, l10n: Optional[dict] = None, devclass: str = "1"
    ) -> bool:
        """Extract value from json body.

        Args:
            result_body (dict): json body retrieved from device
            l10n (dict, optional): Dictionary to translate tags to strings. Defaults to None.
            devclass (str, optional): The device class of the device used to extract the value.
                Defaults to "1".

        Returns:
            bool: Extracting value successful
        """
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
                    JMESPATH_VAL_STR.format(self.key_idx),
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

        # SMA will return None instead of 0 if if no power is generated
        # For "W" sensors we will set it to 0 by default.
        if res is None and self.unit == "W":
            res = 0

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

    def __init__(self, sensors: Union[Sensor, List[Sensor], None] = None):
        """Init Sensors.

        Args:
            sensors (Union[Sensor, List[Sensor], None], optional): One or a list of sensors
                to add on init. Defaults to None.
        """
        self.__s: List[Sensor] = []

        if sensors:
            self.add(sensors)

    def __len__(self) -> int:
        """Length of Sensor list.

        Returns:
            int: Number of Sensor objects
        """
        return len(self.__s)

    def __contains__(self, key: str) -> bool:
        """Check if a sensor is defined.

        Args:
            key (str): [description]

        Returns:
            bool: [description]
        """
        try:
            if self[key]:
                return True
        except KeyError:
            pass
        return False

    def __getitem__(self, key: str) -> Sensor:
        """Get a sensor.

        Args:
            key (str): Either the name or key of the Sensor

        Raises:
            KeyError: Item was not found

        Returns:
            Sensor: The matching Sensor object
        """
        for sen in self.__s:
            if key in (sen.name, sen.key):
                return sen
        raise KeyError(key)

    def __iter__(self) -> Iterator[Sensor]:
        """Iterate Sensor objects.

        Yields:
            Iterator[Sensor]: Sensor iterator
        """
        return self.__s.__iter__()

    def add(self, sensor: Union[Sensor, List[Sensor]]) -> None:
        """Add a sensor, logs warning if it exists.

        A copy of sensor, or the sensors in the list, will be added.
        If the sensor name already exists it will be overwritten.
        If the sensor key already exists it will not be added.

        Args:
            sensor (Sensor, List[Sensor]): One or a list of sensors to add

        Raises:
            TypeError: Argument sensor does not match an expected type
        """
        if isinstance(sensor, (list, tuple)):
            for sss in sensor:
                self.add(sss)
            return

        if isinstance(sensor, Sensor):
            sensor = copy.copy(sensor)
        else:
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
