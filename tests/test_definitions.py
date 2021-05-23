"""Test pysma const file."""

import pysma.definitions


def test_duplicate_sensors():
    """Test if defined sensors have unique key and name"""
    variables = vars(pysma.definitions)
    found_keys = []
    found_names = []
    for value in variables.values():
        if isinstance(value, pysma.definitions.SensorDefinition):
            found_key = value.key
            found_name = value.name
            if len(value.key.split("_")) == 2:
                found_key = found_key + "_0"

            assert found_key not in found_keys
            found_keys.append(found_key)

            assert found_name not in found_names
            found_names.append(found_name)


def test_sensor_map():
    """Test if all map entries only contain unique items"""
    for sensor_map in pysma.definitions.sensor_map.values():
        unique_items = list({s.key: s for s in sensor_map}.values())
        assert unique_items == sensor_map
