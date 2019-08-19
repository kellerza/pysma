"""Test pysma sensors."""
import logging
from json import loads
from unittest.mock import patch

import pytest

import pysma

_LOGGER = logging.getLogger(__name__)


SB_1_5 = loads(
    # {"result": {"012F-7309879F":
    """
    {
        "6400_00260100": {"1": [{"val": 3514000}]},
        "6400_00262200": {"1": [{"val": 402}]}
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
        "6400_00260100": {"val": 3514000}
    }
    """
    # }}
)


@pytest.fixture
def sensors():
    """Fixture to create some sensors."""
    yield [
        (402, True, pysma.Sensor("6400_00262200", "s_402", "W")),
        (3514, True, pysma.Sensor("6400_00260100", "s_3514", "W", 1000)),
    ]


class Test_sensor_class:
    """Test the Sensor class"""

    def test_sensor_sb_1_5(self, sensors):
        """Test extract value."""
        for val, change, sens in sensors:
            assert sens.path is None
            assert sens.extract_value(SB_1_5) is change
            assert sens.value == val
            assert sens.path == pysma.JMESPATH_VAL_IDX.format(sens.key_idx)

            assert sens.extract_value(SB_1_5) is False

    def test_sensor_sb_2_5(self, sensors):
        """Test extract value."""
        for val, change, sens in sensors:
            assert sens.path is None
            assert sens.extract_value(SB_2_5) is change
            assert sens.value == val
            assert sens.path == pysma.JMESPATH_VAL

            assert sens.extract_value(SB_2_5) is False

    def test_null(self):
        """Test a null or None result."""
        sens = pysma.Sensor("6100_40263F00", "s_null", "W")
        assert (
            sens.extract_value({"result": {"_": {"6100_40263F00": {"val": None}}}})
            is False
        )
        assert sens.value is None
        assert (
            sens.extract_value(
                {"result": {"_": {"6100_40263F00": {"1": [{"val": None}]}}}}
            )
            is False
        )
        assert sens.value is None
        assert sens.extract_value({"result": {"_": {}}}) is False
        assert sens.value is None

    @patch("pysma._LOGGER.warning")
    def test_default_no_duplicates(self, mock_warn):
        """Ensure warning on duplicates."""
        sen = pysma.Sensors()
        assert mock_warn.call_count == 0
        # Add duplicate frequency
        news = pysma.Sensor("key1", "frequency", "")
        sen.add(news)
        assert mock_warn.call_count == 1
        assert sen[news.name] == news
        # Add duplicate freq, key should not be raised
        sen.add(pysma.Sensor("6100_00465700", "frequency", ""))
        assert mock_warn.call_count == 2
        # Add duplicate freq key only
        sen.add(pysma.Sensor("6100_00465700", "f001", ""))
        assert mock_warn.call_count == 3

    @patch("pysma._LOGGER.warning")
    def test_default_jmes(self, mock_warn):
        """Ensure default sensors are ok."""
        sens = pysma.Sensors()
        for sen in sens:
            sen.extract_value(SB_1_5)
        assert mock_warn.called


class Test_sms_connection:
    def test_init(self):
        """Initialize & close the SMA transport class."""
        aiosession = None
        sma = pysma.SMA(aiosession, "192.168.0.100", "pass")
        sma.close_session()
