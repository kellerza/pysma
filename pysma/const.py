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
SENSOR_CURRENT_TOTAL = { # Example: "6100_00664F00":{"7":[{"val":3501}]} # 10038=GridMs.TotA\6704896\Grid current
    SKEY: "6100_00664F00",
    SNAME: "current_total",
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
SENSOR_BATTERY_DC_VOLTAGE_A = { # Example: "6100_00495C00":{"7":[{"val":16363},{"val":null},{"val":null}]} # 10905=Bat.Vol\4807680\Battery voltage
    SKEY: "6100_00495C00_0",
    SNAME: "battery_dc_voltage_a",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_DC_VOLTAGE_B = { # Example: "6100_00495C00":{"7":[{"val":16363},{"val":null},{"val":null}]} # 10905=Bat.Vol\4807680\Battery voltage
    SKEY: "6100_00495C00_1",
    SNAME: "battery_dc_voltage_b",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_DC_VOLTAGE_C = { # Example: "6100_00495C00":{"7":[{"val":16363},{"val":null},{"val":null}]} # 10905=Bat.Vol\4807680\Battery voltage
    SKEY: "6100_00495C00_2",
    SNAME: "battery_dc_voltage_c",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_DC_CHARGING_VOLTAGE_A = { # Example "6102_00493500":{"7":[{"val":17520},{"val":null},{"val":null}]} # 
    SKEY: "6102_00493500_0",
    SNAME: "battery_dc_charging_voltage_a",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_DC_CHARGING_VOLTAGE_B = { # Example: "6102_00493500":{"7":[{"val":17520},{"val":null},{"val":null}]} # 
    SKEY: "6102_00493500_1",
    SNAME: "battery_dc_charging_voltage_b",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_DC_CHARGING_VOLTAGE_C = { # Example: "6102_00493500":{"7":[{"val":17520},{"val":null},{"val":null}]} # 
    SKEY: "6102_00493500_2",
    SNAME: "battery_dc_charging_voltage_c",
    SUNIT: "V",
    SFACTOR: 100,
}
SENSOR_BATTERY_DC_CURRENT_A = { # Example: "6100_40495D00":{"7":[{"val":44},{"val":null},{"val":null}]} # 
    SKEY: "6100_40495D00_0",
    SNAME: "battery_dc_current_a",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_BATTERY_DC_CURRENT_B = { # Example: "6100_40495D00":{"7":[{"val":44},{"val":null},{"val":null}]} # 
    SKEY: "6100_40495D00_1",
    SNAME: "battery_dc_current_b",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_BATTERY_DC_CURRENT_C = { # Example: "6100_40495D00":{"7":[{"val":44},{"val":null},{"val":null}]} # 
    SKEY: "6100_40495D00_2",
    SNAME: "battery_dc_current_c",
    SUNIT: "A",
    SFACTOR: 1000,
}
SENSOR_BATTERY_AC_POWER_LIMIT = { # Example: "6800_00832A00":{"7":[{"low":3680,"high":3680,"val":3680}]} # 10121=Inverter.WLim\8595968\Maximum active power device
    SKEY: "6800_00832A00",
    SNAME: "battery_ac_power_limit",
    SUNIT: "W",
}
SENSOR_BATTERY_AC_POWER_CHARGE_TOTAL = { # Example: "6100_00496900":{"7":[{"val":0}]} # 11224=BatChrg.CurBatCha\4811008\Present battery charge
    SKEY: "6100_00496900",
    SNAME: "battery_ac_power_charge_total",
    SUNIT: "W",
}
SENSOR_BATTERY_AC_POWER_CHARGE_A = { # Example: "6100_00499300":{"7":[{"val":0},{"val":null},{"val":null}]}
    SKEY: "6100_00499300_0",
    SNAME: "battery_ac_power_charge_a",
    SUNIT: "W",
}
SENSOR_BATTERY_AC_POWER_CHARGE_B = { # Example: "6100_00499300":{"7":[{"val":0},{"val":null},{"val":null}]}
    SKEY: "6100_00499300_1",
    SNAME: "battery_ac_power_charge_b",
    SUNIT: "W",
}
SENSOR_BATTERY_AC_POWER_CHARGE_C = { # Example: "6100_00499300":{"7":[{"val":0},{"val":null},{"val":null}]}
    SKEY: "6100_00499300_2",
    SNAME: "battery_ac_power_charge_c",
    SUNIT: "W",
}
SENSOR_BATTERY_AC_POWER_DISCHARGE_TOTAL = { # Example: # "6100_00496A00":{"7":[{"val":0}]} # 11225=BatDsch.CurBatDsch\4811264\Present battery discharge
    SKEY: "6100_00496A00",
    SNAME: "battery_ac_power_discharge_total",
    SUNIT: "W",
}
SENSOR_BATTERY_AC_POWER_DISCHARGE_A = { # Example: "6100_00499400":{"7":[{"val":0},{"val":null},{"val":null}]}
    SKEY: "6100_00499400_0",
    SNAME: "battery_ac_power_discharge_a",
    SUNIT: "W",
}
SENSOR_BATTERY_AC_POWER_DISCHARGE_B = { # Example: "6100_00499400":{"7":[{"val":0},{"val":null},{"val":null}]}
    SKEY: "6100_00499400_1",
    SNAME: "battery_ac_power_discharge_b",
    SUNIT: "W",
}
SENSOR_BATTERY_AC_POWER_DISCHARGE_C = { # Example: "6100_00499400":{"7":[{"val":0},{"val":null},{"val":null}]}
    SKEY: "6100_00499400_2",
    SNAME: "battery_ac_power_discharge_c",
    SUNIT: "W",
}
SENSOR_BATTERY_AC_REACTIVE_POWER = { # Example: "6100_40265F00":{"7":[{"val":-3}]}
    SKEY: "6100_40265F00",
    SNAME: "battery_ac_reactive_power",
    SUNIT: "var",
}
SENSOR_BATTERY_AC_REACTIVE_POWER_L1 = { # Example: "6100_40666000":{"7":[{"val":-6}]} # 10044=GridMs.VAr.phsA\6709248\Reactive power L1
    SKEY: "6100_40666000",
    SNAME: "battery_ac_reactive_power_l1",
    SUNIT: "var",
}
SENSOR_BATTERY_AC_REACTIVE_POWER_L2 = { # Example: "6100_40666100":{"7":[{"val":null}]} # 10045=GridMs.VAr.phsB\6709504\Reactive power L2
    SKEY: "6100_40666100",
    SNAME: "battery_ac_reactive_power_l2",
    SUNIT: "var",
}
SENSOR_BATTERY_AC_REACTIVE_POWER_L3 = { # Example: "6100_40666200":{"7":[{"val":null}]} # 10046=GridMs.VAr.phsC\6709760\Reactive power L3
    SKEY: "6100_40666200",
    SNAME: "battery_ac_reactive_power_l3",
    SUNIT: "var",
}
SENSOR_BATTERY_AC_APPARENT_POWER = { # Example: "6100_40666700":{"7":[{"val":0}]} # 10047=GridMs.TotVA\6711040\Apparent power
    SKEY: "6100_40666700",
    SNAME: "battery_ac_apparent_power",
    SUNIT: "VA",
}
SENSOR_BATTERY_AC_APPARENT_POWER_L1 = { # Example: "6100_40666800":{"7":[{"val":0}]} # 10048=GridMs.VA.phsA\6711296\Apparent power L1
    SKEY: "6100_40666800",
    SNAME: "battery_ac_apparent_power_l1",
    SUNIT: "VA",
}
SENSOR_BATTERY_AC_APPARENT_POWER_L2 = { # Example: "6100_40666900":{"7":[{"val":null}]} # 10049=GridMs.VA.phsB\6711552\Apparent power L2
    SKEY: "6100_40666900",
    SNAME: "battery_ac_apparent_power_l2",
    SUNIT: "VA",
}
SENSOR_BATTERY_AC_APPARENT_POWER_L3 = { # Example: "6100_40666A00":{"7":[{"val":null}]} # 10050=GridMs.VA.phsC\6711808\Apparent power L3
    SKEY: "6100_40666A00",
    SNAME: "battery_ac_apparent_power_l3",
    SUNIT: "VA",
}
SENSOR_BATTERY_AC_POWER_FACTOR = { # Example: "6100_00665900":{"7":[{"val":999}]} # 10710=GridMs.TotPFPrc\6707456\Displacement power factor
    SKEY: "6100_00665900",
    SNAME: "battery_ac_power_factor",
    SUNIT: "",
    SFACTOR: 1000,
}
SENSOR_BATTERY_AC_POWER_FACTOR_EXCITATION = { # Example: "6180_08465A00":{"7":[{"val":[{"tag":1042}]}]} # 10711=GridMs.TotPFExt\4610560\Excitation type of cos φ # 1041=OvExt\0\Overexcited # 1042=UnExt\0\Underexcited
    SKEY: "6180_08465A00",
    SNAME: "battery_ac_power_factor_excitation",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_AC_ENERGY_CHARGE_TOTAL = { # Example: "6400_00496700":{"7":[{"val":64712}]} # 11218=BatChrg.BatChrg\4810496\Battery charge
    SKEY: "6400_00496700",
    SNAME: "battery_ac_energy_charge_total",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_AC_ENERGY_CHARGE_A = { # Example: "6400_00499500":{"7":[{"val":64712},{"val":null},{"val":null}]}
    SKEY: "6400_00499500_0",
    SNAME: "battery_ac_energy_charge_a",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_AC_ENERGY_CHARGE_B = { # Example: "6400_00499500":{"7":[{"val":64712},{"val":null},{"val":null}]}
    SKEY: "6400_00499500_1",
    SNAME: "battery_ac_energy_charge_b",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_AC_ENERGY_CHARGE_C = { # Example: "6400_00499500":{"7":[{"val":64712},{"val":null},{"val":null}]}
    SKEY: "6400_00499500_2",
    SNAME: "battery_ac_energy_charge_c",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_AC_ENERGY_DISCHARGE_TOTAL = { # Example: "6400_00496800":{"7":[{"val":42044}]} # 11219=BatDsch.BatDsch\4810752\Battery discharge
    SKEY: "6400_00496800",
    SNAME: "battery_ac_energy_discharge_total",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_AC_ENERGY_DISCHARGE_A = { # Example: "6400_00499600":{"7":[{"val":42044},{"val":null},{"val":null}]}
    SKEY: "6400_00499600_0",
    SNAME: "battery_ac_energy_discharge_a",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_AC_ENERGY_DISCHARGE_B = { # Example: "6400_00499600":{"7":[{"val":42044},{"val":null},{"val":null}]}
    SKEY: "6400_00499600_1",
    SNAME: "battery_ac_energy_discharge_b",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_AC_ENERGY_DISCHARGE_C = { # Example: "6400_00499600":{"7":[{"val":42044},{"val":null},{"val":null}]}
    SKEY: "6400_00499600_2",
    SNAME: "battery_ac_energy_discharge_c",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_AC_ENERGY_DISCHARGE_DAY = { # Example: "6400_00262200":{"7":[{"val":1819}]} # 10272=Metering.DyWhOut\2499072\Day yield
    SKEY: "6400_00496800",
    SNAME: "battery_ac_energy_discharge_day",
    SUNIT: "kWh",
    SFACTOR: 1000,
}
SENSOR_BATTERY_SOC_TOTAL = { # Example: "6100_00295A00":{"7":[{"val":100}]} # 2292=BatChaStt\2710016\Charge battery
    SKEY: "6100_00295A00",
    SNAME: "battery_soc_total",
    SUNIT: "%",
}
SENSOR_BATTERY_SOC_A = { # Example: "6100_00498F00":{"7":[{"val":100},{"val":null},{"val":null}]}
    SKEY: "6100_00498F00_0",
    SNAME: "battery_soc_a",
    SUNIT: "%",
}
SENSOR_BATTERY_SOC_B = { # Example: "6100_00498F00":{"7":[{"val":100},{"val":null},{"val":null}]}
    SKEY: "6100_00498F00_1",
    SNAME: "battery_soc_b",
    SUNIT: "%",
}
SENSOR_BATTERY_SOC_C = { # Example: "6100_00498F00":{"7":[{"val":100},{"val":null},{"val":null}]}
    SKEY: "6100_00498F00_2",
    SNAME: "battery_soc_c",
    SUNIT: "%",
}
SENSOR_BATTERY_CAPACITY_TOTAL = { # Example: "6100_00696E00":{"7":[{"val":100}]} # 10921=Bat.Diag.ActlCapacNom\6909440\Current battery capacity
    SKEY: "6100_00696E00",
    SNAME: "battery_capacity_total",
    SUNIT: "%",
}
SENSOR_BATTERY_CAPACITY_A = { # Example: "6100_00499100":{"7":[{"val":100},{"val":null},{"val":null}]}
    SKEY: "6100_00499100_0",
    SNAME: "battery_capacity_a",
    SUNIT: "%",
}
SENSOR_BATTERY_CAPACITY_B = { # Example: "6100_00499100":{"7":[{"val":100},{"val":null},{"val":null}]}
    SKEY: "6100_00499100_1",
    SNAME: "battery_capacity_b",
    SUNIT: "%",
}
SENSOR_BATTERY_CAPACITY_C = { # Example: "6100_00499100":{"7":[{"val":100},{"val":null},{"val":null}]}
    SKEY: "6100_00499100_2",
    SNAME: "battery_capacity_c",
    SUNIT: "%",
}
SENSOR_BATTERY_TEMP_A = { # Example: "6100_40495B00":{"7":[{"val":180},{"val":null},{"val":null}]} # 10904=Bat.TmpVal\4807424\Battery temperature
    SKEY: "6100_40495B00_0",
    SNAME: "battery_temp_a",
    SUNIT: "C",
    SFACTOR: 10,
}
SENSOR_BATTERY_TEMP_B = { # Example: "6100_40495B00":{"7":[{"val":180},{"val":null},{"val":null}]} # 10904=Bat.TmpVal\4807424\Battery temperature
    SKEY: "6100_40495B00_1",
    SNAME: "battery_temp_b",
    SUNIT: "C",
    SFACTOR: 10,
}
SENSOR_BATTERY_TEMP_C = { # Example: "6100_40495B00":{"7":[{"val":180},{"val":null},{"val":null}]} # 10904=Bat.TmpVal\4807424\Battery temperature
    SKEY: "6100_40495B00_2",
    SNAME: "battery_temp_c",
    SUNIT: "C",
    SFACTOR: 10,
}
SENSOR_BATTERY_INSULATION_RESISTANCE = { # Example: # "6102_00254F00":{"7":[{"val":3000000}]} # 10079=Isolation.LeakRis\2445056\Insulation resistance
    SKEY: "6102_00254F00",
    SNAME: "battery_insulation_resistance",
    SUNIT: "kOhm",
    SFACTOR: 1000,
}
SENSOR_BATTERY_INSULATION_RESIDUAL_CURRENT = { # Example: # "6102_40254E00":{"7":[{"val":7}]} # 10078=Isolation.FltA\2444800\Residual current mA
    SKEY: "6102_40254E00",
    SNAME: "battery_insulation_residual_current",
    SUNIT: "mA",
}
SENSOR_BATTERY_OPERATING_TIME_TOTAL = { # Example: "6400_00462E00":{"7":[{"val":1314643}]} # 10011=Metering.TotOpTms\4599296\Operating time
    SKEY: "6400_00462E00",
    SNAME: "battery_operating_time_total",
    SUNIT: "h",
    SFACTOR: 3600,
}
SENSOR_BATTERY_OPERATING_TIME_FEEDIN = { # Example: "6400_00462F00":{"7":[{"val":941649}]} # 10012=Metering.TotFeedTms\4599552\Feed-in time
    SKEY: "6400_00462F00",
    SNAME: "battery_operating_time_feedin",
    SUNIT: "h",
    SFACTOR: 3600,
}
SENSOR_BATTERY_STATS_GRID_CONNECTIONS = { # Example: "6402_00666F00":{"7":[{"val":111}]}} # 10010=Operation.GriSwCnt\6713088\Number of grid connections
    SKEY: "6402_00666F00",
    SNAME: "battery_stats_grid_connections",
    SUNIT: "",
}
SENSOR_BATTERY_CONDITION_INVERTER = { # Example: "6180_08414C00":{"7":[{"val":[{"tag":307}]}]} # 11176=Operation.Inverter.Health\4279296\Inverter status # Gives back a code, 307 = Ok
    SKEY: "6180_08414C00",
    SNAME: "battery_condition_inverter",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_CONDITION_A = { # Example: "6180_08414D00":{"7":[{"val":[{"tag":307}]},{"val":[{"tag":16777213}]},{"val":[{"tag":16777213}]}]} # 11177=Operation.Bat.Health\4279552\Battery status # Gives back a code, 307 = Ok, 16777213 = Information not available
    SKEY: "6180_08414D00_0",
    SNAME: "battery_condition_a",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_CONDITION_B = { # Example: "6180_08414D00":{"7":[{"val":[{"tag":307}]},{"val":[{"tag":16777213}]},{"val":[{"tag":16777213}]}]} # 11177=Operation.Bat.Health\4279552\Battery status # Gives back a code, 307 = Ok, 16777213 = Information not available
    SKEY: "6180_08414D00_1",
    SNAME: "battery_condition_b",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_CONDITION_C = { # Example: "6180_08414D00":{"7":[{"val":[{"tag":307}]},{"val":[{"tag":16777213}]},{"val":[{"tag":16777213}]}]} # 11177=Operation.Bat.Health\4279552\Battery status # Gives back a code, 307 = Ok, 16777213 = Information not available
    SKEY: "6180_08414D00_2",
    SNAME: "battery_condition_c",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_CONDITION_TEMP_A = { # Example: # "6180_08414E00":{"7":[{"val":[{"tag":307}]},{"val":[{"tag":16777213}]},{"val":[{"tag":16777213}]}]} # 11261=Operation.Bat.TmpHealth\4279808\Battery temp. # Gives back a code, 307 = Ok, 16777213 = Information not available
    SKEY: "6180_08414E00_0",
    SNAME: "battery_condition_temp_a",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_CONDITION_TEMP_B = { # Example: # "6180_08414E00":{"7":[{"val":[{"tag":307}]},{"val":[{"tag":16777213}]},{"val":[{"tag":16777213}]}]} # 11261=Operation.Bat.TmpHealth\4279808\Battery temp. # Gives back a code, 307 = Ok, 16777213 = Information not available
    SKEY: "6180_08414E00_1",
    SNAME: "battery_condition_temp_b",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_CONDITION_TEMP_C = { # Example: # "6180_08414E00":{"7":[{"val":[{"tag":307}]},{"val":[{"tag":16777213}]},{"val":[{"tag":16777213}]}]} # 11261=Operation.Bat.TmpHealth\4279808\Battery temp. # Gives back a code, 307 = Ok, 16777213 = Information not available
    SKEY: "6180_08414E00_2",
    SNAME: "battery_condition_temp_c",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_STATUS_GENERAL = { # Example: "6180_08412800":{"7":[{"val":[{"tag":1295}]}]} # 11040=Operation.OpStt\4270080\General operating status # gives back a code; 1295 = Standby, 569 = Activated  
    SKEY: "6180_08412800",
    SNAME: "battery_status_general",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_STATUS_BMS_A = { # Example: "6182_08497F00":{"7":[{"val":[{"tag":388}]},{"val":[{"tag":16777213}]},{"val":[{"tag":16777213}]}]} # 11803=Operation.CmpBMS.OpStt\4816640\Operating status # 388=SttOp\0\Operation status
    SKEY: "6182_08497F00_0",
    SNAME: "battery_status_bms_a",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_STATUS_BMS_B = { # Example: "6182_08497F00":{"7":[{"val":[{"tag":388}]},{"val":[{"tag":16777213}]},{"val":[{"tag":16777213}]}]} # 11803=Operation.CmpBMS.OpStt\4816640\Operating status # 388=SttOp\0\Operation status
    SKEY: "6182_08497F00_1",
    SNAME: "battery_status_bms_b",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_STATUS_BMS_C = { # Example: "6182_08497F00":{"7":[{"val":[{"tag":388}]},{"val":[{"tag":16777213}]},{"val":[{"tag":16777213}]}]} # 11803=Operation.CmpBMS.OpStt\4816640\Operating status # 388=SttOp\0\Operation status
    SKEY: "6182_08497F00_2",
    SNAME: "battery_status_bms_c",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_STATUS_OPERATING_MODE = { # Example: "6180_08495E00":{"7":[{"val":[{"tag":2293}]}]} # gives back a code: 2292 = Charge battery, 2293 = Discharge battery
    SKEY: "6180_08495E00",
    SNAME: "battery_status_operating_mode",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_STATUS_GRID_SWITCH = { # Example: "6180_08416400":{"7":[{"val":[{"tag":311}]}]} # 10114=Operation.GriSwStt\4285440\Grid relay/contactor # Gives back a code, 311 = Open, 51 = Closed
    SKEY: "6180_08416400",
    SNAME: "battery_status_grid_switch",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_STATUS_POWER_SUPPLY = { # Example: "6180_0846A700":{"7":[{"val":[{"tag":303}]}]} # 10760=Operation.CsmpGriConnStt\4630272\Power supply status # 303=Off\0\Off # 1461=GriConn\0\Mains connected
    SKEY: "6180_0846A700",
    SNAME: "battery_status_power_supply",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_STATUS_FIRMWARE_UPDATE = { # Example: "6180_08412900":{"7":[{"val":[{"tag":302}]}]} # 3522=UpdStt\4270336\Update of the FW being performed # Gives back a code, 302 = -------
    SKEY: "6180_08412900",
    SNAME: "battery_status_firmware_update",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_STATUS_SYSTEM_INIT = { # Example: "6800_08811F00": {"7": [{"validVals": [1129, 1130], "val": [{"tag": 1129}]}]} --> gives back a code: 1129 = Yes, 1130 = No 
    SKEY: "6800_08811F00",
    SNAME: "battery_status_system_init",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
}
SENSOR_BATTERY_STATUS_CHARGE_CONTROL_COMM = { # Example: "6182_08495600":{"7":[{"val":[{"tag":1129}]}]} # 11466=Bat.ChaCtlComAval\4806144\Control of battery charging via communication available # 1129=Yes\0\Yes 
    SKEY: "6182_08495600",
    SNAME: "battery_status_charge_control_comm",
    SPATH: JMESPATHS_TAG,
    SL10N: True,
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
        SENSOR_BATTERY_DC_VOLTAGE_A, 
        SENSOR_BATTERY_DC_VOLTAGE_B, 
        SENSOR_BATTERY_DC_VOLTAGE_C, 
        SENSOR_BATTERY_DC_CHARGING_VOLTAGE_A, 
        SENSOR_BATTERY_DC_CHARGING_VOLTAGE_B, 
        SENSOR_BATTERY_DC_CHARGING_VOLTAGE_C ,
        SENSOR_BATTERY_DC_CURRENT_A,
        SENSOR_BATTERY_DC_CURRENT_B,
        SENSOR_BATTERY_DC_CURRENT_C,
        SENSOR_BATTERY_AC_POWER_LIMIT,
        SENSOR_BATTERY_AC_POWER_CHARGE_TOTAL,
        SENSOR_BATTERY_AC_POWER_CHARGE_A,
        SENSOR_BATTERY_AC_POWER_CHARGE_B,
        SENSOR_BATTERY_AC_POWER_CHARGE_C,
        SENSOR_BATTERY_AC_POWER_DISCHARGE_TOTAL,
        SENSOR_BATTERY_AC_POWER_DISCHARGE_A,
        SENSOR_BATTERY_AC_POWER_DISCHARGE_B,
        SENSOR_BATTERY_AC_POWER_DISCHARGE_C,
        SENSOR_BATTERY_AC_REACTIVE_POWER,
        SENSOR_BATTERY_AC_REACTIVE_POWER_L1,
        SENSOR_BATTERY_AC_REACTIVE_POWER_L2,
        SENSOR_BATTERY_AC_REACTIVE_POWER_L3,
        SENSOR_BATTERY_AC_APPARENT_POWER,
        SENSOR_BATTERY_AC_APPARENT_POWER_L1,
        SENSOR_BATTERY_AC_APPARENT_POWER_L2,
        SENSOR_BATTERY_AC_APPARENT_POWER_L3,
        SENSOR_BATTERY_AC_POWER_FACTOR,
        SENSOR_BATTERY_AC_POWER_FACTOR_EXCITATION,
        SENSOR_BATTERY_AC_ENERGY_CHARGE_TOTAL,
        SENSOR_BATTERY_AC_ENERGY_CHARGE_A,
        SENSOR_BATTERY_AC_ENERGY_CHARGE_B,
        SENSOR_BATTERY_AC_ENERGY_CHARGE_C,
        SENSOR_BATTERY_AC_ENERGY_DISCHARGE_TOTAL,
        SENSOR_BATTERY_AC_ENERGY_DISCHARGE_A,
        SENSOR_BATTERY_AC_ENERGY_DISCHARGE_B,
        SENSOR_BATTERY_AC_ENERGY_DISCHARGE_C,
        SENSOR_BATTERY_AC_ENERGY_DISCHARGE_DAY,
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
        SENSOR_BATTERY_INSULATION_RESISTANCE,
        SENSOR_BATTERY_INSULATION_RESIDUAL_CURRENT,
        SENSOR_BATTERY_OPERATING_TIME_TOTAL,
        SENSOR_BATTERY_OPERATING_TIME_FEEDIN,
        SENSOR_BATTERY_STATS_GRID_CONNECTIONS,
        SENSOR_BATTERY_CONDITION_INVERTER,
        SENSOR_BATTERY_CONDITION_A,
        SENSOR_BATTERY_CONDITION_B,
        SENSOR_BATTERY_CONDITION_C,
        SENSOR_BATTERY_CONDITION_TEMP_A,
        SENSOR_BATTERY_CONDITION_TEMP_B,
        SENSOR_BATTERY_CONDITION_TEMP_C,
        SENSOR_BATTERY_STATUS_GENERAL,
        SENSOR_BATTERY_STATUS_BMS_A,
        SENSOR_BATTERY_STATUS_BMS_B,
        SENSOR_BATTERY_STATUS_BMS_C,
        SENSOR_BATTERY_STATUS_OPERATING_MODE,
        SENSOR_BATTERY_STATUS_GRID_SWITCH,
        SENSOR_BATTERY_STATUS_POWER_SUPPLY,
        SENSOR_BATTERY_STATUS_FIRMWARE_UPDATE,
        SENSOR_BATTERY_STATUS_SYSTEM_INIT,
        SENSOR_BATTERY_STATUS_CHARGE_CONTROL_COMM,
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
