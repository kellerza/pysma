from dataclasses import dataclass
from typing import Union

from .const import (
    DEVCLASS_BATTERY,
    DEVCLASS_ENERGY_METER,
    DEVCLASS_INVERTER,
    DEVICE_INFO,
    ENERGY_METER_VIA_INVERTER,
    JMESPATHS_TAG,
    OPTIMIZERS_VIA_INVERTER,
)


@dataclass
class Sensor:
    name: str
    key: str
    idx: str = "0"
    unit: str = ""
    factor: int = None
    path: Union[str, list, tuple] = None
    enabled: bool = True
    l10n_translate: bool = False
    value: Union[str, int] = None


# Status - Operation
status = Sensor("status", "6180_08214800", path=JMESPATHS_TAG, l10n=True)
operating_status_general = Sensor(
    "operating_status_general", "6180_08412800", path=JMESPATHS_TAG, l10n=True
)

# Status - Operation - Inverter
inverter_condition = Sensor(
    "inverter_condition", "6180_08414C00", path=JMESPATHS_TAG, l10n=True
)
inverter_system_init = Sensor(
    "inverter_system_init", "6800_08811F00", path=JMESPATHS_TAG, l10n=True
)
grid_connection_status = Sensor(
    "grid_connection_status", "6180_0846A700", path=JMESPATHS_TAG, l10n=True
)
grid_relay_status = Sensor(
    "grid_relay_status", "6180_08416400", path=JMESPATHS_TAG, l10n=True
)

# Inverter operating time
total_operating_time = Sensor(
    "total_operating_time", "6400_00462E00", unit="h", factor=3600
)
total_feedin_time = Sensor("total_feedin_time", "6400_00462F00", unit="h", factor=3600)

# DC side - DC measurements PV
pv_power_a = Sensor("pv_power_a", "6380_40251E00", idx="0", unit="W")
pv_power_b = Sensor("pv_power_b", "6380_40251E00", idx="1", unit="W")
pv_voltage_a = Sensor("pv_voltage_a", "6380_40451F00", idx="0", unit="V", factor=100)
pv_voltage_b = Sensor("pv_voltage_b", "6380_40451F00", idx="1", unit="V", factor=100)
pv_current_a = Sensor("pv_current_a", "6380_40452100", idx="0", unit="A", factor=1000)
pv_current_b = Sensor("pv_current_b", "6380_40452100", idx="1", unit="A", factor=1000)

# DC Side - Insulation monitoring
insulation_residual_current = Sensor(
    "insulation_residual_current", "6102_40254E00", unit="mA"
)

# AC Side - Grid measurements
grid_power = Sensor("grid_power", "6100_40263F00", unit="W")
frequency = Sensor("frequency", "6100_00465700", unit="Hz", factor=100)

# AC Side - Grid measurements - Active power
power_l1 = Sensor("power_l1", "6100_40464000", unit="W")
power_l2 = Sensor("power_l2", "6100_40464100", unit="W")
power_l3 = Sensor("power_l3", "6100_40464200", unit="W")

# AC Side - Grid measurements - Reactive power
grid_reactive_power = Sensor("grid_reactive_power", "6100_40265F00", unit="var")
grid_reactive_power_l1 = Sensor("grid_reactive_power_l1", "6100_40666000", unit="var")
grid_reactive_power_l2 = Sensor("grid_reactive_power_l2", "6100_40666100", unit="var")
grid_reactive_power_l3 = Sensor("grid_reactive_power_l3", "6100_40666200", unit="var")

# AC Side - Grid measurements - Apparent power
grid_apparent_power = Sensor("grid_apparent_power", "6100_40666700", unit="VA")
grid_apparent_power_l1 = Sensor("grid_apparent_power_l1", "6100_40666800", unit="VA")
grid_apparent_power_l2 = Sensor("grid_apparent_power_l2", "6100_40666900", unit="VA")
grid_apparent_power_l3 = Sensor("grid_apparent_power_l3", "6100_40666A00", unit="VA")


# AC Side - Grid measurements - Power factor
grid_power_factor = Sensor("grid_power_factor", "6100_00665900", unit="", factor=1000)
grid_power_factor_excitation = Sensor(
    "grid_power_factor_excitation", "6180_08465A00", path=JMESPATHS_TAG, l10n=True
)

