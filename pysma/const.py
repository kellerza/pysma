URL_LOGIN = "/dyn/login.json"
URL_LOGOUT = "/dyn/logout.json"
URL_VALUES = "/dyn/getValues.json"
URL_LOGGER = "/dyn/getLogger.json"
URL_DASH_LOGGER = "/dyn/getDashLogger.json"
URL_DASH_VALUES = "/dyn/getDashValues.json"

USERS = {"user": "usr", "installer": "istl"}

JMESPATH_BASE = "result.*"
JMESPATH_VAL_IDX = '"{}"[{}].val'
JMESPATH_VAL = "val"

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
ENERGY_METER_VIA_INVERTER = "254"
DEVICE_INFO = "255"

SNAME = "name"
SKEY = "key"
SUNIT = "unit"
SFACTOR = "factor"
SPATH = "path"
SL10N = "l10n_translate"

SENSOR_GRID_POWER = {SKEY: "6100_40263F00", SNAME: "grid_power", SUNIT: "W"}
SENSOR_POWER_L1 = {SKEY: "6100_40464000", SNAME: "power_l1", SUNIT: "W"}
SENSOR_POWER_L2 = {SKEY: "6100_40464100", SNAME: "power_l2", SUNIT: "W"}
SENSOR_POWER_L3 = {SKEY: "6100_40464200", SNAME: "power_l3", SUNIT: "W"}
SENSOR_FREQUENCY = {
    SKEY: "6100_00465700",
    SNAME: "frequency",
    SUNIT: "Hz",
    SFACTOR: 100,
}
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

# DC side - PV Generation
#   Power form the panels: pv_power_a (similar to old pv_power)
#   Old 6100_0046C200 is the power generated by the inverter (always equal to grid_power)
SENSOR_PV_POWER_A = {SKEY: "6380_40251E00_0", SNAME: "pv_power_a", SUNIT: "W"}
SENSOR_PV_POWER_B = {SKEY: "6380_40251E00_1", SNAME: "pv_power_b", SUNIT: "W"}
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
SENSOR_PV_GEN_METER = {
    SKEY: "6400_0046C300",
    SNAME: "pv_gen_meter",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_TOTAL_YIELD = {
    SKEY: "6400_00260100",
    SNAME: "total_yield",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_DAILY_YIELD = {SKEY: "6400_00262200", SNAME: "daily_yield", SUNIT: "Wh"}
# AC side - Measured values - Grid measurements
SENSOR_GRID_POWER_SUPPLIED = {
    SKEY: "6100_40463600",
    SNAME: "grid_power_supplied",
    SUNIT: "W",
}
SENSOR_GRID_POWER_ABSORBED = {
    SKEY: "6100_40463700",
    SNAME: "grid_power_absorbed",
    SUNIT: "W",
}
SENSOR_GRID_TOTAL_YIELD = {
    SKEY: "6400_00462400",
    SNAME: "grid_total_yield",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_GRID_TOTAL_ABSORBED = {
    SKEY: "6400_00462500",
    SNAME: "grid_total_absorbed",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
# Consumption = Energy from the PV system and grid
SENSOR_CURRENT_CONSUMPTION = {
    SKEY: "6100_00543100",
    SNAME: "current_consumption",
    SUNIT: "W",
}
SENSOR_GRID_ACTIVE_POWER_CONSUMED_L1 = {
    SKEY: "6100_0046EB00",
    SNAME: "grid_active_power_consumed_l1",
    SUNIT: "W",
}
SENSOR_GRID_ACTIVE_POWER_CONSUMED_L2 = {
    SKEY: "6100_0046EC00",
    SNAME: "grid_active_power_consumed_l2",
    SUNIT: "W",
}
SENSOR_GRID_ACTIVE_POWER_CONSUMED_L3 = {
    SKEY: "6100_0046ED00",
    SNAME: "grid_active_power_consumed_l3",
    SUNIT: "W",
}
SENSOR_TOTAL_CONSUMPTION = {
    SKEY: "6400_00543A00",
    SNAME: "total_consumption",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
# Battery related sensors
SENSOR_BATTERY_SOC = ["6100_00295A00_0", "battery_soc", "%"]
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
SENSOR_BATTERY_INVERTER_POWER = {
    SKEY: "6100_40263F00_0",
    SNAME: "battery_inverter_power",
    SUNIT: "W",
}
# General
SENSOR_STATUS = {
    SKEY: "6180_08214800",
    SNAME: "status",
    SPATH: ('"1"[0].val[0].tag', "val[0].tag"),
    SL10N: True,
}
SENSOR_SERIAL_NUMBER = {SKEY: "6800_00A21E00", SNAME: "serial_number"}
SENSOR_DEVICE_NAME = {SKEY: "6800_10821E00", SNAME: "device_name"}
SENSOR_DEVICE_TYPE = {
    SKEY: "6800_08822000",
    SNAME: "device_type",
    SPATH: ('"1"[0].val[0].tag', "val[0].tag"),
    SL10N: True,
}

SENSOR_DEVICE_MANUFACTURER = {
    SKEY: "6800_08822B00",
    SNAME: "device_manufacturer",
    SPATH: ('"1"[0].val[0].tag', "val[0].tag"),
    SL10N: True,
}

SENSOR_MAP = {
    DEVCLASS_INVERTER: [
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
        SENSOR_PV_POWER_A,
        SENSOR_PV_POWER_B,
        SENSOR_PV_VOLTAGE_A,
        SENSOR_PV_VOLTAGE_B,
        SENSOR_PV_CURRENT_A,
        SENSOR_PV_CURRENT_B,
        SENSOR_PV_GEN_METER,
        SENSOR_TOTAL_YIELD,
        SENSOR_DAILY_YIELD,
        SENSOR_GRID_POWER_SUPPLIED,
        SENSOR_GRID_POWER_ABSORBED,
        SENSOR_GRID_TOTAL_YIELD,
        SENSOR_CURRENT_CONSUMPTION,
        SENSOR_TOTAL_CONSUMPTION,
        SENSOR_STATUS,
    ],
    ENERGY_METER_VIA_INVERTER: [
        SENSOR_GRID_ACTIVE_POWER_CONSUMED_L1,
        SENSOR_GRID_ACTIVE_POWER_CONSUMED_L2,
        SENSOR_GRID_ACTIVE_POWER_CONSUMED_L3,
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
        SENSOR_BATTERY_INVERTER_POWER,
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
    ],
    DEVICE_INFO: [
        SENSOR_SERIAL_NUMBER,
        SENSOR_DEVICE_NAME,
        SENSOR_DEVICE_TYPE,
        SENSOR_DEVICE_MANUFACTURER,
    ],
}