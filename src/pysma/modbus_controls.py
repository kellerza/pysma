"""Named controls exposed over SMA Modbus/SunSpec (Model 123/124).

Kept separate from pysma.controls.Control, which is WebConnect-only (see its
docstring) - SMAWebConnect never needs to special-case a control it can't
serve, and SMAModbus never needs WebConnect's tag-id conventions.
"""

from enum import StrEnum


class ModbusControl(StrEnum):
    """Semantic controls exposed over Modbus/SunSpec. Added one at a time."""

    # --- Model 123 (immediate_controls) ---
    INVERTER_ENABLED = "inverter_enabled"
    # Raw values are SunSpec Model 123's Conn enum (0=DISCONNECT, 1=CONNECT) -
    # NOT WebConnect's OPERATING_MODE_STOP/START tag ids (381/1467). The two
    # transports' Control enums are deliberately separate; do not assume the
    # raw int means the same thing across both. Confirmed working (read AND
    # write) against a real Sunny Tripower 5.0 SE.

    POWER_LIMIT = "power_limit"
    # SunSpec Model 123's WMaxLimPct (% of WMax, 0-100) - NOT the same
    # register or scale as WebConnect's Control.POWER_LIMIT (an absolute-Watt
    # value via a different mechanism entirely). Requires WMaxLim_Ena to be
    # enabled to take effect; SMAModbus.set_control enables it lazily (only
    # if not already enabled), never on every write - see the flash-wear
    # warning in sma_modbus's module docstring.

    POWER_FACTOR = "power_factor"
    # SunSpec Model 123's OutPFSet (cos phi, -1.0 to 1.0). No WebConnect
    # equivalent. Requires OutPFSet_Ena, gated lazily like POWER_LIMIT above.

    REACTIVE_POWER_WMAX_PCT = "reactive_power_wmax_pct"
    REACTIVE_POWER_VARMAX_PCT = "reactive_power_varmax_pct"
    REACTIVE_POWER_VARAVAL_PCT = "reactive_power_varaval_pct"
    # SunSpec Model 123's VArWMaxPct/VArMaxPct/VArAvalPct (-100 to 100) -
    # three different bases for the SAME underlying reactive-power setpoint;
    # only the one currently selected by VArPct_Mod has any effect on the
    # device. Setting any one of these three lazily switches VArPct_Mod to
    # match it and enables VArPct_Ena (same lazy-gate pattern as above) - so
    # setting a different one of the three later switches the mode again.
    # No WebConnect equivalent.

    # ACTIVE_POWER_LIMITATION_GCP: intentionally not implemented. Likely
    # plant-level (Sunny Home Manager), not per-inverter Modbus. Revisit only
    # once verified against a real device's register map - do not guess an
    # offset.

    # --- Model 124 (storage) ---
    STORAGE_CHARGE_RATE = "storage_charge_rate"  # InWRte
    STORAGE_DISCHARGE_RATE = "storage_discharge_rate"  # OutWRte
    STORAGE_RESERVE_SOC = "storage_reserve_soc"  # MinRsvPct
    # WChaMax and StorCtl_Mod are modelled as component fields (see
    # sma_modbus._StorageControls) but not exposed as their own
    # get_control/set_control targets in this pass - the spec named only the
    # three controls above. Revisit if a caller needs to read/toggle the
    # charge-control-enabled bits or max charge power directly. Model 124
    # itself is confirmed NOT present under SunSpec profile 2.0 (see
    # sma_modbus module docstring) - kept here for older-profile devices.
