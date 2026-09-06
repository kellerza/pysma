"""Named, model-agnostic controls exposed over SMA WebConnect."""

from enum import StrEnum

from .definitions.webconnect import (
    active_power_limitation,
    active_power_limitation_gcp,
    inverter_power_limit,
    operating_mode,
)

#: SMA's global tag ids for the "Operation.OpMod" (operating_mode) parameter.
OPERATING_MODE_STOP = 381
OPERATING_MODE_START = 1467


class Control(StrEnum):
    """Semantic controls. Added one at a time as they're identified."""

    # Maybe we can remove this later on, now it works fine for testing

    POWER_LIMIT = inverter_power_limit.name
    ACTIVE_POWER_LIMITATION = active_power_limitation.name
    ACTIVE_POWER_LIMITATION_GCP = active_power_limitation_gcp.name
    INVERTER_ENABLED = operating_mode.name
