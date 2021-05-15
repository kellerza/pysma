"""Constants for SMA WebConnect library for Python. """
URL_LOGIN = "/dyn/login.json"
URL_LOGOUT = "/dyn/logout.json"
URL_VALUES = "/dyn/getValues.json"
URL_LOGGER = "/dyn/getLogger.json"
URL_DASH_LOGGER = "/dyn/getDashLogger.json"
URL_DASH_VALUES = "/dyn/getDashValues.json"

USERS = {"user": "usr", "installer": "istl"}

JMESPATH_BASE = "result.*"

JMESPATH_VAL = "val"
JMESPATH_VAL_TAG = JMESPATH_VAL + "[0].tag"
JMESPATH_VAL_IDX = '"{}"[{}].val'
JMESPATH_VAL_IDX_TAG = JMESPATH_VAL_IDX + "[0].tag"
JMESPATHS_TAG = (JMESPATH_VAL_IDX_TAG, JMESPATH_VAL_TAG)

LEGACY_MAP = {
    "pv_power": {"old_key": "6100_0046C200", "new_sensor": "pv_power_a"},
    "pv_voltage": {
        "old_key": "6380_40451F00",
        "new_sensor": "pv_power_a",
    },
    "pv_current": {
        "old_key": "6380_40452100",
        "new_sensor": "pv_current_a",
    },
}

FALLBACK_DEVICE_INFO = {
    "manufacturer": "SMA",
    "name": "SMA Device",
    "type": "",
    "serial": "9999999999",
}

DEVCLASS_INVERTER = "1"
DEVCLASS_BATTERY = "7"
DEVCLASS_ENERGY_METER = "65"
OPTIMIZERS_VIA_INVERTER = "253"
ENERGY_METER_VIA_INVERTER = "254"
DEVICE_INFO = "255"

SNAME = "name"
SKEY = "key"
SUNIT = "unit"
SFACTOR = "factor"
SPATH = "path"
SL10N = "l10n_translate"

