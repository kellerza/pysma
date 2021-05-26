"""Tests for pysma."""
import pytest
from aioresponses import aioresponses

MOCK_DEVICE = {
    "manufacturer": "SMA",
    "name": "SMA Device Name",
    "type": "Sunny Boy 3.6",
    "serial": "123456789",
    "sw_version": "",
}
MOCK_L10N = {"461": "SMA", "9402": "Sunny Boy 3.6"}


@pytest.fixture
def mock_aioresponse():
    """Yield a mock aioresponses."""
    with aioresponses() as m:
        yield m
