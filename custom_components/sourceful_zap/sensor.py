"""Support for P1 Reader sensors."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL, UnitOfPower
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    CONF_ENDPOINT,
    CONF_SYSTEM_ENDPOINT,
    DEFAULT_ENDPOINT,
    DEFAULT_HOST,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SYSTEM_ENDPOINT,
    DOMAIN,
)
from .obis_definitions import SENSOR_DEFINITIONS
from .p1datacoordinator import P1DataCoordinator
from .p1sensor import P1Sensor
from .system_sensor_definitions import SYSTEM_SENSOR_DEFINITIONS
from .systemdatacoordinator import SystemDataCoordinator
from .systemsensor import SystemSensor

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Optional(CONF_ENDPOINT, default=DEFAULT_ENDPOINT): cv.string,
        vol.Optional(CONF_SYSTEM_ENDPOINT, default=DEFAULT_SYSTEM_ENDPOINT): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
    }
)


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