# Status - Operation
SENSOR_STATUS = {
    SKEY: "6180_08214800",
    SNAME: "status",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_OPERATING_STATUS_GENERAL = {
    SKEY: "6180_08412800",
    SNAME: "operating_status_general",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}

# Status - Operation - Inverter
SENSOR_INVERTER_CONDITION = {
    SKEY: "6180_08414C00",
    SNAME: "inverter_condition",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_INVERTER_SYSTEM_INIT = {
    SKEY: "6800_08811F00",
    SNAME: "inverter_system_init",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_GRID_CONNECTION_STATUS = {
    SKEY: "6180_0846A700",
    SNAME: "grid_connection_status",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_GRID_RELAY_STATUS = {
    SKEY: "6180_08416400",
    SNAME: "grid_relay_status",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}

# Inverter operating time
SENSOR_TOTAL_OPERATING_TIME = {
    SKEY: "6400_00462E00",
    SNAME: "total_operating_time",
    SUNIT: "h",
    SFACTOR: 3600,
}
SENSOR_TOTAL_FEEDIN_TIME = {
    SKEY: "6400_00462F00",
    SNAME: "total_feedin_time",
    SUNIT: "h",
    SFACTOR: 3600,
}

# DC side - DC measurements PV
SENSOR_PV_POWER_A = {
    SKEY: "6380_40251E00_0",
    SNAME: "pv_power_a",
    SUNIT: "W",
}
SENSOR_PV_POWER_B = {
    SKEY: "6380_40251E00_1",
    SNAME: "pv_power_b",
    SUNIT: "W",
}
SENSOR_PV_VOLTAGE_A = {
    SKEY: "6380_40451F00_0",
    SNAME: "pv_voltage_a",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_PV_VOLTAGE_B = {
    SKEY: "6380_40451F00_1",
    SNAME: "pv_voltage_b",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_PV_CURRENT_A = {
    SKEY: "6380_40452100_0",
    SNAME: "pv_current_a",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_PV_CURRENT_B = {
    SKEY: "6380_40452100_1",
    SNAME: "pv_current_b",
    SUNIT: "A",
    SFACTOR: 1000,
}

# AC Side - Grid measurements
SENSOR_GRID_POWER = {
    SKEY: "6100_40263F00",
    SNAME: "grid_power",
    SUNIT: "W",
}
SENSOR_FREQUENCY = {
    SKEY: "6100_00465700",
    SNAME: "frequency",
    SUNIT: "Hz",
    SFACTOR: 100,
}

# AC Side - Grid measurements - Active power
SENSOR_POWER_L1 = {
    SKEY: "6100_40464000",
    SNAME: "power_l1",
    SUNIT: "W",
}
SENSOR_POWER_L2 = {
    SKEY: "6100_40464100",
    SNAME: "power_l2",
    SUNIT: "W",
}
SENSOR_POWER_L3 = {
    SKEY: "6100_40464200",
    SNAME: "power_l3",
    SUNIT: "W",
}

# AC Side - Grid measurements - reactive power, apparent power and power factor
SENSOR_GRID_REACTIVE_POWER = {
    SKEY: "6100_40265F00",
    SNAME: "grid_reactive_power",
    SUNIT: "var",
}
SENSOR_GRID_REACTIVE_POWER_L1 = {
    SKEY: "6100_40666000",
    SNAME: "grid_reactive_power_l1",
    SUNIT: "var",
}
SENSOR_GRID_REACTIVE_POWER_L2 = {
    SKEY: "6100_40666100",
    SNAME: "grid_reactive_power_l2",
    SUNIT: "var",
}
SENSOR_GRID_REACTIVE_POWER_L3 = {
    SKEY: "6100_40666200",
    SNAME: "grid_reactive_power_l3",
    SUNIT: "var",
}
SENSOR_GRID_APPARENT_POWER = {
    SKEY: "6100_40666700",
    SNAME: "grid_apparent_power",
    SUNIT: "VA",
}
SENSOR_GRID_APPARENT_POWER_L1 = {
    SKEY: "6100_40666800",
    SNAME: "grid_apparent_power_l1",
    SUNIT: "VA",
}
SENSOR_GRID_APPARENT_POWER_L2 = {
    SKEY: "6100_40666900",
    SNAME: "grid_apparent_power_l2",
    SUNIT: "VA",
}
SENSOR_GRID_APPARENT_POWER_L3 = {
    SKEY: "6100_40666A00",
    SNAME: "grid_apparent_power_l3",
    SUNIT: "VA",
}
SENSOR_GRID_POWER_FACTOR = {
    SKEY: "6100_00665900",
    SNAME: "grid_power_factor",
    SUNIT: "",
    SFACTOR: 1000,
}
SENSOR_GRID_POWER_FACTOR_EXCITATION = {
    SKEY: "6180_08465A00",
    SNAME: "grid_power_factor_excitation",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}

# AC Side - Grid measurements - frequency
# AC Side - Grid measurements - current
SENSOR_CURRENT_L1 = {
    SKEY: "6100_40465300",
    SNAME: "current_l1",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_CURRENT_L2 = {
    SKEY: "6100_40465400",
    SNAME: "current_l2",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_CURRENT_L3 = {
    SKEY: "6100_40465500",
    SNAME: "current_l3",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_CURRENT_TOTAL = {
    SKEY: "6100_00664F00",
    SNAME: "current_total",
    SUNIT: "A",
    SFACTOR: 1000,
}

# AC Side - Grid measurements - phase voltage
SENSOR_VOLTAGE_L1 = {
    SKEY: "6100_00464800",
    SNAME: "voltage_l1",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_VOLTAGE_L2 = {
    SKEY: "6100_00464900",
    SNAME: "voltage_l2",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_VOLTAGE_L3 = {
    SKEY: "6100_00464A00",
    SNAME: "voltage_l3",
    SUNIT: "V",
    SFACTOR: 100,
}

# AC Side - Measured values - energy
SENSOR_TOTAL_YIELD = {
    SKEY: "6400_00260100",
    SNAME: "total_yield",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_DAILY_YIELD = {
    SKEY: "6400_00262200",
    SNAME: "daily_yield",
    SUNIT: "Wh",
}

# AC Side - Measured values - Grid measurements
SENSOR_METERING_POWER_SUPPLIED = {
    SKEY: "6100_40463600",
    SNAME: "metering_power_supplied",
    SUNIT: "W",
}
SENSOR_METERING_POWER_ABSORBED = {
    SKEY: "6100_40463700",
    SNAME: "metering_power_absorbed",
    SUNIT: "W",
}
SENSOR_METERING_FREQUENCY = {
    SKEY: "6100_00468100",
    SNAME: "metering_frequency",
    SUNIT: "Hz",
    SFACTOR: 100,
}
SENSOR_METERING_TOTAL_YIELD = {
    SKEY: "6400_00462400",
    SNAME: "metering_total_yield",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_METERING_TOTAL_ABSORBED = {
    SKEY: "6400_00462500",
    SNAME: "metering_total_absorbed",
    SUNIT: "kWh",
    SFACTOR: 1000,
}

# AC Side - Measured values - Phase currents
SENSOR_METERING_CURRENT_L1 = {
    SKEY: "6100_40466500",
    SNAME: "metering_current_l1",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_METERING_CURRENT_L2 = {
    SKEY: "6100_40466600",
    SNAME: "metering_current_l2",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_METERING_CURRENT_L3 = {
    SKEY: "6100_40466B00",
    SNAME: "metering_current_l3",
    SUNIT: "A",
    SFACTOR: 1000,
}

# AC Side - Measured values - Phase voltage
SENSOR_METERING_VOLTAGE_L1 = {
    SKEY: "6100_0046E500",
    SNAME: "metering_voltage_l1",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_METERING_VOLTAGE_L2 = {
    SKEY: "6100_0046E600",
    SNAME: "metering_voltage_l2",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_METERING_VOLTAGE_L3 = {
    SKEY: "6100_0046E700",
    SNAME: "metering_voltage_l3",
    SUNIT: "V",
    SFACTOR: 100,
}

# AC Side - Electricity meter - Measured values - Active power feed-in
SENSOR_METERING_ACTIVE_POWER_L1 = {
    SKEY: "6100_0046E800",
    SNAME: "metering_active_power_l1",
    SUNIT: "W",
}
SENSOR_METERING_ACTIVE_POWER_L2 = {
    SKEY: "6100_0046E900",
    SNAME: "metering_active_power_l2",
    SUNIT: "W",
}
SENSOR_METERING_ACTIVE_POWER_L3 = {
    SKEY: "6100_0046EA00",
    SNAME: "metering_active_power_l3",
    SUNIT: "W",
}

# AC Side - Electricity meter - Measured values - Active power drawn
SENSOR_METERING_ACTIVE_POWER_CONSUMED_L1 = {
    SKEY: "6100_0046EB00",
    SNAME: "metering_active_power_consumed_l1",
    SUNIT: "W",
}
SENSOR_METERING_ACTIVE_POWER_CONSUMED_L2 = {
    SKEY: "6100_0046EC00",
    SNAME: "metering_active_power_consumed_l2",
    SUNIT: "W",
}
SENSOR_METERING_ACTIVE_POWER_CONSUMED_L3 = {
    SKEY: "6100_0046ED00",
    SNAME: "metering_active_power_consumed_l3",
    SUNIT: "W",
}

# AC Side - PV generation
SENSOR_PV_GEN_METER = {
    SKEY: "6400_0046C300",
    SNAME: "pv_gen_meter",
    SUNIT: "kWh",
    SFACTOR: 1000,
}

# PV Inverter Optimizers
SENSOR_OPTIMIZER_SERIAL = {
    SKEY: "6800_10852600",
    SNAME: "optimizer_serial",
}
SENSOR_OPTIMIZER_POWER = {
    SKEY: "6100_40652A00",
    SNAME: "optimizer_power",
    SUNIT: "W",
}
SENSOR_OPTIMIZER_CURRENT = {
    SKEY: "6100_40652900",
    SNAME: "optimizer_current",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_OPTIMIZER_VOLTAGE = {
    SKEY: "6100_40652800",
    SNAME: "optimizer_voltage",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_OPTIMIZER_TEMP = {
    SKEY: "6100_40652B00",
    SNAME: "optimizer_temp",
    SUNIT: "C",
    SFACTOR: 10,
}


# Battery (inverter) related sensors
SENSOR_BATTERY_VOLTAGE_A = {
    SKEY: "6100_00495C00_0",
    SNAME: "battery_voltage_a",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_VOLTAGE_B = {
    SKEY: "6100_00495C00_1",
    SNAME: "battery_voltage_b",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_VOLTAGE_C = {
    SKEY: "6100_00495C00_2",
    SNAME: "battery_voltage_c",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_CHARGING_VOLTAGE_A = {
    SKEY: "6102_00493500_0",
    SNAME: "battery_charging_voltage_a",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_CHARGING_VOLTAGE_B = {
    SKEY: "6102_00493500_1",
    SNAME: "battery_charging_voltage_b",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_CHARGING_VOLTAGE_C = {
    SKEY: "6102_00493500_2",
    SNAME: "battery_charging_voltage_c",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_CURRENT_A = {
    SKEY: "6100_40495D00_0",
    SNAME: "battery_current_a",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_BATTERY_CURRENT_B = {
    SKEY: "6100_40495D00_1",
    SNAME: "battery_current_b",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_BATTERY_CURRENT_C = {
    SKEY: "6100_40495D00_2",
    SNAME: "battery_current_c",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_BATTERY_POWER_CHARGE_TOTAL = {
    SKEY: "6100_00496900",
    SNAME: "battery_power_charge_total",
    SUNIT: "W",
}
SENSOR_BATTERY_POWER_CHARGE_A = {
    SKEY: "6100_00499300_0",
    SNAME: "battery_power_charge_a",
    SUNIT: "W",
}
SENSOR_BATTERY_POWER_CHARGE_B = {
    SKEY: "6100_00499300_1",
    SNAME: "battery_power_charge_b",
    SUNIT: "W",
}
SENSOR_BATTERY_POWER_CHARGE_C = {
    SKEY: "6100_00499300_2",
    SNAME: "battery_power_charge_c",
    SUNIT: "W",
}
SENSOR_BATTERY_POWER_DISCHARGE_TOTAL = {
    SKEY: "6100_00496A00",
    SNAME: "battery_power_discharge_total",
    SUNIT: "W",
}
SENSOR_BATTERY_POWER_DISCHARGE_A = {
    SKEY: "6100_00499400_0",
    SNAME: "battery_power_discharge_a",
    SUNIT: "W",
}
SENSOR_BATTERY_POWER_DISCHARGE_B = {
    SKEY: "6100_00499400_1",
    SNAME: "battery_power_discharge_b",
    SUNIT: "W",
}
SENSOR_BATTERY_POWER_DISCHARGE_C = {
    SKEY: "6100_00499400_2",
    SNAME: "battery_power_discharge_c",
    SUNIT: "W",
}
SENSOR_BATTERY_CHARGE_TOTAL = {
    SKEY: "6400_00496700",
    SNAME: "battery_charge_total",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_CHARGE_A = {
    SKEY: "6400_00499500_0",
    SNAME: "battery_charge_a",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_CHARGE_B = {
    SKEY: "6400_00499500_1",
    SNAME: "battery_charge_b",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_CHARGE_C = {
    SKEY: "6400_00499500_2",
    SNAME: "battery_charge_c",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_DISCHARGE_TOTAL = {
    SKEY: "6400_00496800",
    SNAME: "battery_discharge_total",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_DISCHARGE_A = {
    SKEY: "6400_00499600_0",
    SNAME: "battery_discharge_a",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_DISCHARGE_B = {
    SKEY: "6400_00499600_1",
    SNAME: "battery_discharge_b",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_DISCHARGE_C = {
    SKEY: "6400_00499600_2",
    SNAME: "battery_discharge_c",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_SOC_TOTAL = {
    SKEY: "6100_00295A00",
    SNAME: "battery_soc_total",
    SUNIT: "%",
}
SENSOR_BATTERY_SOC_A = {
    SKEY: "6100_00498F00_0",
    SNAME: "battery_soc_a",
    SUNIT: "%",
}
SENSOR_BATTERY_SOC_B = {
    SKEY: "6100_00498F00_1",
    SNAME: "battery_soc_b",
    SUNIT: "%",
}
SENSOR_BATTERY_SOC_C = {
    SKEY: "6100_00498F00_2",
    SNAME: "battery_soc_c",
    SUNIT: "%",
}
SENSOR_BATTERY_CAPACITY_TOTAL = {
    SKEY: "6100_00696E00",
    SNAME: "battery_capacity_total",
    SUNIT: "%",
}
SENSOR_BATTERY_CAPACITY_A = {
    SKEY: "6100_00499100_0",
    SNAME: "battery_capacity_a",
    SUNIT: "%",
}
SENSOR_BATTERY_CAPACITY_B = {
    SKEY: "6100_00499100_1",
    SNAME: "battery_capacity_b",
    SUNIT: "%",
}
SENSOR_BATTERY_CAPACITY_C = {
    SKEY: "6100_00499100_2",
    SNAME: "battery_capacity_c",
    SUNIT: "%",
}
SENSOR_BATTERY_TEMP_A = {
    SKEY: "6100_40495B00_0",
    SNAME: "battery_temp_a",
    SUNIT: "C",
    SFACTOR: 10,
}
SENSOR_BATTERY_TEMP_B = {
    SKEY: "6100_40495B00_1",
    SNAME: "battery_temp_b",
    SUNIT: "C",
    SFACTOR: 10,
}
SENSOR_BATTERY_TEMP_C = {
    SKEY: "6100_40495B00_2",
    SNAME: "battery_temp_c",
    SUNIT: "C",
    SFACTOR: 10,
}
SENSOR_BATTERY_STATUS_OPERATING_MODE = {
    SKEY: "6180_08495E00",
    SNAME: "battery_status_operating_mode",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_INSULATION_RESIDUAL_CURRENT = {
    SKEY: "6102_40254E00",
    SNAME: "insulation_residual_current",
    SUNIT: "mA",
}


# Device Parameters
# Type Label - Type Label
SENSOR_SERIAL_NUMBER = {
    SKEY: "6800_00A21E00",
    SNAME: "serial_number",
}
SENSOR_DEVICE_NAME = {
    SKEY: "6800_10821E00",
    SNAME: "device_name",
}
SENSOR_DEVICE_TYPE = {
    SKEY: "6800_08822000",
    SNAME: "device_type",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_DEVICE_MANUFACTURER = {
    SKEY: "6800_08822B00",
    SNAME: "device_manufacturer",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}

# Device - Inverter
SENSOR_INVERTER_POWER_LIMIT = {
    SKEY: "6800_00832A00",
    SNAME: "inverter_power_limit",
    SUNIT: "W",
}

# System communication - Meter on Speedwire
SENSOR_ENERGY_METER = {
    SKEY: "6800_008AA300",
    SNAME: "energy_meter",
}


SENSOR_MAP = {
    DEVCLASS_INVERTER: [
        SENSOR_STATUS,
        SENSOR_PV_POWER_A,
        SENSOR_PV_POWER_B,
        SENSOR_PV_VOLTAGE_A,
        SENSOR_PV_VOLTAGE_B,
        SENSOR_PV_CURRENT_A,
        SENSOR_PV_CURRENT_B,
        SENSOR_GRID_POWER,
        SENSOR_FREQUENCY,
        SENSOR_CURRENT_L1,
        SENSOR_CURRENT_L2,
        SENSOR_CURRENT_L3,
        SENSOR_VOLTAGE_L1,
        SENSOR_VOLTAGE_L2,
        SENSOR_VOLTAGE_L3,
        SENSOR_POWER_L1,
        SENSOR_POWER_L2,
        SENSOR_POWER_L3,
        SENSOR_TOTAL_YIELD,
        SENSOR_DAILY_YIELD,
        SENSOR_PV_GEN_METER,
    ],
    OPTIMIZERS_VIA_INVERTER: [
        SENSOR_OPTIMIZER_POWER,
        SENSOR_OPTIMIZER_CURRENT,
        SENSOR_OPTIMIZER_VOLTAGE,
        SENSOR_OPTIMIZER_TEMP,
    ],
    ENERGY_METER_VIA_INVERTER: [
        SENSOR_METERING_POWER_SUPPLIED,
        SENSOR_METERING_POWER_ABSORBED,
        SENSOR_METERING_TOTAL_YIELD,
        SENSOR_METERING_TOTAL_ABSORBED,
        SENSOR_METERING_CURRENT_L1,
        SENSOR_METERING_CURRENT_L2,
        SENSOR_METERING_CURRENT_L3,
        SENSOR_METERING_VOLTAGE_L1,
        SENSOR_METERING_VOLTAGE_L2,
        SENSOR_METERING_VOLTAGE_L3,
        SENSOR_METERING_ACTIVE_POWER_L1,
        SENSOR_METERING_ACTIVE_POWER_L2,
        SENSOR_METERING_ACTIVE_POWER_L3,
        SENSOR_METERING_ACTIVE_POWER_CONSUMED_L1,
        SENSOR_METERING_ACTIVE_POWER_CONSUMED_L2,
        SENSOR_METERING_ACTIVE_POWER_CONSUMED_L3,
    ],
    DEVCLASS_BATTERY: [
        SENSOR_BATTERY_VOLTAGE_A,
        SENSOR_BATTERY_VOLTAGE_B,
        SENSOR_BATTERY_VOLTAGE_C,
        SENSOR_BATTERY_CHARGING_VOLTAGE_A,
        SENSOR_BATTERY_CHARGING_VOLTAGE_B,
        SENSOR_BATTERY_CHARGING_VOLTAGE_C,
        SENSOR_BATTERY_CURRENT_A,
        SENSOR_BATTERY_CURRENT_B,
        SENSOR_BATTERY_CURRENT_C,
        SENSOR_INVERTER_POWER_LIMIT,
        SENSOR_BATTERY_POWER_CHARGE_TOTAL,
        SENSOR_BATTERY_POWER_CHARGE_A,
        SENSOR_BATTERY_POWER_CHARGE_B,
        SENSOR_BATTERY_POWER_CHARGE_C,
        SENSOR_BATTERY_POWER_DISCHARGE_TOTAL,
        SENSOR_BATTERY_POWER_DISCHARGE_A,
        SENSOR_BATTERY_POWER_DISCHARGE_B,
        SENSOR_BATTERY_POWER_DISCHARGE_C,
        SENSOR_GRID_REACTIVE_POWER,
        SENSOR_GRID_REACTIVE_POWER_L1,
        SENSOR_GRID_REACTIVE_POWER_L2,
        SENSOR_GRID_REACTIVE_POWER_L3,
        SENSOR_GRID_APPARENT_POWER,
        SENSOR_GRID_APPARENT_POWER_L1,
        SENSOR_GRID_APPARENT_POWER_L2,
        SENSOR_GRID_APPARENT_POWER_L3,
        SENSOR_GRID_POWER_FACTOR,
        SENSOR_GRID_POWER_FACTOR_EXCITATION,
        SENSOR_BATTERY_CHARGE_TOTAL,
        SENSOR_BATTERY_CHARGE_A,
        SENSOR_BATTERY_CHARGE_B,
        SENSOR_BATTERY_CHARGE_C,
        SENSOR_BATTERY_DISCHARGE_TOTAL,
        SENSOR_BATTERY_DISCHARGE_A,
        SENSOR_BATTERY_DISCHARGE_B,
        SENSOR_BATTERY_DISCHARGE_C,
        SENSOR_BATTERY_SOC_TOTAL,
        SENSOR_BATTERY_SOC_A,
        SENSOR_BATTERY_SOC_B,
        SENSOR_BATTERY_SOC_C,
        SENSOR_BATTERY_CAPACITY_TOTAL,
        SENSOR_BATTERY_CAPACITY_A,
        SENSOR_BATTERY_CAPACITY_B,
        SENSOR_BATTERY_CAPACITY_C,
        SENSOR_BATTERY_TEMP_A,
        SENSOR_BATTERY_TEMP_B,
        SENSOR_BATTERY_TEMP_C,
        SENSOR_INSULATION_RESIDUAL_CURRENT,
        SENSOR_INVERTER_CONDITION,
        SENSOR_OPERATING_STATUS_GENERAL,
        SENSOR_BATTERY_STATUS_OPERATING_MODE,
        SENSOR_GRID_RELAY_STATUS,
        SENSOR_GRID_CONNECTION_STATUS,
        SENSOR_INVERTER_SYSTEM_INIT,
        SENSOR_GRID_POWER,
        SENSOR_VOLTAGE_L1,
        SENSOR_VOLTAGE_L2,
        SENSOR_VOLTAGE_L3,
        SENSOR_CURRENT_L1,
        SENSOR_CURRENT_L2,
        SENSOR_CURRENT_L3,
        SENSOR_CURRENT_TOTAL,
        SENSOR_FREQUENCY,
        SENSOR_STATUS,
    ],
    DEVCLASS_ENERGY_METER: [
        SENSOR_STATUS,
        SENSOR_GRID_POWER,
        SENSOR_FREQUENCY,
        SENSOR_CURRENT_L1,
        SENSOR_CURRENT_L2,
        SENSOR_CURRENT_L3,
        SENSOR_VOLTAGE_L1,
        SENSOR_VOLTAGE_L2,
        SENSOR_VOLTAGE_L3,
        SENSOR_POWER_L1,
        SENSOR_POWER_L2,
        SENSOR_POWER_L3,
    ],
    DEVICE_INFO: [
        SENSOR_SERIAL_NUMBER,
        SENSOR_DEVICE_NAME,
        SENSOR_DEVICE_TYPE,
        SENSOR_DEVICE_MANUFACTURER,
    ],
}
