from __future__ import annotations

import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class EpeverCoordinator(DataUpdateCoordinator):
    """Coordinator for polling Modbus data from an Epever device."""

    def __init__(self, hass, client, profile, device_name, update_interval):
        super().__init__(
            hass,
            _LOGGER,
            name=f"Epever {device_name}",
            update_interval=timedelta(seconds=update_interval),
        )

        self.client = client
        self.profile = profile
        self.device_name = device_name

    async def _async_update_data(self):
        """Fetch data from Modbus and return cleaned, scaled values."""

        result = {}

        try:
            for sensor in self.profile["sensors"]:

                key = sensor["key"]
                reg = sensor["register"]
                # support both "length" and "count"
                count = sensor.get("length") or sensor.get("count") or 1
                reg_type = sensor.get("reg_type") or sensor.get("type")
                scale = sensor.get("scale")

                # Read register(s)
                raw = await self.client.read_register(reg, count=count)

                if raw is None:
                    _LOGGER.warning(
                        "Failed to read register 0x%04X for key '%s'",
                        reg, key
                    )
                    result[key] = None
                    continue

               # 32-bit (2-register) value: [L, H] -> H<<16 | L
                if count == 2:
                    value = (raw[1] << 16) | raw[0]
                else:
                    value = raw[0]
                    if reg_type == "int16" and value > 0x7FFF:
                        value -= 0x10000

                    # Signed conversion
                    if reg_type == "int16" and value > 0x7FFF:
                        value -= 0x10000

                # Apply scale if defined
                if scale:
                    value = value * scale

                result[key] = value

            return result

        except Exception as e:
            _LOGGER.error("Unexpected Modbus update failure: %s", e)
            raise
