from __future__ import annotations

import logging
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, DEVICE_TYPES
from .modbus_client import EpeverModbusClient
from .coordinator import EpeverCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


# ================================================================
#   SETUP ENTRY
# ================================================================
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Epever Modbus device from a config entry."""

    host = entry.data["host"]
    port = entry.data["port"]
    slave = entry.data["slave"]
    name = entry.data["name"]
    device_type = entry.data["device_type"]

    profile = DEVICE_TYPES.get(device_type)
    if profile is None:
        _LOGGER.error("Unknown device type: %s", device_type)
        return False

    # ------------------------------------------------------------
    # Create Modbus client
    # ------------------------------------------------------------
    client = EpeverModbusClient(
        host=host,
        port=port,
        slave=slave,
    )

    try:
        await client.connect()
        _LOGGER.info("Connected to Epever device %s at %s:%s", name, host, port)
    except Exception as err:
        _LOGGER.error("Modbus connection failed: %s", err)
        return False

    # ------------------------------------------------------------
    # Create coordinator (polling every 5 seconds)
    # ------------------------------------------------------------
    coordinator = EpeverCoordinator(
        hass=hass,
        client=client,
        profile=profile,
        device_name=name,
        update_interval=5,
    )

    # Initial data load
    await coordinator.async_config_entry_first_refresh()

    # Store for access by platforms + services
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
        "profile": profile,
        "name": name,
        "device_id": entry.entry_id,   # required for service targeting
    }


    # ------------------------------------------------------------
    # Load platform(s)
    # ------------------------------------------------------------
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


# ================================================================
#   UNLOAD ENTRY
# ================================================================
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a Epever Modbus config entry."""
    data = hass.data[DOMAIN].pop(entry.entry_id)

    client: EpeverModbusClient = data["client"]
    await client.close()

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return unload_ok
