"""SMA Modbus/SunSpec support (Model 123 immediate controls, Model 124 storage).

Confirmed against SMA's official documentation (SunSpecModbus-TI-en-11.pdf,
covering Sunny Boy / Sunny Tripower / Sunny Highpower, and
STP60_SHP75_STPS60-SunSpec_Modbus-TI-en-15.pdf for the Tripower 60/Highpower
Peak1/Tripower Storage 60 + Inverter Manager line):

- SunSpec Modbus is a SEPARATE profile from SMA's own proprietary Modbus
  profile (the one input-register-based community libraries such as
  https://github.com/burmistrzak/sma-modbus-hacs use for telemetry). Both can
  be active on the same device at once, on different unit IDs.
- Modbus (and specifically the SunSpec profile) is disabled by default and
  must be enabled per-device via the installation assistant (Network
  configuration > Modbus).
- The SunSpec profile's unit ID is NOT the same as the proprietary profile's
  unit ID: it is the proprietary profile's unit ID + 123. SMA's own default
  proprietary-profile unit ID is 3, so the SunSpec unit ID defaults to 126 -
  NOT 1 or 3. Get this wrong and every SunSpec read fails with Modbus
  exception 0x02 (ILLEGAL_DATA_ADDRESS), which looks identical to "this
  device doesn't support SunSpec at all."
- The SunSpec profile version (1.0/1.1/2.0) is auto-selected by the device's
  configured country data set (2.0 for a data set based on SMA Grid Guard 10,
  i.e. year >= 2018; older/compatibility-mode systems get 1.0/1.1). Model 123
  (Immediate Controls) is supported in all versions. Model 124 (Storage) was
  DROPPED in profile 2.0 (see "Not Supported Information Models" in
  SunSpecModbus-TI-en-11.pdf) with no direct replacement yet - the 700-series
  successor (Model 713, DER Storage Capacity) is documented as planned for a
  future firmware version, not necessarily present yet. So _StorageControls
  below may simply not exist on a modern (2018+ country data set) device;
  get_control_schema/get_control/set_control already return None/raise for a
  model that discover() didn't find, so this degrades gracefully - but do not
  expect Model 124 support on a current-firmware, modern-dataset install.
"""

from dataclasses import dataclass, field
from enum import IntEnum, IntFlag
from typing import Any, Self

from modbus_connection import (
    ModbusError,
    ModbusExceptionError,
    ModbusTcpParams,
    ModbusTimeoutError,
)
from modbus_connection.model.sunspec import (
    SunSpecComponent,
    bitfield16,
    enum16,
    int16,
    scan,
    sunssf,
    uint16,
)
from modbus_connection.model.sunspec.errors import SunSpecError
from modbus_connection.tmodbus import ModbusConnection

from .exceptions import (
    SmaConnectionException,
    SmaReadException,
    SmaSunSpecException,
    SmaTimeoutException,
    SmaWriteException,
)
from .modbus_controls import ModbusControl

MODEL_ID_IMMEDIATE_CONTROLS = 123
MODEL_ID_STORAGE_CONTROLS = 124

#: Per SMA's documented convention: the SunSpec profile's unit ID is the
#: proprietary "SMA Modbus profile" unit ID + 123 - NOT the same unit ID.
SUNSPEC_UNIT_ID_OFFSET = 123
#: SMA's own default unit ID for the proprietary profile (and thus, + 123,
#: for SunSpec) - see module docstring.
DEFAULT_SMA_UNIT_ID = 3


class InverterConnAction(IntEnum):
    """SunSpec Model 123 `Conn` point values."""

    DISCONNECT = 0
    CONNECT = 1


class WMaxLimEna(IntEnum):
    """SunSpec Model 123 `WMaxLim_Ena` point values - gates `w_max_lim_pct`."""

    DISABLED = 0
    ENABLED = 1


class OutPFSetEna(IntEnum):
    """SunSpec Model 123 `OutPFSet_Ena` point values - gates `out_pf_set`."""

    DISABLED = 0
    ENABLED = 1