# AC Side - Grid measurements - Phase Current
current_l1 = Sensor("current_l1", "6100_40465300", unit="A", factor=1000)
current_l2 = Sensor("current_l2", "6100_40465400", unit="A", factor=1000)
current_l3 = Sensor("current_l3", "6100_40465500", unit="A", factor=1000)
current_total = Sensor("current_total", "6100_00664F00", unit="A", factor=1000)

# AC Side - Grid measurements - Phase voltage
voltage_l1 = Sensor("voltage_l1", "6100_00464800", unit="V", factor=100)
voltage_l2 = Sensor("voltage_l2", "6100_00464900", unit="V", factor=100)
voltage_l3 = Sensor("voltage_l3", "6100_00464A00", unit="V", factor=100)

# AC Side - Measured values - energy
total_yield = Sensor("total_yield", "6400_00260100", unit="kWh", factor=1000)
daily_yield = Sensor("daily_yield", "6400_00262200", unit="Wh")

# AC Side - Measured values - Grid measurements
metering_power_supplied = Sensor("metering_power_supplied", "6100_40463600", unit="W")
metering_power_absorbed = Sensor("metering_power_absorbed", "6100_40463700", unit="W")
metering_frequency = Sensor(
    "metering_frequency", "6100_00468100", unit="Hz", factor=100
)
metering_total_yield = Sensor(
    "metering_total_yield", "6400_00462400", unit="kWh", factor=1000
)
metering_total_absorbed = Sensor(
    "metering_total_absorbed", "6400_00462500", unit="kWh", factor=1000
)

# AC Side - Measured values - Phase currents
metering_current_l1 = Sensor(
    "metering_current_l1", "6100_40466500", unit="A", factor=1000
)
metering_current_l2 = Sensor(
    "metering_current_l2", "6100_40466600", unit="A", factor=1000
)
metering_current_l3 = Sensor(
    "metering_current_l3", "6100_40466B00", unit="A", factor=1000
)

# AC Side - Measured values - Phase voltage
metering_voltage_l1 = Sensor(
    "metering_voltage_l1", "6100_0046E500", unit="V", factor=100
)
metering_voltage_l2 = Sensor(
    "metering_voltage_l2", "6100_0046E600", unit="V", factor=100
)
metering_voltage_l3 = Sensor(
    "metering_voltage_l3", "6100_0046E700", unit="V", factor=100
)

# AC Side - Electricity meter - Measured values - Active power feed-in
metering_active_power_l1 = Sensor("metering_active_power_l1", "6100_0046E800", unit="W")
metering_active_power_l2 = Sensor("metering_active_power_l2", "6100_0046E900", unit="W")
metering_active_power_l3 = Sensor("metering_active_power_l3", "6100_0046EA00", unit="W")

# AC Side - Electricity meter - Measured values - Active power drawn
metering_active_power_consumed_l1 = Sensor(
    "metering_active_power_consumed_l1", "6100_0046EB00", unit="W"
)
metering_active_power_consumed_l2 = Sensor(
    "metering_active_power_consumed_l2", "6100_0046EC00", unit="W"
)
metering_active_power_consumed_l3 = Sensor(
    "metering_active_power_consumed_l3", "6100_0046ED00", unit="W"
)

# AC Side - PV generation
pv_gen_meter = Sensor("pv_gen_meter", "6400_0046C300", unit="kWh", factor=1000)

# PV Inverter Optimizers
optimizer_serial = Sensor("optimizer_serial", "6800_10852600")
optimizer_power = Sensor("optimizer_power", "6100_40652A00", unit="W")
optimizer_current = Sensor("optimizer_current", "6100_40652900", unit="A", factor=1000)
optimizer_voltage = Sensor("optimizer_voltage", "6100_40652800", unit="V", factor=100)
optimizer_temp = Sensor("optimizer_temp", "6100_40652B00", unit="C", factor=10)


