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

# DC side - DC measurements
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

# AC Side - Grid measurements - Phase currents
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

# AC Side - Grid measurements - Phase voltage
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

# AC Side - Measured values
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

# AC Side - Measured values - Active power
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

# AC Side - Measured values - Active power consumed
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

# Inverter Optimizers
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


# Battery related sensors
SENSOR_BATTERY_SOC = [
    "6100_00295A00_0",
    "battery_soc",
    "%",
]
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
        SENSOR_BATTERY_SOC,
        SENSOR_BATTERY_TEMP_A,
        SENSOR_BATTERY_TEMP_B,
        SENSOR_BATTERY_TEMP_C,
        SENSOR_BATTERY_VOLTAGE_A,
        SENSOR_BATTERY_VOLTAGE_B,
        SENSOR_BATTERY_VOLTAGE_C,
        SENSOR_BATTERY_CURRENT_A,
        SENSOR_BATTERY_CURRENT_B,
        SENSOR_BATTERY_CURRENT_C,
        SENSOR_GRID_POWER,
        SENSOR_STATUS,
    ],
    DEVCLASS_ENERGY_METER: [
        SENSOR_GRID_POWER,
        SENSOR_POWER_L1,
        SENSOR_POWER_L2,
        SENSOR_POWER_L3,
        SENSOR_FREQUENCY,
        SENSOR_VOLTAGE_L1,
        SENSOR_VOLTAGE_L2,
        SENSOR_VOLTAGE_L3,
        SENSOR_CURRENT_L1,
        SENSOR_CURRENT_L2,
        SENSOR_CURRENT_L3,
        SENSOR_STATUS,
    ],
    DEVICE_INFO: [
        SENSOR_SERIAL_NUMBER,
        SENSOR_DEVICE_NAME,
        SENSOR_DEVICE_TYPE,
        SENSOR_DEVICE_MANUFACTURER,
    ],
}