class VArPctMod(IntEnum):
    """SunSpec Model 123 `VArPct_Mod` - selects which VAr-percent point is live."""

    NONE = 0
    WMAX = 1
    VAR_MAX = 2
    VAR_AVAL = 3


class VArPctEna(IntEnum):
    """SunSpec Model 123 `VArPct_Ena` point values - gates the VAr-percent points."""

    DISABLED = 0
    ENABLED = 1


class _ImmediateControls(SunSpecComponent):
    """SunSpec Model 123 - subset of fields pysma uses."""

    conn = enum16(4, InverterConnAction, writable=True)
    w_max_lim_pct = uint16(5, scale_register=23, writable=True, unit="% WMax")
    w_max_lim_ena = enum16(9, WMaxLimEna, writable=True)
    out_pf_set = int16(10, scale_register=24, writable=True, unit="cos()")
    out_pf_set_ena = enum16(14, OutPFSetEna, writable=True)
    v_ar_w_max_pct = int16(15, scale_register=25, writable=True, unit="% WMax")
    v_ar_max_pct = int16(16, scale_register=25, writable=True, unit="% VArMax")
    v_ar_aval_pct = int16(17, scale_register=25, writable=True, unit="% VArAval")
    v_ar_pct_mod = enum16(21, VArPctMod, writable=True)
    v_ar_pct_ena = enum16(22, VArPctEna, writable=True)
    _w_max_lim_pct_sf = sunssf(23)
    _out_pf_set_sf = sunssf(24)
    _var_pct_sf = sunssf(25)


class StorageControlMode(IntFlag):
    """Bit values for SunSpec Model 124 `StorCtl_Mod` (not itself exposed as a control)."""

    CHARGE_ENABLED = 1
    DISCHARGE_ENABLED = 2


class _StorageControls(SunSpecComponent):
    """SunSpec Model 124 - subset of fields pysma uses.

    Confirmed NOT discovered on a real Sunny Tripower 5.0 SE (SunSpec profile
    2.0 dropped Model 124, per SMA's SunSpecModbus-TI-en-11.pdf - see module
    docstring); discover() correctly leaves storage controls unavailable
    rather than erroring. Kept for devices still on an older SunSpec profile
    version, but the offsets themselves remain UNVERIFIED against any real
    Model 124 data - confirm before relying on them.
    """

    wcha_max = uint16(2, scale_register=18, writable=True)  # WChaMax
    stor_ctl_mod = bitfield16(5, StorageControlMode, writable=True)  # StorCtl_Mod
    min_rsv_pct = uint16(7, scale_register=21, writable=True)  # MinRsvPct
    out_w_rte = int16(12, scale_register=25, writable=True)  # OutWRte
    in_w_rte = int16(13, scale_register=25, writable=True)  # InWRte
    _cha_sf = sunssf(18)
    _rsv_sf = sunssf(21)
    _rte_sf = sunssf(25)


@dataclass(frozen=True)
class _ControlSpec:
    """Where a control lives, its valid range, and any one-time gates to arm first."""

    component_cls: type[SunSpecComponent]
    field: str
    range: tuple[float, float]
    #: (gate field name, required value) pairs. set_control ensures each gate
    #: already holds its required value before writing `field`, writing a
    #: gate only when it doesn't already match - never on every call. See
    #: _ImmediateControls' docstring for why (flash-wear).
    gates: tuple[tuple[str, IntEnum], ...] = ()


