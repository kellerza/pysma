"""Test pysma sensors."""
import logging
from json import loads
from unittest.mock import patch

import pytest

from pysma.const import (
    DEVCLASS_INVERTER,
    JMESPATH_VAL,
    JMESPATH_VAL_IDX,
    JMESPATH_VAL_STR,
)
from pysma.definitions import sensor_map
from pysma.sensor import Sensor, Sensors

_LOGGER = logging.getLogger(__name__)


SB_1_5 = loads(
    # {"result": {"012F-7309879F":
    """
    {
        "6400_00260100": {"1": [{"val": 3514000}]},
        "6400_00262200": {"1": [{"val": 402}]},
        "6380_40251E00": {"1": [{"val": 448}, {"val": 0}]}
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
        "6380_40251E00": [{"str": 1, "val": 448}]
    }
    """
    # }}
)


@pytest.fixture
def sensors():
    """Fixture to create some sensors."""
    yield [
        (402, True, Sensor("6400_00262200", "s_402", "W")),
        (3514, True, Sensor("6400_00260100", "s_3514", "W", 1000)),
        (448, True, Sensor("6380_40251E00_0", "pv_power_a", unit="W")),
    ]


class Test_sensor_class:
    """Test the Sensor class."""

    def test_sensor_sb_1_5(self, sensors):
        """Test extract value."""
        for val, change, sens in sensors:
            assert sens.path is None
            assert sens.extract_value(SB_1_5) is change
            assert sens.value == val
            assert sens.path == JMESPATH_VAL_IDX.format("1", sens.key_idx)

            assert sens.extract_value(SB_1_5) is False

    def test_sensor_sb_2_5(self, sensors):
        """Test extract value."""
        for val, change, sens in sensors:
            assert sens.path is None
            assert sens.extract_value(SB_2_5) is change
            assert sens.value == val
            assert sens.path == JMESPATH_VAL or JMESPATH_VAL_STR.format(sens.key_idx)

            assert sens.extract_value(SB_2_5) is False

    def test_null(self):
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

    def test_no_value_decoded(self):
        sens = Sensor("6100_40263F00", "s_null", "W")
        assert sens.extract_value({"6100_40263F00": None}) is True
        sens = Sensor("6100_40263F00", "s_null", "kWh")
        assert sens.extract_value({"6100_40263F00": None}) is False


class Test_sensors_class:
    """Test the Sensors class."""

    @patch("pysma.sensor._LOGGER.warning")
    def test_default_no_duplicates(self, mock_warn):
        """Ensure warning on duplicates."""
        sen = Sensors(sensor_map[DEVCLASS_INVERTER])
        assert len(sen) > 20
        assert len(sen) < 50
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

    @patch("pysma.sensor._LOGGER.warning")
    def test_type_error(self, mock_warn):
        """Ensure TypeError on not isinstance."""
        sen = Sensors()
        with pytest.raises(TypeError):
            sen.add("This is not a Sensor")

    @patch("pysma.sensor._LOGGER.warning")
    def test_default_jmes(self, mock_warn):
        """Ensure default sensors are ok."""
        sens = Sensors(sensor_map[DEVCLASS_INVERTER])
        for sen in sens:
            sen.extract_value(SB_1_5)
        assert mock_warn.called
