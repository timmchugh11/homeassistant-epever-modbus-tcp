from __future__ import annotations

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# ============================================================
#  SCALING HELPERS
# ============================================================

def _scale_100(raw):
    """Scale register with factor 0.01."""
    return raw * 0.01 if raw is not None else None


def _scale_10(raw):
    """Scale register with factor 10."""
    return raw * 10.0 if raw is not None else None


def _scale_kwh_001(raw):
    """Scale register with factor 0.01 to kWh."""
    return raw * 0.01 if raw is not None else None


def _signed_int32(val: int | None) -> int | None:
    """Convert 32-bit unsigned to signed."""
    if val is None:
        return None
    if val & 0x80000000:
        return val - 0x100000000
    return val


# ============================================================
#  FORMULA FUNCTIONS (match const.py formula names)
# ============================================================

# ----- Rated values -----

def epever_array_rated_voltage(d):
    return _scale_100(d.get("array_rated_voltage_raw"))


def epever_array_rated_current(d):
    return _scale_100(d.get("array_rated_current_raw"))


def epever_array_rated_power(d):
    # 32-bit register, already combined in coordinator
    return _scale_100(d.get("array_rated_power_raw"))


def epever_battery_rated_voltage(d):
    return _scale_100(d.get("battery_rated_voltage_raw"))


def epever_battery_rated_current(d):
    return _scale_100(d.get("battery_rated_current_raw"))


def epever_battery_rated_power(d):
    return _scale_100(d.get("battery_rated_power_raw"))


# ----- Battery realtime -----

def epever_battery_voltage(d):
    # 0x331A, voltage /100
    return _scale_100(d.get("battery_voltage_raw"))


def epever_battery_current(d):
    # 0x331B/0x331C combined 32-bit, signed, A/100
    raw = _signed_int32(d.get("battery_current_raw"))
    return raw * 0.01 if raw is not None else None


def epever_battery_soc(d):
    # 0x311A, already percent
    return d.get("battery_soc_raw")


def epever_battery_temperature(d):
    # 0x3110, °C/100
    return _scale_100(d.get("battery_temp_raw"))


# ----- Device temperatures -----

def epever_device_temperature(d):
    # 0x3111, °C/100
    return _scale_100(d.get("device_temp_raw"))


def epever_component_temperature(d):
    # 0x3112, °C/100
    return _scale_100(d.get("component_temp_raw"))


# ----- Charging side (controller → battery) -----

def epever_charging_voltage(d):
    return _scale_100(d.get("charging_voltage_raw"))


def epever_charging_current(d):
    return _scale_100(d.get("charging_current_raw"))


def epever_charging_power(d):
    # 32-bit, W/100
    return _scale_100(d.get("charging_power_raw"))


# ----- Load side -----

def epever_load_voltage(d):
    return _scale_100(d.get("load_voltage_raw"))


def epever_load_current(d):
    return _scale_100(d.get("load_current_raw"))


def epever_load_power(d):
    # 32-bit, W/100
    return _scale_100(d.get("load_power_raw"))


# ----- Min/max voltages today -----

def epever_max_pv_voltage_today(d):
    return _scale_100(d.get("max_pv_today_raw"))


def epever_min_pv_voltage_today(d):
    return _scale_100(d.get("min_pv_today_raw"))


def epever_max_batt_voltage_today(d):
    return _scale_100(d.get("max_batt_today_raw"))


def epever_min_batt_voltage_today(d):
    return _scale_100(d.get("min_batt_today_raw"))


# ----- Energy – consumed -----
# Match your template:
#   Today/month: raw * 10  -> Wh
#   Year/total:  raw * 0.01 -> kWh

def epever_energy_consumed_today(d):
    return _scale_10(d.get("consumed_today_raw"))


def epever_energy_consumed_month(d):
    return _scale_10(d.get("consumed_month_raw"))


def epever_energy_consumed_year(d):
    return _scale_kwh_001(d.get("consumed_year_raw"))


def epever_energy_consumed_total(d):
    return _scale_kwh_001(d.get("consumed_total_raw"))


# ----- Energy – generated -----

def epever_energy_generated_today(d):
    return _scale_10(d.get("generated_today_raw"))


def epever_energy_generated_month(d):
    return _scale_10(d.get("generated_month_raw"))


def epever_energy_generated_year(d):
    return _scale_kwh_001(d.get("generated_year_raw"))


def epever_energy_generated_total(d):
    return _scale_kwh_001(d.get("generated_total_raw"))


def epever_generated_charge_today(d):
    """
    ESPHome-style extra: approximate Ah generated today,
    assuming ~12 V system: Wh_today / 12.
    """
    wh_today = epever_energy_generated_today(d)
    return wh_today / 12.0 if wh_today is not None else None


# ----- CO₂ reduction -----

def epever_co2_reduction(d):
    # co2_raw * 10 -> kg, like your template
    return _scale_10(d.get("co2_raw"))


# ----- Status codes (just expose raw) -----

def epever_battery_status_code(d):
    return d.get("battery_status_raw")


def epever_charger_status_code(d):
    return d.get("charger_status_raw")


def epever_charging_mode_code(d):
    return d.get("charging_mode_raw")

# ------ PV side -----
def epever_pv_voltage(d):
    return _scale_100(d.get("pv_voltage_raw"))

def epever_pv_current(d):
    return _scale_100(d.get("pv_current_raw"))

def epever_pv_power(d):
    # 32-bit, W/100
    return _scale_100(d.get("pv_power_raw"))

