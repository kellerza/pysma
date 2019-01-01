"""Test pysma sensors."""
import logging
from json import loads

import pytest

# from tests.test_util.aiohttp import mock_aiohttp_client
import pysma

_LOGGER = logging.getLogger(__name__)


SB_1_5 = loads("""
    {"result": {"012F-7309879F": {
        "6400_00260100": {"1": [{"val": 3514000}]},
        "6400_00262200": {"1": [{"val": 402}]}
    }}}""")


SB_2_5 = loads("""
    {"result": {"012F-730A2A43": {
        "6400_00262200": {"val": 402},
        "6100_40263F00": {"val": null},
        "6400_00260100": {"val": 3514000}
    }}}""")


@pytest.fixture
def sensors():
    """Fixture to create some sensors."""
    yield [
        (402, True, pysma.Sensor('s_402', '6400_00262200', 'W')),
        (3514, True, pysma.Sensor('s_3514', '6400_00260100', 'W', 1000)),
        # (None, False, pysma.Sensor('s_null', '6100_40263F00', 'W'))
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
