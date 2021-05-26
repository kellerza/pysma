"""Test pysma helpers file."""
from pysma.helpers import version_int_to_string


def test_version_int_to_string():
    assert version_int_to_string(51387396) == "3.10.28.R"
    assert version_int_to_string(None) == ""
