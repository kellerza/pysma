"""Test pysma sensors."""
# from homeassistant.loader import async_get_dhcp
import logging
from json import loads
from unittest.mock import patch

import aiohttp
import pytest

from pysma import SMA
from pysma.const import (
    DEVCLASS_INVERTER,
    ENERGY_METER_VIA_INVERTER,
    JMESPATH_VAL,
    JMESPATH_VAL_IDX,
    OPTIMIZERS_VIA_INVERTER,
)
from pysma.definitions import sensor_map
from pysma.sensor import Sensor, Sensors

from . import MOCK_DEVICE, MOCK_L10N, mock_aioresponse  # noqa: F401

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
        (402, True, Sensor("6400_00262200", "s_402", "W")),
        (3514, True, Sensor("6400_00260100", "s_3514", "W", 1000)),
    ]


class Test_sensor_class:
    """Test the Sensor class"""

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
            assert sens.path == JMESPATH_VAL

            assert sens.extract_value(SB_2_5) is False

    def test_null(self):
        """Test a null or None result."""
        sens = Sensor("6100_40263F00", "s_null", "W")
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


class Test_SMA_class:
    @pytest.fixture(autouse=True)
    def _setup(self, mock_aioresponse):  # noqa: F811
        self.host = "1.1.1.1"
        self.base_url = f"http://{self.host}"
        mock_aioresponse.get(
            f"{self.base_url}/data/l10n/en-US.json", payload=MOCK_L10N, repeat=True
        )
        mock_aioresponse.post(
            f"{self.base_url}/dyn/logout.json?sid=ABCD", payload={}, repeat=True
        )

    @patch("pysma._LOGGER.warning")
    async def test_session(self, mock_warn, mock_aioresponse):  # noqa: F811
        mock_aioresponse.post(
            f"{self.base_url}/dyn/login.json", payload={"result": {"sid": "ABCD"}}
        )
        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "extralongpassword")
        assert await sma.new_session()

        assert mock_warn.call_count == 1
        await sma.close_session()
        await sma.close_session()

        assert mock_warn.call_count == 1

    async def test_new_session_invalid_group(self, mock_aioresponse):  # noqa: F811
        session = aiohttp.ClientSession()
        with pytest.raises(KeyError):
            SMA(session, self.host, "pass", "invalid-group")

    async def test_new_session_fail(self, mock_aioresponse):  # noqa: F811
        mock_aioresponse.post(f"{self.base_url}/dyn/login.json", payload={"result": {}})

        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
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
        sma = SMA(session, self.host, "pass")
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
        sma = SMA(session, self.host, "pass")
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
        sma = SMA(session, self.host, "pass")
        assert await sma.new_session()
        result = await sma.device_info()
        assert not result

    async def test_get_devclass(self, mock_aioresponse):  # noqa: F811
        mock_aioresponse.post(
            f"{self.base_url}/dyn/login.json",
            payload={"result": {"sid": "ABCD"}},
        )
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={"result": {"0199-xxxxx385": {}}},
        )

        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
        assert await sma.get_devclass() is None

        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={
                "result": {
                    "0199-xxxxx385": {
                        "6180_08214800": {
                            "1": [{"val": [{"tag": "123"}]}],
                        },
                    }
                }
            },
        )

        assert await sma.get_devclass() == DEVCLASS_INVERTER

        sma.devclass = None
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={
                "result": {
                    "0199-xxxxx385": {
                        "6180_08214800": {},
                    }
                }
            },
        )
        assert await sma.get_devclass() is None

        sma.devclass = None
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={
                "result": {
                    "0199-xxxxx385": {
                        "6180_08214800": {
                            "val": "402",
                        },
                    }
                }
            },
        )
        assert await sma.get_devclass() is None

        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={
                "result": {
                    "0199-xxxxx385": {
                        "6800_12345678": {
                            "1": [{"val": "value1"}],
                            "7": [{"val": "value2"}],
                        },
                    }
                }
            },
        )

        with pytest.raises(KeyError):
            await sma.get_devclass()

        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={
                "result": {
                    "0199-xxxxx385": {
                        "6180_08214800": {
                            "1": [{"val": [{"tag": "123"}]}],
                        },
                    }
                }
            },
        )

        sma.devclass = None
        assert await sma.get_devclass("BOGUS_BODY") == DEVCLASS_INVERTER

        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={
                "result": {
                    "0199-xxxxx385": {
                        "6180_08214800": {
                            "1": [{"val": [{"tag": "123"}]}],
                        },
                    }
                }
            },
        )

        assert await sma.get_devclass({}) == DEVCLASS_INVERTER

        sma.devclass = "test"
        assert await sma.get_devclass() == "test"

    async def test_get_sensors(self, mock_aioresponse):  # noqa: F811
        mock_aioresponse.post(
            f"{self.base_url}/dyn/login.json", payload={"result": {"sid": "ABCD"}}
        )
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={
                "result": {
                    "0199-xxxxx385": {
                        "6180_08214800": {
                            "1": [{"val": [{"tag": "123"}]}],
                        },
                        "6800_008AA300": {
                            "1": [{"val": "0123456"}],
                        },
                        "6800_10852600": {
                            "1": [
                                {"val": "1"},
                                {"val": "2"},
                                {"val": None},
                            ]
                        },
                    }
                }
            },
            repeat=True,
        )

        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
        assert len(await sma.get_sensors()) == (
            len(sensor_map[DEVCLASS_INVERTER])
            + len(sensor_map[ENERGY_METER_VIA_INVERTER])
            + (len(sensor_map[OPTIMIZERS_VIA_INVERTER]) * 2)
        )

    async def test_get_sensors_no_result_body(self, mock_aioresponse):  # noqa: F811
        mock_aioresponse.post(
            f"{self.base_url}/dyn/login.json", payload={"result": {"sid": "ABCD"}}
        )
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={},
            repeat=True,
        )

        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
        assert len(await sma.get_sensors()) == len(sensor_map[DEVCLASS_INVERTER])