# Battery (inverter) - Battery (general parameters)
battery_soc_total = Sensor("battery_soc_total", "6100_00295A00", unit="%")
battery_soc_a = Sensor("battery_soc_a", "6100_00498F00", idx="0", unit="%")
battery_soc_b = Sensor("battery_soc_b", "6100_00498F00", idx="1", unit="%")
battery_soc_c = Sensor("battery_soc_c", "6100_00498F00", idx="2", unit="%")
battery_voltage_a = Sensor(
    "battery_voltage_a", "6100_00495C00", idx="0", unit="V", factor=100
)
battery_voltage_b = Sensor(
    "battery_voltage_b", "6100_00495C00", idx="1", unit="V", factor=100
)
battery_voltage_c = Sensor(
    "battery_voltage_c", "6100_00495C00", idx="2", unit="V", factor=100
)
battery_current_a = Sensor(
    "battery_current_a", "6100_40495D00", idx="0", unit="A", factor=1000
)
battery_current_b = Sensor(
    "battery_current_b", "6100_40495D00", idx="1", unit="A", factor=1000
)
battery_current_c = Sensor(
    "battery_current_c", "6100_40495D00", idx="2", unit="A", factor=1000
)
battery_temp_a = Sensor("battery_temp_a", "6100_40495B00", idx="0", unit="C", factor=10)
battery_temp_b = Sensor("battery_temp_b", "6100_40495B00", idx="1", unit="C", factor=10)
battery_temp_c = Sensor("battery_temp_c", "6100_40495B00", idx="2", unit="C", factor=10)
battery_status_operating_mode = Sensor(
    "battery_status_operating_mode", "6180_08495E00", path=JMESPATHS_TAG, l10n=True
)

# Battery (inverter) - Diagnosis
battery_capacity_total = Sensor("battery_capacity_total", "6100_00696E00", unit="%")
battery_capacity_a = Sensor("battery_capacity_a", "6100_00499100", idx="0", unit="%")
battery_capacity_b = Sensor("battery_capacity_b", "6100_00499100", idx="1", unit="%")
battery_capacity_c = Sensor("battery_capacity_c", "6100_00499100", idx="2", unit="%")

# Battery (inverter) - Charge (voltage)
battery_charging_voltage_a = Sensor(
    "battery_charging_voltage_a", "6102_00493500", idx="0", unit="V", factor=100
)
battery_charging_voltage_b = Sensor(
    "battery_charging_voltage_b", "6102_00493500", idx="1", unit="V", factor=100
)
battery_charging_voltage_c = Sensor(
    "battery_charging_voltage_c", "6102_00493500", idx="2", unit="V", factor=100
)

# Battery (inverter) - Battery charge (power & energy)
battery_power_charge_total = Sensor(
    "battery_power_charge_total", "6100_00496900", unit="W"
)
battery_power_charge_a = Sensor(
    "battery_power_charge_a", "6100_00499300", idx="0", unit="W"
)
battery_power_charge_b = Sensor(
    "battery_power_charge_b", "6100_00499300", idx="1", unit="W"
)
battery_power_charge_c = Sensor(
    "battery_power_charge_c", "6100_00499300", idx="2", unit="W"
)
battery_charge_total = Sensor(
    "battery_charge_total", "6400_00496700", unit="kWh", factor=1000
)
battery_charge_a = Sensor(
    "battery_charge_a", "6400_00499500", idx="0", unit="kWh", factor=1000
)
battery_charge_b = Sensor(
    "battery_charge_b", "6400_00499500", idx="1", unit="kWh", factor=1000
)
battery_charge_c = Sensor(
    "battery_charge_c", "6400_00499500", idx="2", unit="kWh", factor=1000
)

# Battery (inverter) - Battery discharge (power & energy)
battery_power_discharge_total = Sensor(
    "battery_power_discharge_total", "6100_00496A00", unit="W"
)
battery_power_discharge_a = Sensor(
    "battery_power_discharge_a", "6100_00499400", idx="0", unit="W"
)
battery_power_discharge_b = Sensor(
    "battery_power_discharge_b", "6100_00499400", idx="1", unit="W"
)
battery_power_discharge_c = Sensor(
    "battery_power_discharge_c", "6100_00499400", idx="2", unit="W"
)
battery_discharge_total = Sensor(
    "battery_discharge_total", "6400_00496800", unit="kWh", factor=1000
)
battery_discharge_a = Sensor(
    "battery_discharge_a", "6400_00499600", idx="0", unit="kWh", factor=1000
)
battery_discharge_b = Sensor(
    "battery_discharge_b", "6400_00499600", idx="1", unit="kWh", factor=1000
)
battery_discharge_c = Sensor(
    "battery_discharge_c", "6400_00499600", idx="2", unit="kWh", factor=1000
)

