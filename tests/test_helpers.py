"""Test pysma helpers file."""
from pysma.helpers import version_int_to_string


def test_version_int_to_string():
    """Ensure version_int_to_string returns correct values."""
    assert version_int_to_string(4294967294) == "ff.ff.255."
    assert version_int_to_string(51387396) == "3.10.28.R"
    assert version_int_to_string(1) == "0.0.0.E"
    assert version_int_to_string(0) == ""
    assert version_int_to_string(None) == ""
