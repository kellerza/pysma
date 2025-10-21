"""Constants for SMA WebConnect library for Python."""

URL_LOGIN = "/dyn/login.json"
URL_LOGOUT = "/dyn/logout.json"
URL_VALUES = "/dyn/getValues.json"
URL_ALL_VALUES = "/dyn/getAllOnlValues.json"
URL_ALL_PARAMS = "/dyn/getAllParamValues.json"
URL_LOGGER = "/dyn/getLogger.json"
URL_DASH_LOGGER = "/dyn/getDashLogger.json"
URL_DASH_VALUES = "/dyn/getDashValues.json"

USERS = {"user": "usr", "installer": "istl"}

DEFAULT_TIMEOUT = 15
DEFAULT_LANG = "en-US"

JMESPATH_VAL = "val"
JMESPATH_VAL_TAG = JMESPATH_VAL + "[0].tag"
JMESPATH_VAL_STR = "[?str==sum([`1`,`{}`])].val | [0]"
JMESPATH_VAL_IDX = "* | [0][{}].val"
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

GENERIC_SENSORS = "generic"
OPTIMIZERS_VIA_INVERTER = "optimizers"
ENERGY_METER_VIA_INVERTER = "energy-meter"
DEVICE_INFO = "device-info"
