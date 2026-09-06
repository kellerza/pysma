"""Test pysma sensors."""

import logging
from collections.abc import Callable, Generator
from json import loads
from unittest.mock import MagicMock, patch

import pytest

from pysma.const import (
    GENERIC_SENSORS,
    JMESPATH_VAL,
    JMESPATH_VAL_IDX,
    JMESPATH_VAL_STR,
)
from pysma.definitions.webconnect import sensor_map
from pysma.sensor import Sensor, Sensor_Range, Sensors

_LOG = logging.getLogger(__name__)


SB_1_5 = loads(
    # {"result": {"012F-7309879F":
    """
    {
        "6400_00260100": {"1": [{"val": 3514000}]},
        "6400_00262200": {"1": [{"val": 402}]},
        "6380_40251E00": {"1": [{"val": 448}, {"val": 522}]}
    }
    """
    # }}
)

SB_2_5 = loads(
    # {"result": {"012F-730A2A43":
    """
    {
        "6400_00262200": {"val": 402},
        "6100_40263F00": {"val": null},
        "6400_00260100": {"val": 3514000},
        "6380_40251E00": [{"str": 1, "val": 448}, {"str": 2, "val": 522}]
    }
    """
    # }}
)


@pytest.fixture
def sensors() -> Generator[list[tuple[int, bool, Sensor]], None, None]:
    """Fixture to create some sensors."""
    yield [
        (402, True, Sensor("6400_00262200", "s_402", "W")),
        (3514, True, Sensor("6400_00260100", "s_3514", "W", 1000)),
        (448, True, Sensor("6380_40251E00_0", "pv_power_a", unit="W")),
        (522, True, Sensor("6380_40251E00_1", "pv_power_b", unit="W")),
    ]


class Test_sensor_class:
    """Test the Sensor class."""

    def test_sensor_sb_1_5(self, sensors: list) -> None:
        """Test extract value."""
        for val, change, sens in sensors:
            assert sens.path is None
            assert sens.extract_value(SB_1_5) is change
            assert sens.value == val
            assert sens.path == JMESPATH_VAL_IDX.format(sens.key_idx)

            assert sens.extract_value(SB_1_5) is False

    def test_sensor_sb_2_5(self, sensors: list) -> None:
        """Test extract value."""
        for val, change, sens in sensors:
            assert sens.path is None
            assert sens.extract_value(SB_2_5) is change
            assert sens.value == val
            assert sens.path == JMESPATH_VAL or JMESPATH_VAL_STR.format(sens.key_idx)

            assert sens.extract_value(SB_2_5) is False

    def test_null(self) -> None:
        """Test a null or None result."""
        sens = Sensor("6100_40263F00", "s_null", "kWh")
        assert sens.extract_value({"6100_40263F00": {"val": None}}) is False
        assert sens.value is None
        assert sens.extract_value({"6100_40263F00": {"1": [{"val": None}]}}) is False
        assert sens.value is None
        assert sens.extract_value({}) is False
        assert sens.value is None

        # For "W" sensors we will set it to 0 by default.
        sens = Sensor("6100_40263F00", "s_null", "W")
        assert sens.extract_value({"6100_40263F00": {"val": None}}) is True
        assert sens.value == 0
        assert sens.extract_value({"6100_40263F00": {"1": [{"val": None}]}}) is False
        assert sens.value == 0
        assert sens.extract_value({}) is True
        assert sens.value is None

    def test_no_value_decoded(self) -> None:
        """Test no value decoded."""
        sens = Sensor("6100_40263F00", "s_null", "W")
        assert sens.extract_value({"6100_40263F00": None}) is True
        sens = Sensor("6100_40263F00", "s_null", "kWh")
        assert sens.extract_value({"6100_40263F00": None}) is False


