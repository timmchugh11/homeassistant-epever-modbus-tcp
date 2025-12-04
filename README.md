
# Epever Modbus TCP Integration for Home Assistant

Custom Home Assistant integration that provides **full Modbus TCP support for Epever solar controllers.

This integration exposes **raw Modbus registers** as Home Assistant sensors, and includes **automatic scaling, bit decoding, human-readable states**, and optional **template helpers**.

## Features
- Reads Epever Modbus TCP registers
- Converts raw register data into battery and charger metrics
- High-resolution 32-bit register support
- Automatic scaling for Epever formats
- Works entirely over Modbus TCP
- Template-friendly

## Installation
Copy the integration into your Home Assistant custom_components directory and restart Home Assistant.

## Configuration
Use the UI intergration to enter the IP, port Address and device

## Entities Created
Includes sensors for PV and battery information such as:
- Voltage
- Current
- Temperature
- State of Charge
- Charger Status

## Contributing
PRs welcome!

## Support
Star the repo if helpful.
