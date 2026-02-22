"""Helper functions for the pysma library."""

from dataclasses import dataclass
from typing import Any


def version_int_to_string(version_integer: Any) -> str:
    """Convert a version integer to a readable string.

    Args:
        version_integer (int): The version integer, as retrieved from the device.

    Returns:
        str: The version translated to a readable string.

    """
    if not version_integer:
        return ""
    if not isinstance(version_integer, int):
        return str(version_integer)

    appendixes = ["N", "E", "A", "B", "R", "S"]
    version_bytes = version_integer.to_bytes(4, "big")
    version_appendix = (
        appendixes[version_bytes[3]] if 0 <= version_bytes[3] < len(appendixes) else ""
    )
    return f"{version_bytes[0]:x}.{version_bytes[1]:x}.{version_bytes[2]}.{version_appendix}"


def ensure_string(value: Any) -> str:
    """Ensure the value is a string."""
    return str(value) if value is not None else ""


@dataclass(slots=True)
class DeviceInfo:
    """Device information."""

    serial: str = ""
    name: str = ""
    type: str = ""
    manufacturer: str = ""
    sw_version: str = ""

    def __post_init__(self) -> None:
        """Fallback values."""
        self.manufacturer = ensure_string(self.manufacturer) or "SMA"
        self.name = ensure_string(self.name) or "SMA Device"
        self.serial = ensure_string(self.serial) or "9999999999"
        self.sw_version = ensure_string(self.sw_version) or "0.0.0.E"
        self.type = ensure_string(self.type)
