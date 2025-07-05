"""Support for P1 Reader sensors."""

from __future__ import annotations

import logging
from datetime import timedelta
import re
from typing import Any

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
    PLATFORM_SCHEMA,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
    UnitOfPower,
    UnitOfEnergy,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "p1_reader"
DEFAULT_NAME = "Zap"
DEFAULT_HOST = "zap.local"
DEFAULT_ENDPOINT = "/api/data/p1/obis"
DEFAULT_SYSTEM_ENDPOINT = "/api/system"
DEFAULT_SCAN_INTERVAL = timedelta(seconds=10)

CONF_ENDPOINT = "endpoint"
CONF_SYSTEM_ENDPOINT = "system_endpoint"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Optional(CONF_ENDPOINT, default=DEFAULT_ENDPOINT): cv.string,
        vol.Optional(CONF_SYSTEM_ENDPOINT, default=DEFAULT_SYSTEM_ENDPOINT): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
    }
)

# Define OBIS code mappings
SENSOR_DEFINITIONS = {
    "1-0:1.8.0": {
        "name": "Total Energy Import",
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:transmission-tower-import",
    },
    "1-0:2.8.0": {
        "name": "Total Energy Export",
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:transmission-tower-export",
    },
    "1-0:1.7.0": {
        "name": "Current Power Import",
        "unit": UnitOfPower.KILO_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:flash",
    },
    "1-0:2.7.0": {
        "name": "Current Power Export",
        "unit": UnitOfPower.KILO_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-power",
    },
    "1-0:3.8.0": {
        "name": "Total Reactive Energy Import",
        "unit": "kVArh",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:sine-wave",
    },
    "1-0:4.8.0": {
        "name": "Total Reactive Energy Export",
        "unit": "kVArh",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:sine-wave",
    },
    "1-0:3.7.0": {
        "name": "Current Reactive Power Import",
        "unit": "kVAr",
        "device_class": SensorDeviceClass.REACTIVE_POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
    },
    "1-0:4.7.0": {
        "name": "Current Reactive Power Export",
        "unit": "kVAr",
        "device_class": SensorDeviceClass.REACTIVE_POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
    },
    # Phase voltages
    "1-0:32.7.0": {
        "name": "Voltage L1",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:flash",
    },
    "1-0:52.7.0": {
        "name": "Voltage L2",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:flash",
    },
    "1-0:72.7.0": {
        "name": "Voltage L3",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:flash",
    },
    # Phase currents
    "1-0:31.7.0": {
        "name": "Current L1",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-ac",
    },
    "1-0:51.7.0": {
        "name": "Current L2",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-ac",
    },
    "1-0:71.7.0": {
        "name": "Current L3",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-ac",
    },
    # Phase power import
    "1-0:21.7.0": {
        "name": "Power L1 Import",
        "unit": UnitOfPower.KILO_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:flash",
    },
    "1-0:41.7.0": {
        "name": "Power L2 Import",
        "unit": UnitOfPower.KILO_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:flash",
    },
    "1-0:61.7.0": {
        "name": "Power L3 Import",
        "unit": UnitOfPower.KILO_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:flash",
    },
    # Phase power export
    "1-0:22.7.0": {
        "name": "Power L1 Export",
        "unit": UnitOfPower.KILO_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-power",
    },
    "1-0:42.7.0": {
        "name": "Power L2 Export",
        "unit": UnitOfPower.KILO_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-power",
    },
    "1-0:62.7.0": {
        "name": "Power L3 Export",
        "unit": UnitOfPower.KILO_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-power",
    },
    # Phase reactive power import
    "1-0:23.7.0": {
        "name": "Reactive Power L1 Import",
        "unit": "kVAr",
        "device_class": SensorDeviceClass.REACTIVE_POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
    },
    "1-0:43.7.0": {
        "name": "Reactive Power L2 Import",
        "unit": "kVAr",
        "device_class": SensorDeviceClass.REACTIVE_POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
    },
    "1-0:63.7.0": {
        "name": "Reactive Power L3 Import",
        "unit": "kVAr",
        "device_class": SensorDeviceClass.REACTIVE_POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
    },
    # Phase reactive power export
    "1-0:24.7.0": {
        "name": "Reactive Power L1 Export",
        "unit": "kVAr",
        "device_class": SensorDeviceClass.REACTIVE_POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
    },
    "1-0:44.7.0": {
        "name": "Reactive Power L2 Export",
        "unit": "kVAr",
        "device_class": SensorDeviceClass.REACTIVE_POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
    },
    "1-0:64.7.0": {
        "name": "Reactive Power L3 Export",
        "unit": "kVAr",
        "device_class": SensorDeviceClass.REACTIVE_POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
    },
}

