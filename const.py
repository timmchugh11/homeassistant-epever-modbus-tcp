DOMAIN = "epever_modbus"

DEVICE_TYPES = {
    "epever_tracer": {
        "name": "EPEVER Tracer MPPT",

        "sensors": [
            # -------------------- RATED VALUES --------------------
            {"key": "array_rated_voltage_raw",   "name": "Array Rated Voltage Raw",   "register": 0x3000, "type": "input", "category": "diagnostic"},
            {"key": "array_rated_current_raw",   "name": "Array Rated Current Raw",   "register": 0x3001, "type": "input", "category": "diagnostic"},
            {"key": "array_rated_power_raw",     "name": "Array Rated Power Raw",     "register": 0x3002, "type": "input", "length": 2, "category": "diagnostic"},

            {"key": "battery_rated_voltage_raw", "name": "Battery Rated Voltage Raw", "register": 0x3004, "type": "input", "category": "diagnostic"},
            {"key": "battery_rated_current_raw", "name": "Battery Rated Current Raw", "register": 0x3005, "type": "input", "category": "diagnostic"},
            {"key": "battery_rated_power_raw",   "name": "Battery Rated Power Raw",   "register": 0x3006, "type": "input", "length": 2, "category": "diagnostic"},

            {"key": "charging_mode_raw",         "name": "Charging Mode Raw",         "register": 0x3008, "type": "input", "category": "diagnostic"},
            {"key": "rated_load_current_raw",    "name": "Rated Load Current Raw",    "register": 0x300E, "type": "input", "category": "diagnostic"},

            # -------------------- REAL-TIME VALUES --------------------
            {"key": "pv_voltage_raw",    "name": "PV Voltage Raw",    "register": 0x3100, "type": "input", "category": "diagnostic"},
            {"key": "pv_current_raw",    "name": "PV Current Raw",    "register": 0x3101, "type": "input", "category": "diagnostic"},
            {"key": "pv_power_raw",      "name": "PV Power Raw",      "register": 0x3102, "type": "input", "length": 2, "category": "diagnostic"},

            {"key": "charging_voltage_raw", "name": "Charging Voltage Raw", "register": 0x3104, "type": "input", "category": "diagnostic"},
            {"key": "charging_current_raw", "name": "Charging Current Raw", "register": 0x3105, "type": "input", "category": "diagnostic"},
            {"key": "charging_power_raw",   "name": "Charging Power Raw",   "register": 0x3106, "type": "input", "length": 2, "category": "diagnostic"},

            {"key": "load_voltage_raw", "name": "Load Voltage Raw", "register": 0x310C, "type": "input", "category": "diagnostic"},
            {"key": "load_current_raw", "name": "Load Current Raw", "register": 0x310D, "type": "input", "category": "diagnostic"},
            {"key": "load_power_raw",   "name": "Load Power Raw",   "register": 0x310E, "type": "input", "length": 2, "category": "diagnostic"},

            {"key": "battery_temp_raw",    "name": "Battery Temp Raw",    "register": 0x3110, "type": "input", "category": "diagnostic"},
            {"key": "device_temp_raw",     "name": "Device Temp Raw",     "register": 0x3111, "type": "input", "category": "diagnostic"},
            {"key": "component_temp_raw",  "name": "Component Temp Raw",  "register": 0x3112, "type": "input", "category": "diagnostic"},

            {"key": "battery_soc_raw",     "name": "Battery SOC Raw",     "register": 0x311A, "type": "input", "category": "diagnostic"},
            {"key": "remote_temp_raw",     "name": "Remote Temp Raw",     "register": 0x311B, "type": "input", "category": "diagnostic"},
            {"key": "remote_real_voltage_raw", "name": "Remote Real Voltage Raw", "register": 0x311D, "type": "input", "category": "diagnostic"},

            {"key": "battery_status_raw",  "name": "Battery Status Raw",  "register": 0x3200, "type": "input", "category": "diagnostic"},
            {"key": "charger_status_raw",  "name": "Charger Status Raw",  "register": 0x3201, "type": "input", "category": "diagnostic"},

            # -------------------- STATS --------------------
            {"key": "max_pv_today_raw",    "name": "Max PV Voltage Today Raw",    "register": 0x3300, "type": "input", "category": "diagnostic"},
            {"key": "min_pv_today_raw",    "name": "Min PV Voltage Today Raw",    "register": 0x3301, "type": "input", "category": "diagnostic"},
            {"key": "max_batt_today_raw",  "name": "Max Battery Voltage Today Raw","register": 0x3302, "type": "input", "category": "diagnostic"},
            {"key": "min_batt_today_raw",  "name": "Min Battery Voltage Today Raw","register": 0x3303, "type": "input", "category": "diagnostic"},

            {"key": "consumed_today_raw",  "name": "Consumed Today Raw",  "register": 0x3304, "type": "input", "length": 2, "category": "diagnostic"},
            {"key": "consumed_month_raw",  "name": "Consumed Month Raw",  "register": 0x3306, "type": "input", "length": 2, "category": "diagnostic"},
            {"key": "consumed_year_raw",   "name": "Consumed Year Raw",   "register": 0x3308, "type": "input", "length": 2, "category": "diagnostic"},
            {"key": "consumed_total_raw",  "name": "Consumed Total Raw",  "register": 0x330A, "type": "input", "length": 2, "category": "diagnostic"},

            {"key": "generated_today_raw", "name": "Generated Today Raw", "register": 0x330C, "type": "input", "length": 2, "category": "diagnostic"},
            {"key": "generated_month_raw", "name": "Generated Month Raw", "register": 0x330E, "type": "input", "length": 2, "category": "diagnostic"},
            {"key": "generated_year_raw",  "name": "Generated Year Raw",  "register": 0x3310, "type": "input", "length": 2, "category": "diagnostic"},
            {"key": "generated_total_raw", "name": "Generated Total Raw", "register": 0x3312, "type": "input", "length": 2, "category": "diagnostic"},

            {"key": "co2_raw",             "name": "CO₂ Raw",             "register": 0x3314, "type": "input", "length": 2, "category": "diagnostic"},

            # your template uses this as "Battery Voltage Raw"
            {"key": "battery_voltage_raw", "name": "Battery Voltage Raw", "register": 0x331A, "type": "input", "category": "diagnostic"},
            {"key": "battery_current_raw", "name": "Battery Current Raw", "register": 0x331B, "type": "input", "length": 2, "category": "diagnostic"},
        ],

        "virtual_sensors": [
            # ------------- Rated values -------------
            {"key": "array_rated_voltage",   "name": "Array Rated Voltage",   "unit": "V",   "formula": "epever_array_rated_voltage",   "precision": 1},
            {"key": "array_rated_current",   "name": "Array Rated Current",   "unit": "A",   "formula": "epever_array_rated_current",   "precision": 2},
            {"key": "array_rated_power",     "name": "Array Rated Power",     "unit": "W",   "formula": "epever_array_rated_power",     "precision": 1},

            {"key": "battery_rated_voltage", "name": "Battery Rated Voltage", "unit": "V",   "formula": "epever_battery_rated_voltage", "precision": 1},
            {"key": "battery_rated_current", "name": "Battery Rated Current", "unit": "A",   "formula": "epever_battery_rated_current", "precision": 1},
            {"key": "battery_rated_power",   "name": "Battery Rated Power",   "unit": "W",   "formula": "epever_battery_rated_power",   "precision": 1},

            # ------------- Battery realtime -------------
            {"key": "battery_voltage",       "name": "Battery Voltage",       "unit": "V",   "formula": "epever_battery_voltage",       "precision": 2},
            {"key": "battery_current",       "name": "Battery Current",       "unit": "A",   "formula": "epever_battery_current",       "precision": 2},
            {"key": "battery_soc",           "name": "Battery SOC",           "unit": "%",   "formula": "epever_battery_soc",           "precision": 0},
            {"key": "battery_temperature",   "name": "Battery Temperature",   "unit": "°C",  "formula": "epever_battery_temperature",   "precision": 1},

            # ------------- PV side -------------
            {"key": "pv_voltage",            "name": "PV Voltage",            "unit": "V",   "formula": "epever_pv_voltage",            "precision": 2},
            {"key": "pv_current",            "name": "PV Current",            "unit": "A",   "formula": "epever_pv_current",            "precision": 2},
            {"key": "pv_power",              "name": "PV Power",              "unit": "W",   "formula": "epever_pv_power",              "precision": 1},

            # ------------- Device temps -------------
            {"key": "device_temperature",    "name": "Device Temperature",    "unit": "°C",  "formula": "epever_device_temperature",    "precision": 1},
            {"key": "component_temperature", "name": "Component Temperature", "unit": "°C",  "formula": "epever_component_temperature", "precision": 1},

            # ------------- Charging side -------------
            {"key": "charging_voltage",      "name": "Charging Voltage",      "unit": "V",   "formula": "epever_charging_voltage",      "precision": 2},
            {"key": "charging_current",      "name": "Charging Current",      "unit": "A",   "formula": "epever_charging_current",      "precision": 2},
            {"key": "charging_power",        "name": "Charging Power",        "unit": "W",   "formula": "epever_charging_power",        "precision": 1},

            # ------------- Load side -------------
            {"key": "load_voltage",          "name": "Load Voltage",          "unit": "V",   "formula": "epever_load_voltage",          "precision": 2},
            {"key": "load_current",          "name": "Load Current",          "unit": "A",   "formula": "epever_load_current",          "precision": 2},
            {"key": "load_power",            "name": "Load Power",            "unit": "W",   "formula": "epever_load_power",            "precision": 1},

            # ------------- Min/max voltages today -------------
            {"key": "max_pv_voltage_today",     "name": "Max PV Voltage Today",     "unit": "V", "formula": "epever_max_pv_voltage_today",    "precision": 2},
            {"key": "min_pv_voltage_today",     "name": "Min PV Voltage Today",     "unit": "V", "formula": "epever_min_pv_voltage_today",    "precision": 2},
            {"key": "max_batt_voltage_today",   "name": "Max Battery Voltage Today","unit": "V", "formula": "epever_max_batt_voltage_today",  "precision": 2},
            {"key": "min_batt_voltage_today",   "name": "Min Battery Voltage Today","unit": "V", "formula": "epever_min_batt_voltage_today",  "precision": 2},

            # ------------- Energy – Consumed -------------
            {"key": "energy_consumed_today",  "name": "Energy Consumed Today",  "unit": "Wh",  "formula": "epever_energy_consumed_today"},
            {"key": "energy_consumed_month",  "name": "Energy Consumed Month",  "unit": "Wh",  "formula": "epever_energy_consumed_month"},
            {"key": "energy_consumed_year",   "name": "Energy Consumed Year",   "unit": "kWh", "formula": "epever_energy_consumed_year",  "precision": 2},
            {"key": "energy_consumed_total",  "name": "Energy Consumed Total",  "unit": "kWh", "formula": "epever_energy_consumed_total",  "precision": 2},

            # ------------- Energy – Generated -------------
            {"key": "energy_generated_today", "name": "Energy Generated Today", "unit": "Wh",  "formula": "epever_energy_generated_today"},
            {"key": "energy_generated_month", "name": "Energy Generated Month", "unit": "Wh",  "formula": "epever_energy_generated_month"},
            {"key": "energy_generated_year",  "name": "Energy Generated Year",  "unit": "kWh", "formula": "epever_energy_generated_year", "precision": 2},
            {"key": "energy_generated_total", "name": "Energy Generated Total", "unit": "kWh", "formula": "epever_energy_generated_total", "precision": 2},

            # Approximate Ah generated today (assuming ~12 V)
            {"key": "generated_charge_today", "name": "Generated Charge Today", "unit": "Ah", "formula": "epever_generated_charge_today", "precision": 2},

            # ------------- CO₂ Reduction -------------
            {"key": "co2_reduction", "name": "CO₂ Reduction", "unit": "kg", "formula": "epever_co2_reduction", "precision": 1},

            # ------------- Status codes (just expose) -------------
            {"key": "battery_status_code",  "name": "Battery Status Code",  "formula": "epever_battery_status_code"},
            {"key": "charger_status_code",  "name": "Charger Status Code",  "formula": "epever_charger_status_code"},
            {"key": "charging_mode_code",   "name": "Charging Mode Code",   "formula": "epever_charging_mode_code"},
        ]
    },
}