# ============================================================
#  FORMULA MAP (MUST MATCH const.py "formula" VALUES)
# ============================================================

FORMULAS = {
    # Rated values
    "epever_array_rated_voltage": epever_array_rated_voltage,
    "epever_array_rated_current": epever_array_rated_current,
    "epever_array_rated_power":   epever_array_rated_power,

    "epever_battery_rated_voltage": epever_battery_rated_voltage,
    "epever_battery_rated_current": epever_battery_rated_current,
    "epever_battery_rated_power":   epever_battery_rated_power,

    # Battery realtime
    "epever_battery_voltage":     epever_battery_voltage,
    "epever_battery_current":     epever_battery_current,
    "epever_battery_soc":         epever_battery_soc,
    "epever_battery_temperature": epever_battery_temperature,

    # Device temps
    "epever_device_temperature":    epever_device_temperature,
    "epever_component_temperature": epever_component_temperature,

    # Charging side
    "epever_charging_voltage": epever_charging_voltage,
    "epever_charging_current": epever_charging_current,
    "epever_charging_power":   epever_charging_power,

    # Load side
    "epever_load_voltage": epever_load_voltage,
    "epever_load_current": epever_load_current,
    "epever_load_power":   epever_load_power,

    # PV side
    "epever_pv_voltage": epever_pv_voltage,
    "epever_pv_current": epever_pv_current,
    "epever_pv_power":   epever_pv_power,

    # Min/max voltages today
    "epever_max_pv_voltage_today":   epever_max_pv_voltage_today,
    "epever_min_pv_voltage_today":   epever_min_pv_voltage_today,
    "epever_max_batt_voltage_today": epever_max_batt_voltage_today,
    "epever_min_batt_voltage_today": epever_min_batt_voltage_today,

    # Energy – consumed
    "epever_energy_consumed_today": epever_energy_consumed_today,
    "epever_energy_consumed_month": epever_energy_consumed_month,
    "epever_energy_consumed_year":  epever_energy_consumed_year,
    "epever_energy_consumed_total": epever_energy_consumed_total,

    # Energy – generated
    "epever_energy_generated_today": epever_energy_generated_today,
    "epever_energy_generated_month": epever_energy_generated_month,
    "epever_energy_generated_year":  epever_energy_generated_year,
    "epever_energy_generated_total": epever_energy_generated_total,

    # Ah estimate from generated energy
    "epever_generated_charge_today": epever_generated_charge_today,

    # CO2
    "epever_co2_reduction": epever_co2_reduction,

    # Status codes
    "epever_battery_status_code": epever_battery_status_code,
    "epever_charger_status_code": epever_charger_status_code,
    "epever_charging_mode_code":  epever_charging_mode_code,
}


# ============================================================
#  RAW SENSOR ENTITY
# ============================================================

class EpeverRawSensor(CoordinatorEntity, SensorEntity):
    """Representation of a raw Modbus register (scaled by coordinator)."""

    def __init__(self, coordinator, device_name, key, cfg):
        super().__init__(coordinator)
        self._key = key
        self._cfg = cfg
        self._dev_name = device_name

        self._attr_name = f"{device_name} {cfg['name']}"
        self._attr_unique_id = f"{device_name}_{key}"
        self._attr_native_unit_of_measurement = cfg.get("unit")

        if cfg.get("category") == "diagnostic":
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._dev_name)},
            "name": self._dev_name,
            "manufacturer": "Epever",
            "model": self.coordinator.profile.get("name", "Epever Device"),
        }


# ============================================================
#  VIRTUAL SENSOR ENTITY
# ============================================================

class EpeverVirtualSensor(CoordinatorEntity, SensorEntity):
    """Representation of a computed / derived sensor."""

    def __init__(self, coordinator, device_name, key, cfg):
        super().__init__(coordinator)
        self._key = key
        self._cfg = cfg
        self._dev_name = device_name

        self._attr_name = f"{device_name} {cfg['name']}"
        self._attr_unique_id = f"{device_name}_{key}"
        self._attr_native_unit_of_measurement = cfg.get("unit")

    @property
    def native_value(self):
        d = self.coordinator.data
        formula_name = self._cfg["formula"]

        try:
            func = FORMULAS.get(formula_name)
            if not func:
                _LOGGER.error("No formula '%s' defined for virtual sensor '%s'", formula_name, self._key)
                return None

            val = func(d)

            precision = self._cfg.get("precision")
            if precision is not None and val is not None:
                val = round(val, precision)

            return val

        except Exception as e:
            _LOGGER.error("Error computing virtual sensor '%s' (formula '%s'): %s",
                          self._key, formula_name, e)
            return None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._dev_name)},
            "name": self._dev_name,
            "manufacturer": "Epever",
            "model": self.coordinator.profile.get("name", "Epever Device"),
        }


# ============================================================
#  ENTITY LOADER
# ============================================================

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up all sensors for this integration."""
    data = hass.data[DOMAIN][entry.entry_id]

    coordinator = data["coordinator"]
    profile = data["profile"]
    device_name = entry.data["name"]

    entities = []

    # RAW registers
    for sensor_cfg in profile["sensors"]:
        entities.append(
            EpeverRawSensor(
                coordinator,
                device_name,
                sensor_cfg["key"],
                sensor_cfg,
            )
        )

    # VIRTUAL sensors
    for vcfg in profile.get("virtual_sensors", []):
        entities.append(
            EpeverVirtualSensor(
                coordinator,
                device_name,
                vcfg["key"],
                vcfg,
            )
        )

    async_add_entities(entities)
