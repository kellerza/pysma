"""Test pysma helpers file."""

import attrs

from pysma.helpers import version_int_to_string, DeviceInfo


def test_version_int_to_string() -> None:
    """Ensure version_int_to_string returns correct values."""
    assert version_int_to_string(4294967294) == "ff.ff.255."
    assert version_int_to_string(51387396) == "3.10.28.R"
    assert version_int_to_string(1) == "0.0.0.E"
    assert version_int_to_string(0) == ""
    assert version_int_to_string(None) == ""  # type: ignore[arg-type]


def test_devtype() -> None:
    """Test DeviceInfo."""
    res = DeviceInfo(
        serial="123456789",
        name="SMA Device",
        type=None,
        manufacturer="SMA",
        sw_version="1.0.0",
    )
    assert attrs.asdict(res) == {
        "serial": "123456789",
        "name": "SMA Device",
        "type": "",
        "manufacturer": "SMA",
        "sw_version": "1.0.0",
    }

    res = DeviceInfo(sw_version=1)

    assert attrs.asdict(res) == {
        "serial": "9999999999",
        "name": "SMA Device",
        "type": "",
        "manufacturer": "SMA",
        "sw_version": "0.0.0.E",
    }
