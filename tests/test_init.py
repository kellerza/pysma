"""Test pysma init."""
import asyncio
import logging
import re
from unittest.mock import patch

import aiohttp
import pytest

from pysma import SMA
from pysma.definitions import device_type as device_type_sensor
from pysma.exceptions import (
    SmaAuthenticationException,
    SmaConnectionException,
    SmaReadException,
)
from pysma.sensor import Sensors

from . import MOCK_DEVICE, MOCK_L10N, SMA_TESTDATA, mock_aioresponse  # noqa: F401

_LOGGER = logging.getLogger(__name__)


class Test_SMA_class:
    """Test the SMA class."""

    @pytest.fixture(autouse=True)
    def _setup(self, mock_aioresponse):  # noqa: F811
        self.host = "1.1.1.1"
        self.base_url = f"http://{self.host}"
        mock_aioresponse.get(
            re.compile(f"{self.base_url}/data/l10n/en-US.json.*"),
            payload=MOCK_L10N,
            repeat=True,
        )
        mock_aioresponse.post(
            f"{self.base_url}/dyn/logout.json?sid=ABCD", payload={}, repeat=True
        )

    async def test_request_json_connect_error(self, mock_aioresponse):  # noqa: F811
        """Test request_json with a SmaConnectionException."""
        mock_aioresponse.get(
            f"{self.base_url}/dummy-url",
            exception=aiohttp.client_exceptions.ClientConnectionError("mocked error"),
        )
        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
        with pytest.raises(SmaConnectionException):
            await sma._get_json("/dummy-url")

    async def test_request_json_server_disconnect_error(
        self, mock_aioresponse  # noqa: F811
    ):
        """Test request_json with a SmaConnectionException from ServerDisconnectedError."""
        mock_aioresponse.get(
            f"{self.base_url}/dummy-url",
            exception=aiohttp.client_exceptions.ServerDisconnectedError("mocked error"),
            repeat=True,
        )
        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
        with pytest.raises(SmaConnectionException):
            await sma._get_json("/dummy-url")

    async def test_timeout_error(self, mock_aioresponse):  # noqa: F811
        """Test request_json with a SmaConnectionException from TimeoutError."""
        mock_aioresponse.get(
            f"{self.base_url}/dummy-url",
            exception=asyncio.TimeoutError("mocked error"),
            repeat=True,
        )
        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
        with pytest.raises(SmaConnectionException):
            await sma._get_json("/dummy-url")

    @patch("pysma._LOGGER.warning")
    async def test_request_json_invalid_json(
        self, mock_warn, mock_aioresponse  # noqa: F811
    ):
        """Test request_json with invalid json."""
        mock_aioresponse.get(
            f"{self.base_url}/dummy-url",
            body="THIS IS NOT A VALID JSON",
        )
        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
        json = await sma._get_json("/dummy-url")
        assert isinstance(json, dict)
        assert json == {}
        assert mock_warn.call_count == 1

    @patch("pysma._LOGGER.warning")
    async def test_read_no_password(self, mock_warn, mock_aioresponse):  # noqa: F811
        """Test read_body without password."""
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getDashValues.json",
            payload={
                "result": {
                    "0199-xxxxx385": {
                        "6800_08822000": {
                            "1": [
                                {
                                    "validVals": [9401, 9402, 9403, 9404, 9405],
                                    "val": [{"tag": 9402}],
                                }
                            ]
                        },
                    }
                }
            },
        )
        session = aiohttp.ClientSession()
        sma = SMA(session, self.host)
        sensors = Sensors(device_type_sensor)
        assert await sma.read(sensors)
        assert sensors["6800_08822000"].value == "Sunny Boy 3.6"
        assert mock_warn.call_count == 0

    @patch("pysma._LOGGER.warning")
    async def test_read_body_error(self, mock_warn, mock_aioresponse):  # noqa: F811
        """Test read_body with SmaReadException."""
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD", payload={"err": 401}
        )
        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
        sma._sid = "ABCD"
        with pytest.raises(SmaReadException):
            await sma._read_body("/dyn/getValues.json", payload={"dummy": "payload"})
        assert mock_warn.call_count == 1

    @patch("pysma._LOGGER.warning")
    async def test_read_body_unexpected(
        self, mock_warn, mock_aioresponse  # noqa: F811
    ):
        """Test read_body with unexpected body."""
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getValues.json?sid=ABCD",
            payload={
                "result": {
                    "0199-xxxxx385": {},
                    "0199-yyyyy385": {},
                }
            },
        )
        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
        sma._sid = "ABCD"
        result_body = await sma._read_body(
            "/dyn/getValues.json", payload={"dummy": "payload"}
        )
        assert result_body == {}
        assert mock_warn.call_count == 1

    async def test_read_dash_logger(self, mock_aioresponse):  # noqa: F811
        """Test read_dash_logger."""
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getDashLogger.json",
            payload={
                "result": {
                    "0199-xxxxx385": {
                        "7000": {
                            "1": [
                                {"t": 1622569500, "v": 4565239},
                                {"t": 1622569800, "v": 4565249},
                            ]
                        },
                        "7020": {
                            "1": [
                                {"t": 1622498400, "v": 4542749},
                                {"t": 1622584800, "v": 4565355},
                            ]
                        },
                    }
                }
            },
        )

        session = aiohttp.ClientSession()
        sma = SMA(session, self.host)
        read_dash_logger = await sma.read_dash_logger()
        assert read_dash_logger == {
            "7000": {
                "1": [
                    {"t": 1622569500, "v": 4565239},
                    {"t": 1622569800, "v": 4565249},
                ]
            },
            "7020": {
                "1": [
                    {"t": 1622498400, "v": 4542749},
                    {"t": 1622584800, "v": 4565355},
                ]
            },
        }

    async def test_read_logger(self, mock_aioresponse):  # noqa: F811
        """Test read_logger."""
        mock_aioresponse.post(
            f"{self.base_url}/dyn/login.json", payload={"result": {"sid": "ABCD"}}
        )
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getLogger.json?sid=ABCD",
            payload={
                "result": {
                    "0199-xxxxx385": [
                        {"t": 1622498400, "v": 4542749},
                        {"t": 1622584800, "v": 4565355},
                    ]
                }
            },
        )

        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
        read_logger = await sma.read_logger(28704, 1622592000, 1622491200)
        assert read_logger == [
            {"t": 1622498400, "v": 4542749},
            {"t": 1622584800, "v": 4565355},
        ]

    async def test_read_logger_error(self, mock_aioresponse):  # noqa: F811
        """Test read_logger with SmaReadException."""
        mock_aioresponse.post(
            f"{self.base_url}/dyn/login.json", payload={"result": {"sid": "ABCD"}}
        )
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getLogger.json?sid=ABCD",
            payload={"result": {"0199-xxxxx385": "NOT A LIST"}},
        )

        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")

        with pytest.raises(SmaReadException):
            await sma.read_logger(28704, 1622592000, 1622491200)

    @patch("pysma._LOGGER.warning")
    async def test_new_session(self, mock_warn, mock_aioresponse):  # noqa: F811
        """Test new_session."""
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
        """Test new_session with invalid group."""
        session = aiohttp.ClientSession()
        with pytest.raises(KeyError):
            SMA(session, self.host, "pass", "invalid-group")

    async def test_new_session_fail(self, mock_aioresponse):  # noqa: F811
        """Test new_session with empty result."""
        mock_aioresponse.post(f"{self.base_url}/dyn/login.json", payload={"result": {}})

        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")
        with pytest.raises(SmaAuthenticationException):
            await sma.new_session()

    @patch("pysma._LOGGER.error")
    async def test_new_session_error(self, mock_error, mock_aioresponse):  # noqa: F811
        """Test new_session with error."""
        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")

        mock_aioresponse.post(
            f"{self.base_url}/dyn/login.json", payload={"err": "dummy-error"}
        )
        with pytest.raises(SmaAuthenticationException):
            await sma.new_session()
        assert mock_error.call_count == 1

        mock_aioresponse.post(f"{self.base_url}/dyn/login.json", payload={"err": 404})
        with pytest.raises(SmaAuthenticationException):
            await sma.new_session()
        assert mock_error.call_count == 2

        # Temporary update the URL to have https
        sma._url = f"https://{self.host}"
        mock_aioresponse.post(
            f"https://{self.host}/dyn/login.json", payload={"err": 404}
        )
        with pytest.raises(SmaAuthenticationException):
            await sma.new_session()
        sma._url = f"http://{self.host}"
        assert mock_error.call_count == 3

        mock_aioresponse.post(f"{self.base_url}/dyn/login.json", payload={"err": 503})
        with pytest.raises(SmaAuthenticationException):
            await sma.new_session()
        assert mock_error.call_count == 4

    async def test_device_info(self, mock_aioresponse):  # noqa: F811
        """Test device_info."""
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
        """Test device_info fallback."""
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
        assert result["sw_version"] == ""

    async def test_device_info_fail(self, mock_aioresponse):  # noqa: F811
        """Test device_info with SmaReadException."""
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
        with pytest.raises(SmaReadException):
            await sma.device_info()

    @pytest.mark.parametrize(
        "get_all_onl_values,get_all_param_values,number_of_sensors", SMA_TESTDATA
    )
    async def test_get_sensors(
        self,
        get_all_onl_values,
        get_all_param_values,
        number_of_sensors,
        mock_aioresponse,  # noqa: F811
    ):
        """Test get_sensors."""
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getAllOnlValues.json?sid=ABCD",
            payload=get_all_onl_values,
            repeat=True,
        )
        mock_aioresponse.post(
            f"{self.base_url}/dyn/getAllParamValues.json?sid=ABCD",
            payload=get_all_param_values,
            repeat=True,
        )

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
        assert len(await sma.get_sensors()) == number_of_sensors

    async def test_post_json(self):
        session = aiohttp.ClientSession()
        sma = SMA(session, self.host, "pass")

        with patch("pysma.SMA._request_json") as mock_request_json:
            await sma._post_json("dummy_url")
            mock_request_json.assert_called_once_with(
                "POST",
                "dummy_url",
                data="{}",
                headers={"content-type": "application/json"},
            )

        with patch("pysma.SMA._request_json") as mock_request_json:
            await sma._post_json("dummy_url", {"data": "dummy"})
            mock_request_json.assert_called_once_with(
                "POST",
                "dummy_url",
                data='{"data": "dummy"}',
                headers={"content-type": "application/json"},
            )
