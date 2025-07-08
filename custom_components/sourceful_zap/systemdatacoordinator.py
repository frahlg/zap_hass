"""System Data Coordinator."""

from datetime import timedelta
import logging
from typing import Any

import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import Throttle

from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


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