# System sensor definitions for Zap device information
SYSTEM_SENSOR_DEFINITIONS = {
    "uptime": {
        "name": "Uptime",
        "unit": "s",
        "device_class": SensorDeviceClass.DURATION,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:timer-outline",
        "path": "uptime_seconds",
    },
    "temperature": {
        "name": "Temperature",
        "unit": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "path": "temperature_celsius",
    },
    "memory_percent": {
        "name": "Memory Usage",
        "unit": "%",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:memory",
        "path": "memory_MB.percent_used",
    },
    "memory_used": {
        "name": "Memory Used",
        "unit": "MB",
        "device_class": SensorDeviceClass.DATA_SIZE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:memory",
        "path": "memory_MB.used",
    },
    "memory_free": {
        "name": "Memory Free",
        "unit": "MB",
        "device_class": SensorDeviceClass.DATA_SIZE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:memory",
        "path": "memory_MB.free",
    },
    "wifi_rssi": {
        "name": "WiFi Signal Strength",
        "unit": "dBm",
        "device_class": SensorDeviceClass.SIGNAL_STRENGTH,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:wifi-strength-2",
        "path": "zap.network.rssi",
    },
    "firmware_version": {
        "name": "Firmware Version",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:chip",
        "path": "zap.firmwareVersion",
    },
    "cpu_frequency": {
        "name": "CPU Frequency",
        "unit": "MHz",
        "device_class": SensorDeviceClass.FREQUENCY,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:cpu-32-bit",
        "path": "zap.cpuFreqMHz",
    },
    "flash_size": {
        "name": "Flash Size",
        "unit": "MB",
        "device_class": SensorDeviceClass.DATA_SIZE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:harddisk",
        "path": "zap.flashSizeMB",
    },
    "wifi_status": {
        "name": "WiFi Status",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:wifi",
        "path": "zap.network.wifiStatus",
    },
    "local_ip": {
        "name": "Local IP",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:ip-network",
        "path": "zap.network.localIP",
    },
    "wifi_ssid": {
        "name": "WiFi SSID",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:router-wireless",
        "path": "zap.network.ssid",
    },
    "device_id": {
        "name": "Device ID",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:identifier",
        "path": "zap.deviceId",
    },
}


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the P1 Reader sensors."""
    _LOGGER.debug("Setting up P1 Reader sensors")

    # Get configuration
    host = config.get(CONF_HOST)
    endpoint = config.get(CONF_ENDPOINT)
    system_endpoint = config.get(CONF_SYSTEM_ENDPOINT)
    name = config.get(CONF_NAME)
    scan_interval = config.get(CONF_SCAN_INTERVAL)

    p1_url = f"http://{host}{endpoint}"
    system_url = f"http://{host}{system_endpoint}"

    # Create data coordinators
    p1_coordinator = P1DataCoordinator(hass, p1_url, scan_interval)
    system_coordinator = SystemDataCoordinator(hass, system_url, scan_interval)

    # Create P1 sensors
    sensors = []
    for obis_code, definition in SENSOR_DEFINITIONS.items():
        sensors.append(
            P1Sensor(
                p1_coordinator,
                system_coordinator,
                obis_code,
                definition["name"],
                definition["unit"],
                definition.get("device_class"),
                definition.get("state_class"),
                definition.get("icon"),
                name,
            )
        )

    # Add net power sensor (calculated)
    sensors.append(P1NetPowerSensor(p1_coordinator, system_coordinator, name))

    # Create system sensors
    for sensor_key, definition in SYSTEM_SENSOR_DEFINITIONS.items():
        sensors.append(
            SystemSensor(
                system_coordinator,
                sensor_key,
                definition["name"],
                definition["unit"],
                definition.get("device_class"),
                definition.get("state_class"),
                definition.get("icon"),
                definition["path"],
                name,
            )
        )

    async_add_entities(sensors, True)


class P1DataCoordinator:
    """Coordinate data fetching for all P1 sensors."""

    def __init__(self, hass: HomeAssistant, url: str, scan_interval: timedelta) -> None:
        """Initialize the data coordinator."""
        self.hass = hass
        self.url = url
        self.data = {}
        self.session = async_get_clientsession(hass)
        self.scan_interval = scan_interval
        self._last_update = None

    @Throttle(DEFAULT_SCAN_INTERVAL)
    async def async_update(self) -> None:
        """Fetch data from API."""
        try:
            async with async_timeout.timeout(10):
                _LOGGER.debug("Fetching data from %s", self.url)
                response = await self.session.get(self.url)
                response.raise_for_status()
                json_data = await response.json()

                if json_data.get("status") == "success":
                    self.data = self._parse_obis_data(json_data.get("data", []))
                    _LOGGER.debug("Successfully parsed %d OBIS codes", len(self.data))
                else:
                    _LOGGER.error(
                        "API returned error status: %s", json_data.get("status")
                    )

        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching P1 data: %s", err)
        except Exception as err:
            _LOGGER.error("Unexpected error fetching P1 data: %s", err)

    def _parse_obis_data(self, data_lines: list[str]) -> dict[str, dict[str, Any]]:
        """Parse OBIS data lines into dictionary."""
        parsed = {}

        # Pattern to match OBIS codes: code(value*unit) or code(value)
        pattern = r"(\d+-\d+:\d+\.\d+\.\d+)\(([0-9.-]+)\*?([^)]*)\)"

        for line in data_lines:
            match = re.match(pattern, line)
            if match:
                obis_code = match.group(1)
                try:
                    value = float(match.group(2))
                    unit = match.group(3) if match.group(3) else None
                    parsed[obis_code] = {"value": value, "unit": unit}
                except ValueError:
                    _LOGGER.warning("Could not parse value from line: %s", line)
            else:
                # Handle timestamp format: 0-0:1.0.0(250705142950W)
                if line.startswith("0-0:1.0.0"):
                    _LOGGER.debug("Timestamp: %s", line)
                else:
                    _LOGGER.debug("Could not parse line: %s", line)

        return parsed


class P1Sensor(SensorEntity):
    """Representation of a P1 meter sensor."""

    def __init__(
        self,
        coordinator: P1DataCoordinator,
        system_coordinator: SystemDataCoordinator,
        obis_code: str,
        sensor_name: str,
        unit: str,
        device_class: SensorDeviceClass | None = None,
        state_class: SensorStateClass | None = None,
        icon: str | None = None,
        name_prefix: str = DEFAULT_NAME,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.system_coordinator = system_coordinator
        self.obis_code = obis_code
        self._attr_name = f"{name_prefix} {sensor_name}"
        self._attr_unique_id = (
            f"{name_prefix.lower().replace(' ', '_')}_"
            f"{obis_code.replace(':', '_').replace('-', '_')}"
        )
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_icon = icon
        self._attr_native_value = None
        self._attr_available = True

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        device_id = self.system_coordinator.device_info.get("device_id", "unknown")
        firmware_version = self.system_coordinator.device_info.get(
            "firmware_version", "unknown"
        )

        return {
            "identifiers": {(DOMAIN, device_id)},
            "name": "Sourceful Energy Zap",
            "manufacturer": "Sourceful Labs AB",
            "model": "Zap P1 Reader",
            "sw_version": firmware_version,
            "configuration_url": "http://zap.local/",
        }

    async def async_update(self) -> None:
        """Update the sensor."""
        await self.coordinator.async_update()

        if self.obis_code in self.coordinator.data:
            self._attr_native_value = self.coordinator.data[self.obis_code]["value"]
            self._attr_available = True
        else:
            self._attr_available = False
            _LOGGER.debug("OBIS code %s not found in data", self.obis_code)


class P1NetPowerSensor(SensorEntity):
    """Calculated net power sensor (import - export)."""

    def __init__(
        self,
        coordinator: P1DataCoordinator,
        system_coordinator: SystemDataCoordinator,
        name_prefix: str = DEFAULT_NAME,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.system_coordinator = system_coordinator
        self._attr_name = f"{name_prefix} Net Power"
        self._attr_unique_id = f"{name_prefix.lower().replace(' ', '_')}_net_power"
        self._attr_native_unit_of_measurement = UnitOfPower.KILO_WATT
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:home-lightning-bolt"
        self._attr_native_value = None
        self._attr_available = True

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        device_id = self.system_coordinator.device_info.get("device_id", "unknown")
        firmware_version = self.system_coordinator.device_info.get(
            "firmware_version", "unknown"
        )

        return {
            "identifiers": {(DOMAIN, device_id)},
            "name": "Sourceful Energy Zap",
            "manufacturer": "Sourceful Labs AB",
            "model": "Zap P1 Reader",
            "sw_version": firmware_version,
            "configuration_url": "http://zap.local/",
        }

    async def async_update(self) -> None:
        """Update the sensor."""
        await self.coordinator.async_update()

        import_power = self.coordinator.data.get("1-0:1.7.0", {}).get("value", 0)
        export_power = self.coordinator.data.get("1-0:2.7.0", {}).get("value", 0)

        # Net power: positive = importing, negative = exporting
        self._attr_native_value = import_power - export_power
        self._attr_available = True


class SystemDataCoordinator:
    """Coordinate system data fetching for Zap device information."""

    def __init__(self, hass: HomeAssistant, url: str, scan_interval: timedelta) -> None:
        """Initialize the system data coordinator."""
        self.hass = hass
        self.url = url
        self.data = {}
        self.device_info = {}
        self.session = async_get_clientsession(hass)
        self.scan_interval = scan_interval
        self._last_update = None

    @Throttle(DEFAULT_SCAN_INTERVAL)
    async def async_update(self) -> None:
        """Fetch system data from API."""
        try:
            async with async_timeout.timeout(10):
                _LOGGER.debug("Fetching system data from %s", self.url)
                response = await self.session.get(self.url)
                response.raise_for_status()
                self.data = await response.json()

                # Extract device info for Home Assistant device registry
                if "zap" in self.data:
                    self.device_info = {
                        "device_id": self.data["zap"].get("deviceId", "unknown"),
                        "firmware_version": self.data["zap"].get(
                            "firmwareVersion", "unknown"
                        ),
                        "sdk_version": self.data["zap"].get("sdkVersion", "unknown"),
                        "local_ip": self.data["zap"]
                        .get("network", {})
                        .get("localIP", "unknown"),
                    }

                _LOGGER.debug("Successfully fetched system data")

        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching system data: %s", err)
        except Exception as err:
            _LOGGER.error("Unexpected error fetching system data: %s", err)

    def get_nested_value(self, path: str) -> Any:
        """Get nested value from data using dot notation."""
        try:
            value = self.data
            for key in path.split("."):
                value = value[key]
            return value
        except (KeyError, TypeError):
            return None


class SystemSensor(SensorEntity):
    """Representation of a Zap system sensor."""

    def __init__(
        self,
        coordinator: SystemDataCoordinator,
        sensor_key: str,
        sensor_name: str,
        unit: str | None,
        device_class: SensorDeviceClass | None = None,
        state_class: SensorStateClass | None = None,
        icon: str | None = None,
        data_path: str = "",
        name_prefix: str = DEFAULT_NAME,
    ) -> None:
        """Initialize the system sensor."""
        self.coordinator = coordinator
        self.sensor_key = sensor_key
        self.data_path = data_path
        self._attr_name = f"{name_prefix} {sensor_name}"
        self._attr_unique_id = (
            f"{name_prefix.lower().replace(' ', '_')}_system_{sensor_key}"
        )
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_icon = icon
        self._attr_native_value = None
        self._attr_available = True

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        device_id = self.coordinator.device_info.get("device_id", "unknown")
        firmware_version = self.coordinator.device_info.get(
            "firmware_version", "unknown"
        )

        return {
            "identifiers": {(DOMAIN, device_id)},
            "name": "Sourceful Energy Zap",
            "manufacturer": "Sourceful Labs AB",
            "model": "Zap P1 Reader",
            "sw_version": firmware_version,
            "configuration_url": "http://zap.local/",
        }

    async def async_update(self) -> None:
        """Update the sensor."""
        await self.coordinator.async_update()

        value = self.coordinator.get_nested_value(self.data_path)
        if value is not None:
            # Round floating point values to 2 decimal places
            if isinstance(value, float):
                self._attr_native_value = round(value, 2)
            else:
                self._attr_native_value = value
            self._attr_available = True
        else:
            self._attr_available = False
            _LOGGER.debug(
                "System sensor %s: No data found at path %s",
                self.sensor_key,
                self.data_path,
            )
