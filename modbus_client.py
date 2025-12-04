from __future__ import annotations

import asyncio
import logging

from .vendor.pymodbus.client import AsyncModbusTcpClient
from .vendor.pymodbus.exceptions import ModbusException

_LOGGER = logging.getLogger(__name__)


class EpeverModbusClient:
    """Async Modbus TCP client using vendored pymodbus 3.11.4."""

    def __init__(self, host: str, port: int, slave: int):
        self._host = host
        self._port = port
        self._slave = slave
        self._client: AsyncModbusTcpClient | None = None
        self._lock = asyncio.Lock()

    async def connect(self):
        """Connect to the Modbus TCP device."""
        _LOGGER.debug("Connecting to Modbus %s:%s", self._host, self._port)

        try:
            self._client = AsyncModbusTcpClient(
                host=self._host,
                port=self._port,
            )

            await self._client.connect()

            if not self._client.connected:
                raise ConnectionError("Failed to connect to Modbus device")

            _LOGGER.info("Connected to Modbus device at %s:%s", self._host, self._port)

        except Exception as err:
            _LOGGER.error("Modbus connection error: %s", err)
            raise

    async def close(self):
        """Close the connection."""
        if self._client:
            await self._client.close()
            _LOGGER.info("Closed Modbus connection")
            self._client = None

    async def read_register(self, register: int, count: int = 1, reg_type: str = "input"):
        """
        Read input or holding registers.

        reg_type:
            "input"   -> function 0x04
            "holding" -> function 0x03
        """
        if not self._client:
            await self.connect()

        async with self._lock:
            try:
                if reg_type == "input":
                    resp = await self._client.read_input_registers(
                        address=register,
                        count=count,
                        device_id=self._slave,
                    )
                else:
                    resp = await self._client.read_holding_registers(
                        address=register,
                        count=count,
                        device_id=self._slave,
                    )

            except ModbusException as err:
                _LOGGER.error("Modbus error reg 0x%04X: %s", register, err)
                return None
            except Exception as err:
                _LOGGER.error("Unexpected Modbus error reg 0x%04X: %s", register, err)
                return None

        if not resp or resp.isError():
            _LOGGER.error("Bad Modbus response reg 0x%04X: %s", register, resp)
            return None

        return resp.registers

    async def read_int(self, register: int, reg_type: str = "input") -> int | None:
        """Read a single register and return its integer value."""
        values = await self.read_register(register, 1, reg_type=reg_type)
        if not values:
            return None
        return values[0]
