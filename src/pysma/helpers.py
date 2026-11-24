"""Helper functions for the pysma library."""

import json
import logging
import pkgutil
from dataclasses import dataclass
from typing import Any

from .const import DEFAULT_LANG

_LOG = logging.getLogger(__name__)


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


def load_l10n(lang: str) -> dict:
    """Load the packaged translations for lang, falling back to DEFAULT_LANG.

    Blocking: run it in an executor from async code.

    Args:
        lang (str): Locale code, e.g., "en-US" or "de-DE".

    Returns:
        dict: Dictionary containing translation keys and their localized strings.

    """
    l10n = _load_l10n_from_package(lang)
    if not l10n and lang != DEFAULT_LANG:
        _LOG.warning(
            "Language '%s' not found in package, falling back to '%s'",
            lang,
            DEFAULT_LANG,
        )
        l10n = _load_l10n_from_package(DEFAULT_LANG)
    return l10n


def _load_l10n_from_package(locale: str) -> dict:
    data = pkgutil.get_data("pysma", f"l10n/{locale}.json")
    if data is None:
        return {}
    return json.loads(data)


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
