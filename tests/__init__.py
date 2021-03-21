"""Tests for pysma."""
from aioresponses import aioresponses
import pytest

MOCK_DEVICE = {
    "manufacturer": "SMA",
    "name": "SMA Device Name",
    "type": "Sunny Boy 3.6",
    "serial": "123456789",
}
MOCK_L10N = {"461": "SMA", "9402": "Sunny Boy 3.6"}


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m
