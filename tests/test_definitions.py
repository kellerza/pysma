"""Test pysma const file."""

import pysma.definitions
from pysma.sensor import Sensor


def test_duplicate_sensors():
    """Test if defined sensors have unique key and name."""
    variables = vars(pysma.definitions)
    found_keys = []
    found_names = []
    for value in variables.values():
        if isinstance(value, Sensor):
            found_key = f"{value.key}_{value.key_idx}"
            found_name = value.name

            assert found_key not in found_keys
            found_keys.append(found_key)

            assert found_name not in found_names
            found_names.append(found_name)


def test_sensor_map():
    """Test if all map entries only contain unique items."""
    for sensor_map in pysma.definitions.sensor_map.values():
        unique_items = list({f"{s.key}_{s.key_idx}": s for s in sensor_map}.values())
        assert unique_items == sensor_map
