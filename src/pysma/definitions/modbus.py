"""Sensor definitions for SMA Modbus (SMA profile, input registers).

Each entry reuses a WebConnect Sensor, so a sensor read over Modbus keeps the
WebConnect key, name, factor and l10n handling. The raw register values equal
WebConnect's raw values, so no extra scaling is needed. Addresses and types
come from SMA's parameter list (PARAMETER-HTML_STPxx-3SE-40_30109R_V11) and
were checked against a live STP5.0-3SE-40 on firmware 4.08.39.R.
"""

from dataclasses import dataclass
from typing import Any, Literal

from modbus_connection.model import int32, uint32, uint64
from modbus_connection.model.fields import RegisterField

from ..sensor import Sensor
from . import webconnect as wc

NAN_S32 = 0x80000000
NAN_U32 = 0xFFFFFFFF
NAN_U64 = 0xFFFFFFFFFFFFFFFF
#: Status/tag values use only the lower 24 bits of a U32.
NAN_TAG = 0xFFFFFD


@dataclass(frozen=True, slots=True)
class ModbusRegister:
    """An SMA profile input register."""

    address: int
    type: Literal["S32", "U32", "U64", "TAG"]

    @property
    def count(self) -> int:
        """Number of 16-bit registers."""
        return 4 if self.type == "U64" else 2

    def field(self) -> RegisterField[Any]:
        """Return a new field for this register, decoding SMA's NaN to None."""
        if self.type == "S32":
            return int32(self.address, nan=NAN_S32)
        if self.type == "U64":
            return uint64(self.address, nan=NAN_U64)
        return uint32(self.address, nan=NAN_TAG if self.type == "TAG" else NAN_U32)


def _s32(address: int) -> ModbusRegister:
    return ModbusRegister(address, "S32")


def _u32(address: int) -> ModbusRegister:
    return ModbusRegister(address, "U32")


def _u64(address: int) -> ModbusRegister:
    return ModbusRegister(address, "U64")


def _tag(address: int) -> ModbusRegister:
    return ModbusRegister(address, "TAG")


sensor_map: list[tuple[Sensor, ModbusRegister]] = [
    (wc.status, _tag(30201)),  # Operation.Health
    (wc.operating_status_general, _tag(40029)),  # Operation.OpStt
    (wc.operating_status, _tag(33003)),  # Operation.RunStt
    (wc.inverter_condition, _tag(32385)),  # Operation.Inverter.Health
    (wc.grid_relay_status, _tag(30217)),  # Operation.GriSwStt
    (wc.pv_power_a, _s32(30773)),  # DcMs.Watt[A]
    (wc.pv_power_b, _s32(30961)),  # DcMs.Watt[B]
    (wc.pv_voltage_a, _s32(30771)),  # DcMs.Vol[A]
    (wc.pv_voltage_b, _s32(30959)),  # DcMs.Vol[B]
    (wc.pv_current_a, _s32(30769)),  # DcMs.Amp[A]
    (wc.pv_current_b, _s32(30957)),  # DcMs.Amp[B]
    (wc.grid_power, _s32(30775)),  # GridMs.TotW
    (wc.frequency, _u32(30803)),  # GridMs.Hz
    (wc.power_l1, _s32(30777)),  # GridMs.W.phsA
    (wc.power_l2, _s32(30779)),  # GridMs.W.phsB
    (wc.power_l3, _s32(30781)),  # GridMs.W.phsC
    (wc.grid_reactive_power, _s32(31497)),  # GridMs.TotVAr
    (wc.grid_reactive_power_l1, _s32(30807)),  # GridMs.VAr.phsA
    (wc.grid_reactive_power_l2, _s32(30809)),  # GridMs.VAr.phsB
    (wc.grid_reactive_power_l3, _s32(30811)),  # GridMs.VAr.phsC
    (wc.grid_apparent_power, _s32(30813)),  # GridMs.TotVA
    (wc.grid_apparent_power_l1, _s32(30815)),  # GridMs.VA.phsA
    (wc.grid_apparent_power_l2, _s32(30817)),  # GridMs.VA.phsB
    (wc.grid_apparent_power_l3, _s32(30819)),  # GridMs.VA.phsC
    (wc.grid_power_factor, _u32(30949)),  # GridMs.TotPFPrc
    (wc.current_l1, _s32(30977)),  # GridMs.A.phsA
    (wc.current_l2, _s32(30979)),  # GridMs.A.phsB
    (wc.current_l3, _s32(30981)),  # GridMs.A.phsC
    (wc.current_total, _u32(30795)),  # GridMs.TotA
    (wc.voltage_l1, _u32(30783)),  # GridMs.PhV.phsA
    (wc.voltage_l2, _u32(30785)),  # GridMs.PhV.phsB
    (wc.voltage_l3, _u32(30787)),  # GridMs.PhV.phsC
    (wc.total_yield, _u64(30513)),  # Metering.TotWhOut
    (wc.daily_yield, _u64(30517)),  # Metering.DyWhOut
]

#: Register per sensor name.
registers: dict[str, ModbusRegister] = {
    sensor.name: register for sensor, register in sensor_map
}