#: Every control this class knows how to serve, keyed by ModbusControl.
_CONTROL_SPECS: dict[ModbusControl, _ControlSpec] = {
    ModbusControl.INVERTER_ENABLED: _ControlSpec(_ImmediateControls, "conn", (0, 1)),
    ModbusControl.POWER_LIMIT: _ControlSpec(
        _ImmediateControls,
        "w_max_lim_pct",
        (0, 100),
        gates=(("w_max_lim_ena", WMaxLimEna.ENABLED),),
    ),
    ModbusControl.POWER_FACTOR: _ControlSpec(
        _ImmediateControls,
        "out_pf_set",
        (-1.0, 1.0),
        gates=(("out_pf_set_ena", OutPFSetEna.ENABLED),),
    ),
    ModbusControl.REACTIVE_POWER_WMAX_PCT: _ControlSpec(
        _ImmediateControls,
        "v_ar_w_max_pct",
        (-100, 100),
        gates=(
            ("v_ar_pct_mod", VArPctMod.WMAX),
            ("v_ar_pct_ena", VArPctEna.ENABLED),
        ),
    ),
    ModbusControl.REACTIVE_POWER_VARMAX_PCT: _ControlSpec(
        _ImmediateControls,
        "v_ar_max_pct",
        (-100, 100),
        gates=(
            ("v_ar_pct_mod", VArPctMod.VAR_MAX),
            ("v_ar_pct_ena", VArPctEna.ENABLED),
        ),
    ),
    ModbusControl.REACTIVE_POWER_VARAVAL_PCT: _ControlSpec(
        _ImmediateControls,
        "v_ar_aval_pct",
        (-100, 100),
        gates=(
            ("v_ar_pct_mod", VArPctMod.VAR_AVAL),
            ("v_ar_pct_ena", VArPctEna.ENABLED),
        ),
    ),
    ModbusControl.STORAGE_CHARGE_RATE: _ControlSpec(
        _StorageControls, "in_w_rte", (0, 100)
    ),
    ModbusControl.STORAGE_DISCHARGE_RATE: _ControlSpec(
        _StorageControls, "out_w_rte", (0, 100)
    ),
    ModbusControl.STORAGE_RESERVE_SOC: _ControlSpec(
        _StorageControls, "min_rsv_pct", (0, 100)
    ),
}


