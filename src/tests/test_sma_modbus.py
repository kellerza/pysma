"""Test sma_modbus."""

import pytest
from modbus_connection import ModbusTimeoutError

from pysma import SmaReadException, SmaSunSpecException, SmaWriteException
from pysma.modbus_controls import ModbusControl
from pysma.sma_modbus import (
    MODEL_ID_IMMEDIATE_CONTROLS,
    MODEL_ID_STORAGE_CONTROLS,
    InverterConnAction,
    OutPFSetEna,
    SMAModbus,
    VArPctEna,
    VArPctMod,
    WMaxLimEna,
)

BASE = 40000
_HEADER = 2  # SunS marker registers


def _seed_sunspec_header(unit, models: list[tuple[int, int]]) -> list[int]:
    """Seed the SunS marker and a model chain (id, data_length) pairs, terminated.

    Returns each model's header address (where its model_id register lives),
    in the same order as `models` - field addresses are `header + field.address`.
    """
    unit.holding[BASE] = 0x5375  # "Su"
    unit.holding[BASE + 1] = 0x6E53  # "nS"
    addr = BASE + _HEADER
    headers = []
    for model_id, length in models:
        headers.append(addr)
        unit.holding[addr] = model_id
        unit.holding[addr + 1] = length
        addr += length + 2
    unit.holding[addr] = 0xFFFF  # end marker
    unit.holding[addr + 1] = 0
    return headers


async def test_sunspec_unit_id_defaults_to_sma_unit_id_plus_123(
    mock_modbus_connection,
) -> None:
    """The SunSpec unit ID is sma_unit_id + 123, per SMA's documented convention.

    This is the actual bug behind the original "ILLEGAL_DATA_ADDRESS on
    function code 0x03" report: using the proprietary profile's unit ID (3)
    directly for a SunSpec read, instead of 3 + 123 = 126.
    """
    sma = SMAModbus(connection=mock_modbus_connection)
    await sma.connect()
    assert sma._unit._unit_id == 126

    sma_custom = SMAModbus(connection=mock_modbus_connection, sma_unit_id=5)
    await sma_custom.connect()
    assert sma_custom._unit._unit_id == 128

    sma_override = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
    await sma_override.connect()
    assert sma_override._unit._unit_id == 1


async def test_requires_host_or_connection() -> None:
    """connect() with neither host nor an existing connection fails clearly."""
    with pytest.raises(ValueError, match="host or an existing connection"):
        await SMAModbus().connect()


async def test_close_does_not_close_an_injected_connection(
    mock_modbus_connection, mock_modbus_unit
) -> None:
    """close() must never tear down a connection the caller supplied, only one it made."""
    sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
    await sma.connect()
    await sma.close()

    # the injected connection must still be usable by its owner afterward
    mock_modbus_unit.holding[100] = 42
    assert await mock_modbus_unit.read_holding_registers(100, 1) == [42]


async def test_async_context_manager_closes_owned_connection(
    mock_modbus_connection,
) -> None:
    """`async with SMAModbus(...)` closes the connection it created on exit.

    Uses an injected mock connection (so connect() does no real network I/O)
    but flips ``_close_connection`` to simulate SMAModbus having created it
    itself - isolating the ownership/close() behavior from connect()'s own
    correctness, which other tests already cover.
    """
    sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
    sma._close_connection = True
    async with sma:
        pass
    assert mock_modbus_connection._closed is True  # only way to prove close() ran