# Device Parameters
# Type Label - Type Label
serial_number = Sensor("serial_number", "6800_00A21E00")
device_name = Sensor("device_name", "6800_10821E00")
device_type = Sensor("device_type", "6800_08822000", path=JMESPATHS_TAG, l10n=True)
device_manufacturer = Sensor(
    "device_manufacturer", "6800_08822B00", path=JMESPATHS_TAG, l10n=True
)

# Device - Inverter
inverter_power_limit = Sensor("inverter_power_limit", "6800_00832A00", unit="W")

# System communication - Meter on Speedwire
energy_meter = Sensor("energy_meter", "6800_008AA300")


sensor_map = {
    DEVCLASS_INVERTER: [
        status,
        pv_power_a,
        pv_power_b,
        pv_voltage_a,
        pv_voltage_b,
        pv_current_a,
        pv_current_b,
        grid_power,
        frequency,
        current_l1,
        current_l2,
        current_l3,
        voltage_l1,
        voltage_l2,
        voltage_l3,
        power_l1,
        power_l2,
        power_l3,
        total_yield,
        daily_yield,
        pv_gen_meter,
    ],
    OPTIMIZERS_VIA_INVERTER: [
        optimizer_power,
        optimizer_current,
        optimizer_voltage,
        optimizer_temp,
    ],
    ENERGY_METER_VIA_INVERTER: [
        metering_power_supplied,
        metering_power_absorbed,
        metering_total_yield,
        metering_total_absorbed,
        metering_current_l1,
        metering_current_l2,
        metering_current_l3,
        metering_voltage_l1,
        metering_voltage_l2,
        metering_voltage_l3,
        metering_active_power_l1,
        metering_active_power_l2,
        metering_active_power_l3,
        metering_active_power_consumed_l1,
        metering_active_power_consumed_l2,
        metering_active_power_consumed_l3,
    ],
    DEVCLASS_BATTERY: [
        battery_voltage_a,
        battery_voltage_b,
        battery_voltage_c,
        battery_charging_voltage_a,
        battery_charging_voltage_b,
        battery_charging_voltage_c,
        battery_current_a,
        battery_current_b,
        battery_current_c,
        inverter_power_limit,
        battery_power_charge_total,
        battery_power_charge_a,
        battery_power_charge_b,
        battery_power_charge_c,
        battery_power_discharge_total,
        battery_power_discharge_a,
        battery_power_discharge_b,
        battery_power_discharge_c,
        grid_reactive_power,
        grid_reactive_power_l1,
        grid_reactive_power_l2,
        grid_reactive_power_l3,
        grid_apparent_power,
        grid_apparent_power_l1,
        grid_apparent_power_l2,
        grid_apparent_power_l3,
        grid_power_factor,
        grid_power_factor_excitation,
        battery_charge_total,
        battery_charge_a,
        battery_charge_b,
        battery_charge_c,
        battery_discharge_total,
        battery_discharge_a,
        battery_discharge_b,
        battery_discharge_c,
        battery_soc_total,
        battery_soc_a,
        battery_soc_b,
        battery_soc_c,
        battery_capacity_total,
        battery_capacity_a,
        battery_capacity_b,
        battery_capacity_c,
        battery_temp_a,
        battery_temp_b,
        battery_temp_c,
        insulation_residual_current,
        inverter_condition,
        operating_status_general,
        battery_status_operating_mode,
        grid_relay_status,
        grid_connection_status,
        inverter_system_init,
        grid_power,
        voltage_l1,
        voltage_l2,
        voltage_l3,
        current_l1,
        current_l2,
        current_l3,
        current_total,
        frequency,
        status,
    ],
    DEVCLASS_ENERGY_METER: [
        status,
        grid_power,
        frequency,
        current_l1,
        current_l2,
        current_l3,
        voltage_l1,
        voltage_l2,
        voltage_l3,
        power_l1,
        power_l2,
        power_l3,
    ],
    DEVICE_INFO: [
        serial_number,
        device_name,
        device_type,
        device_manufacturer,
    ],
}