class Test_sensor_range:
    """Test Sensor.range detection, using shapes seen from a real STP5.0-3SE device."""

    def test_min_max(self) -> None:
        """A low != high pair is a genuine adjustable numeric range."""
        sens = Sensor("6802_00874100", "s_range")
        sens.extract_value(
            {"6802_00874100": {"9": [{"low": 10, "high": 1000000, "val": 100}]}}
        )
        assert sens.range == Sensor_Range("min/max", [10, 1000000])
        assert sens.range.contains(500)
        assert not sens.range.contains(5)

    def test_min_max_locked(self) -> None:
        """A low == high pair is still a range, just currently fixed to one value."""
        sens = Sensor("6800_00832A00", "inverter_power_limit")
        sens.extract_value(
            {"6800_00832A00": {"9": [{"low": 5000, "high": 5000, "val": 5000}]}}
        )
        assert sens.range == Sensor_Range("min/max", [5000, 5000])
        assert sens.range.contains(5000)
        assert not sens.range.contains(4999)

    def test_selection(self) -> None:
        """ValidVals with fewer selected tags than valid ones is a real selection."""
        sens = Sensor("6800_08822800", "s_selection")
        sens.extract_value(
            {
                "6800_08822800": {
                    "9": [{"validVals": [302, 1129, 1130], "val": [{"tag": 302}]}]
                }
            }
        )
        assert sens.range == Sensor_Range("selection", [302, 1129, 1130])
        assert sens.range.contains(1129)
        assert not sens.range.contains(9999)

    def test_capability_list_is_not_writable(self) -> None:
        """All validVals already present in val is a capability list, not a setting."""
        sens = Sensor("6800_08822100", "s_capabilities")
        sens.extract_value(
            {
                "6800_08822100": {
                    "9": [
                        {
                            "validVals": [601, 605, 606],
                            "val": [{"tag": 601}, {"tag": 605}, {"tag": 606}],
                        }
                    ]
                }
            }
        )
        assert sens.range is None

    def test_plain_string_is_not_writable(self) -> None:
        """A plain val with no low/high/validVals is read-only."""
        sens = Sensor("6800_10821E00", "device_name")
        sens.extract_value({"6800_10821E00": {"9": [{"val": "STP5.0-3SE-40 141"}]}})
        assert sens.range is None

    def test_writable_filter(self) -> None:
        """Sensors.writable() returns only sensors with a known range."""
        writable = Sensor("6802_00874100", "s_range")
        writable.extract_value(
            {"6802_00874100": {"9": [{"low": 10, "high": 1000000, "val": 100}]}}
        )
        readonly = Sensor("6800_10821E00", "device_name")
        readonly.extract_value({"6800_10821E00": {"9": [{"val": "some name"}]}})

        sens = Sensors([writable, readonly])
        assert sens.writable() == [writable]


class Test_sensors_class:
    """Test the Sensors class."""

    @patch("pysma.sensor._LOG.warning")
    def test_default_no_duplicates(self, mock_warn: MagicMock) -> None:
        """Ensure warning on duplicates."""
        sen = Sensors(sensor_map[GENERIC_SENSORS])
        assert len(sen) == len(sensor_map[GENERIC_SENSORS])
        assert mock_warn.call_count == 0
        # Add duplicate frequency
        news = Sensor("key1", "frequency", "")
        sen.add(news)
        assert mock_warn.call_count == 1
        assert sen[news.name] == news
        # Add duplicate freq, key should not be raised
        sen.add(Sensor("6100_00465700", "frequency", ""))
        assert mock_warn.call_count == 2
        # Add duplicate freq key only
        sen.add(Sensor("6100_00465700", "f001", ""))
        assert mock_warn.call_count == 3
        # Test different key_idx only
        sen.add(Sensor("key1_0", "frequency_0", ""))
        assert mock_warn.call_count == 3
        sen.add(Sensor("key1_1", "frequency_1", ""))
        assert mock_warn.call_count == 3

    @patch("pysma.sensor._LOG.warning")
    def test_type_error(self, mock_warn: Callable) -> None:
        """Ensure TypeError on not isinstance."""
        sen = Sensors()
        with pytest.raises(TypeError):
            sen.add("This is not a Sensor")  # type: ignore[arg-type]

    @patch("pysma.sensor._LOG.warning")
    def test_default_jmes(self, mock_warn: MagicMock) -> None:
        """Ensure default sensors are ok."""
        sens = Sensors(sensor_map[GENERIC_SENSORS])
        for sen in sens:
            sen.extract_value(SB_1_5)
        assert mock_warn.called
