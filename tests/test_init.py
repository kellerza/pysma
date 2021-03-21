"""Test pysma sensors."""
# from homeassistant.loader import async_get_dhcp
import logging
import aiohttp
from json import loads
from unittest.mock import patch

import pytest

import pysma

from . import MOCK_L10N, MOCK_DEVICE, mock_aioresponse  # noqa: F401

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
        assert len(sen) == 30
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
        # Test different key_idx only
        sen.add(pysma.Sensor("key1_0", "frequency_0", ""))
        assert mock_warn.call_count == 3
        sen.add(pysma.Sensor("key1_1", "frequency_1", ""))
        assert mock_warn.call_count == 3

    @patch("pysma._LOGGER.warning")
    def test_type_error(self, mock_warn):
        """Ensure TypeError on not isinstance."""
        sen = pysma.Sensors()
        with pytest.raises(TypeError):
            sen.add("This is not a Sensor")

    @patch("pysma._LOGGER.warning")
    def test_default_jmes(self, mock_warn):
        """Ensure default sensors are ok."""
        sens = pysma.Sensors()
        for sen in sens:
            sen.extract_value(SB_1_5)
        assert mock_warn.called


class Test_SMA_class:
    @pytest.fixture(autouse=True)
    def _setup(self, mock_aioresponse):  # noqa: F811
        self.host = "1.1.1.1"
        self.base_url = f"http://{self.host}"
        mock_aioresponse.get(
            f"{self.base_url}/data/l10n/en-US.json",
            payload=MOCK_L10N,
        )
        mock_aioresponse.post(f"{self.base_url}/dyn/logout.json?sid=ABCD", payload={})

    @patch("pysma._LOGGER.warning")
    async def test_session(self, mock_warn, mock_aioresponse):  # noqa: F811
        mock_aioresponse.post(
            f"{self.base_url}/dyn/login.json", payload={"result": {"sid": "ABCD"}}
        )
        session = aiohttp.ClientSession()
        sma = pysma.SMA(session, self.host, "extralongpassword")
        assert await sma.new_session()

        assert mock_warn.call_count == 1
        await sma.close_session()
        await sma.close_session()

        assert mock_warn.call_count == 1

    async def test_new_session_invalid_group(self, mock_aioresponse):  # noqa: F811
        session = aiohttp.ClientSession()
        with pytest.raises(KeyError):
            pysma.SMA(session, self.host, "pass", "invalid-group")

    async def test_new_session_fail(self, mock_aioresponse):  # noqa: F811
        mock_aioresponse.post(f"{self.base_url}/dyn/login.json", payload={"result": {}})

        session = aiohttp.ClientSession()
        sma = pysma.SMA(session, self.host, "pass")
        assert not await sma.new_session()

    async def test_device_info(self, mock_aioresponse):  # noqa: F811
        mock_aioresponse.post(
            f"{self.base_url}/dyn/login.json", payload={"result": {"sid": "ABCD"}}
        )
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={
                "result": {
                    "0199-xxxxx385": {
                        "6800_08822B00": {
                            "1": [{"validVals": [461], "val": [{"tag": 461}]}]
                        },
                        "6800_00A21E00": {
                            "1": [
                                {"low": 0, "high": None, "val": MOCK_DEVICE["serial"]}
                            ]
                        },
                        "6800_08822000": {
                            "1": [
                                {
                                    "validVals": [9401, 9402, 9403, 9404, 9405],
                                    "val": [{"tag": 9402}],
                                }
                            ]
                        },
                        "6800_10821E00": {"1": [{"val": MOCK_DEVICE["name"]}]},
                    }
                }
            },
        )
        session = aiohttp.ClientSession()
        sma = pysma.SMA(session, self.host, "pass")
        result = await sma.device_info()
        assert result
        assert result == MOCK_DEVICE

    async def test_device_info_fallback(self, mock_aioresponse):  # noqa: F811
        mock_aioresponse.post(
            f"{self.base_url}/dyn/login.json", payload={"result": {"sid": "ABCD"}}
        )
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={
                "result": {
                    "0199-xxxxx385": {
                        "6800_08822B00": {
                            "1": [{"validVals": [461], "val": [{"tag": 461}]}]
                        },
                        "6800_10821E00": {"1": [{"val": MOCK_DEVICE["name"]}]},
                    }
                }
            },
        )
        session = aiohttp.ClientSession()
        sma = pysma.SMA(session, self.host, "pass")
        assert await sma.new_session()
        result = await sma.device_info()
        assert result
        assert result["manufacturer"] == "SMA"
        assert result["name"] == MOCK_DEVICE["name"]
        assert result["type"] == ""
        assert result["serial"] == "9999999999"

    async def test_device_info_fail(self, mock_aioresponse):  # noqa: F811
        mock_aioresponse.post(
            f"{self.base_url}/dyn/login.json", payload={"result": {"sid": "ABCD"}}
        )
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={},
        )
        session = aiohttp.ClientSession()
        sma = pysma.SMA(session, self.host, "pass")
        assert await sma.new_session()
        result = await sma.device_info()
        assert not result