@dataclass
class SMAModbus:
    """Connect to an SMA device over Modbus/SunSpec and read/write controls.

    Construction does no I/O and does not create the connection - call
    ``connect()`` explicitly once before ``discover()``/``get_control()``/
    ``set_control()``. Keeping this out of ``__init__`` lets a caller (e.g.
    Home Assistant's ``async_setup_entry``) construct the object cheaply
    ahead of time and control exactly when the connection is established.

    Owns its Modbus TCP connection by default - built from ``host``/``port``
    inside ``connect()``, so a caller doesn't need to build one separately.
    Call ``close()`` (or use ``async with SMAModbus(...) as sma_modbus:``,
    which calls ``connect()`` on enter and ``close()`` on exit) when done.
    Pass an existing ``connection`` instead to reuse one you already opened
    (e.g. shared with another client on the same device, or in tests);
    ``host``/``port`` are then ignored, and SMAModbus will never close a
    connection it did not create itself.

    ``sma_unit_id`` is the proprietary "SMA Modbus profile" unit ID (SMA's
    own default is 3, matching e.g. burmistrzak/sma-modbus-hacs's
    ``default_unit_id`` for telemetry) - NOT the SunSpec unit ID. The SunSpec
    unit ID is derived automatically as ``sma_unit_id + SUNSPEC_UNIT_ID_OFFSET``
    per SMA's documented convention, unless ``sunspec_unit_id`` is given
    explicitly to override a device that deviates from the default.
    """

    host: str | None = None
    port: int = 502
    sma_unit_id: int = DEFAULT_SMA_UNIT_ID
    sunspec_unit_id: int | None = None
    connection: ModbusConnection | None = field(default=None, repr=False)

    _close_connection: bool = field(default=False, init=False, repr=False)
    _unit: Any = field(default=None, init=False, repr=False)
    _immediate: _ImmediateControls | None = field(default=None, init=False, repr=False)
    _storage: _StorageControls | None = field(default=None, init=False, repr=False)

    async def connect(self) -> None:
        """Create (or reuse) the Modbus connection, and open the TCP link.

        Must be called once before discover()/get_control()/set_control().
        Safe to call more than once - a no-op if already connected. :)

        Raises:
            SmaConnectionException: the device could not be reached.

        """
        if self.connection is None:
            if self.host is None:
                raise ValueError(
                    "SMAModbus requires either host or an existing connection"
                )
            self.connection = ModbusConnection(
                ModbusTcpParams(host=self.host, port=self.port)
            )
            self._close_connection = True
        uid = (
            self.sunspec_unit_id
            if self.sunspec_unit_id is not None
            else self.sma_unit_id + SUNSPEC_UNIT_ID_OFFSET
        )
        self._unit = self.connection.for_unit(uid)
        try:
            await self.connection.connect()
        except ModbusTimeoutError as exc:
            raise SmaTimeoutException(str(exc)) from exc
        except ModbusError as exc:
            raise SmaConnectionException(str(exc)) from exc

    async def discover(self, base_address: int = 40000) -> None:
        """Probe for supported SunSpec models. Idempotent; safe to re-call.

        Populates whichever of Model 123/124 are present, independently - a
        device without Model 124 (dropped in SunSpec profile 2.0, see module
        docstring) still gets Model 123 support.

        Raises:
            SmaSunSpecException: no SunSpec marker found at base_address on
                this unit ID, or the model chain is malformed. If you get
                this, double check: (1) Modbus/SunSpec is actually enabled on
                the device, (2) the unit ID - it's sma_unit_id + 123, not
                sma_unit_id itself (see class docstring).
            SmaConnectionException: the device could not be reached at all
                (as opposed to reached but not answering SunSpec).

        """
        try:
            models = await scan(self._unit, base_address)
        except SunSpecError as exc:
            raise SmaSunSpecException(str(exc)) from exc
        except ModbusError as exc:
            raise SmaConnectionException(str(exc)) from exc

        if (found := models.first(MODEL_ID_IMMEDIATE_CONTROLS)) is not None:
            self._immediate = _ImmediateControls(self._unit, found)
        if (found := models.first(MODEL_ID_STORAGE_CONTROLS)) is not None:
            self._storage = _StorageControls(self._unit, found)

    def _component_for(self, control: ModbusControl) -> SunSpecComponent | None:
        cls = _CONTROL_SPECS[control].component_cls
        return self._immediate if cls is _ImmediateControls else self._storage

    def get_control_schema(self, control: ModbusControl) -> tuple[float, float] | None:
        """Return control's valid (min, max), or None if unsupported on this device."""
        if self._component_for(control) is None:
            return None
        return _CONTROL_SPECS[control].range

    async def get_control(self, control: ModbusControl) -> float | None:
        """Return control's current value, reading fresh from the device.

        Returns None if control is unsupported on this device (model not
        discovered).

        Raises:
            SmaReadException: the read failed (communication error).

        """
        component = self._component_for(control)
        if component is None:
            return None
        try:
            await component.async_update()
        except (ModbusExceptionError, ModbusError) as exc:
            raise SmaReadException(str(exc)) from exc
        value = getattr(component, _CONTROL_SPECS[control].field)
        return float(value) if value is not None else None

    async def set_control(self, control: ModbusControl, value: float) -> None:
        """Set control to value.

        If the control has one-time gate fields (e.g. WMaxLim_Ena for
        POWER_LIMIT), each is armed first - but only if it doesn't already
        hold its required value, per the flash-wear warning in
        _ImmediateControls' docstring. Arming reads the component fresh, so
        this costs one extra round trip only when a gate isn't already set.

        Raises:
            SmaWriteException: unsupported on this device, value outside
                get_control_schema()'s range, or the write failed.

        """
        spec = _CONTROL_SPECS[control]
        component = self._component_for(control)
        if component is None:
            raise SmaWriteException(f"This device does not support {control}")
        low, high = spec.range
        if not low <= value <= high:
            raise SmaWriteException(
                f"{value} is outside {control}'s range ({low}, {high})"
            )
        try:
            if spec.gates:
                await component.async_update()
                for gate_field, required in spec.gates:
                    if getattr(component, gate_field) != required:
                        await component.write(gate_field, required)
            await component.write(spec.field, value)
        except (AttributeError, ValueError, ModbusError) as exc:
            raise SmaWriteException(str(exc)) from exc

    async def close(self) -> None:
        """Close the Modbus connection, if this instance created it."""
        if self.connection is not None and self._close_connection:
            await self.connection.close()

    async def __aenter__(self) -> Self:
        """Connect, then enter as an async context manager."""
        await self.connect()
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        """Close the connection on exit, if this instance created it."""
        await self.close()