class Test_SMAModbus_controls:
    """Test SMAModbus's control methods."""

    async def test_discover_immediate_only(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """Device with only Model 123 (no battery) - storage is unsupported, not an error."""
        (header,) = _seed_sunspec_header(
            mock_modbus_unit, [(MODEL_ID_IMMEDIATE_CONTROLS, 4)]
        )
        mock_modbus_unit.holding[header + 4] = InverterConnAction.CONNECT  # conn

        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()

        assert await sma.get_control(ModbusControl.INVERTER_ENABLED) == 1
        assert await sma.get_control(ModbusControl.STORAGE_CHARGE_RATE) is None

    async def test_discover_both_models(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """Both Model 123 and 124 present -> both control groups available, independently."""
        _seed_sunspec_header(
            mock_modbus_unit,
            [(MODEL_ID_IMMEDIATE_CONTROLS, 4), (MODEL_ID_STORAGE_CONTROLS, 26)],
        )
        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()

        assert sma.get_control_schema(ModbusControl.INVERTER_ENABLED) is not None
        assert sma.get_control_schema(ModbusControl.POWER_LIMIT) is not None
        assert sma.get_control_schema(ModbusControl.POWER_FACTOR) is not None
        assert sma.get_control_schema(ModbusControl.REACTIVE_POWER_WMAX_PCT) is not None
        assert (
            sma.get_control_schema(ModbusControl.REACTIVE_POWER_VARMAX_PCT) is not None
        )
        assert (
            sma.get_control_schema(ModbusControl.REACTIVE_POWER_VARAVAL_PCT) is not None
        )
        assert sma.get_control_schema(ModbusControl.STORAGE_CHARGE_RATE) is not None
        assert sma.get_control_schema(ModbusControl.STORAGE_DISCHARGE_RATE) is not None
        assert sma.get_control_schema(ModbusControl.STORAGE_RESERVE_SOC) is not None

    async def test_get_control_schema(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """get_control_schema reflects only discovered controls."""
        _seed_sunspec_header(mock_modbus_unit, [(MODEL_ID_IMMEDIATE_CONTROLS, 4)])
        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()

        assert sma.get_control_schema(ModbusControl.INVERTER_ENABLED) == (0, 1)
        assert sma.get_control_schema(ModbusControl.STORAGE_CHARGE_RATE) is None

    async def test_set_control(self, mock_modbus_connection, mock_modbus_unit) -> None:
        """set_control writes, and the value round-trips on the next get_control."""
        _seed_sunspec_header(mock_modbus_unit, [(MODEL_ID_IMMEDIATE_CONTROLS, 4)])
        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()

        await sma.set_control(
            ModbusControl.INVERTER_ENABLED, InverterConnAction.CONNECT
        )

        assert await sma.get_control(ModbusControl.INVERTER_ENABLED) == 1

    async def test_set_control_out_of_range(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """set_control rejects a value outside get_control_schema()'s range."""
        _seed_sunspec_header(mock_modbus_unit, [(MODEL_ID_IMMEDIATE_CONTROLS, 4)])
        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()

        with pytest.raises(SmaWriteException):
            await sma.set_control(ModbusControl.INVERTER_ENABLED, 7)

    async def test_set_control_unsupported(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """set_control raises when the model wasn't discovered (e.g. no battery)."""
        _seed_sunspec_header(mock_modbus_unit, [(MODEL_ID_IMMEDIATE_CONTROLS, 4)])
        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()

        with pytest.raises(SmaWriteException):
            await sma.set_control(ModbusControl.STORAGE_CHARGE_RATE, 50)

    async def test_discover_no_marker(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """No SunS marker at all -> SmaSunSpecException, not a silent empty result."""
        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()

        with pytest.raises(SmaSunSpecException):
            await sma.discover()

    async def test_read_failure_wrapped(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """A transport-level read failure surfaces as SmaReadException, not raw ModbusError."""
        (header,) = _seed_sunspec_header(
            mock_modbus_unit, [(MODEL_ID_IMMEDIATE_CONTROLS, 4)]
        )
        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()  # succeeds before the failure below is configured

        mock_modbus_unit.fail_read(header, ModbusTimeoutError("timeout"))

        with pytest.raises(SmaReadException):
            await sma.get_control(ModbusControl.INVERTER_ENABLED)

    async def test_scale_factor_round_trip(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """A negative scale factor on a rate point scales correctly on write."""
        (header,) = _seed_sunspec_header(
            mock_modbus_unit, [(MODEL_ID_STORAGE_CONTROLS, 26)]
        )
        # _rte_sf = sunssf(25) -> exponent -1, so engineering value 50 <-> raw 500
        mock_modbus_unit.holding[header + 25] = 0x10000 - 1  # int16 -1 as uint16

        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()

        await sma.set_control(ModbusControl.STORAGE_CHARGE_RATE, 50)

        assert mock_modbus_unit.holding[header + 13] == 500  # in_w_rte raw register
        assert await sma.get_control(ModbusControl.STORAGE_CHARGE_RATE) == 50

    async def test_power_limit_lazy_enable(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """set_control(POWER_LIMIT, ...) arms WMaxLim_Ena only if not already armed."""
        (header,) = _seed_sunspec_header(
            mock_modbus_unit, [(MODEL_ID_IMMEDIATE_CONTROLS, 26)]
        )
        mock_modbus_unit.holding[header + 9] = WMaxLimEna.DISABLED  # w_max_lim_ena

        writes: list[int] = []
        mock_modbus_unit.on_write(
            lambda event, addr=header + 9: (
                writes.append(event.address) if event.address == addr else None
            )
        )

        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()

        await sma.set_control(ModbusControl.POWER_LIMIT, 42)
        assert mock_modbus_unit.holding[header + 9] == WMaxLimEna.ENABLED
        assert await sma.get_control(ModbusControl.POWER_LIMIT) == 42
        assert len(writes) == 1  # the gate was armed

        await sma.set_control(ModbusControl.POWER_LIMIT, 55)
        assert await sma.get_control(ModbusControl.POWER_LIMIT) == 55
        assert len(writes) == 1  # NOT re-armed the second time - already enabled

    async def test_reactive_power_wmax_pct_lazy_enable(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """set_control(REACTIVE_POWER_WMAX_PCT, ...) arms VArPct_Ena, only if needed.

        VArPct_Mod is read-only and fixed at WMAX on SMA devices - no mode
        gate to arm, unlike the earlier (incorrect) assumption that it could
        be switched. See VArPctMod's docstring.
        """
        (header,) = _seed_sunspec_header(
            mock_modbus_unit, [(MODEL_ID_IMMEDIATE_CONTROLS, 26)]
        )
        mock_modbus_unit.holding[header + 21] = VArPctMod.WMAX  # fixed on real hardware
        mock_modbus_unit.holding[header + 22] = VArPctEna.DISABLED

        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()

        await sma.set_control(ModbusControl.REACTIVE_POWER_WMAX_PCT, 30)
        assert mock_modbus_unit.holding[header + 22] == VArPctEna.ENABLED
        assert await sma.get_control(ModbusControl.REACTIVE_POWER_WMAX_PCT) == 30

    async def test_reactive_power_varmax_and_varaval_are_read_only(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """VArMaxPct/VArAvalPct are read-only on SMA devices - get works, set doesn't."""
        (header,) = _seed_sunspec_header(
            mock_modbus_unit, [(MODEL_ID_IMMEDIATE_CONTROLS, 26)]
        )
        mock_modbus_unit.holding[header + 16] = 42  # v_ar_max_pct
        mock_modbus_unit.holding[header + 17] = -7  # v_ar_aval_pct

        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()

        assert await sma.get_control(ModbusControl.REACTIVE_POWER_VARMAX_PCT) == 42
        assert await sma.get_control(ModbusControl.REACTIVE_POWER_VARAVAL_PCT) == -7

        with pytest.raises(SmaWriteException):
            await sma.set_control(ModbusControl.REACTIVE_POWER_VARMAX_PCT, 10)
        with pytest.raises(SmaWriteException):
            await sma.set_control(ModbusControl.REACTIVE_POWER_VARAVAL_PCT, 10)

    async def test_power_factor_scale_round_trip(
        self, mock_modbus_connection, mock_modbus_unit
    ) -> None:
        """A fractional power factor scales correctly via a negative scale factor."""
        (header,) = _seed_sunspec_header(
            mock_modbus_unit, [(MODEL_ID_IMMEDIATE_CONTROLS, 26)]
        )
        mock_modbus_unit.holding[header + 14] = OutPFSetEna.DISABLED
        # _out_pf_set_sf = sunssf(24) -> exponent -2, so 0.95 <-> raw 95
        mock_modbus_unit.holding[header + 24] = 0x10000 - 2  # int16 -2 as uint16

        sma = SMAModbus(connection=mock_modbus_connection, sunspec_unit_id=1)
        await sma.connect()
        await sma.discover()

        await sma.set_control(ModbusControl.POWER_FACTOR, 0.95)

        assert mock_modbus_unit.holding[header + 14] == OutPFSetEna.ENABLED
        assert mock_modbus_unit.holding[header + 10] == 95  # out_pf_set raw register
        assert await sma.get_control(ModbusControl.POWER_FACTOR) == 0.95
