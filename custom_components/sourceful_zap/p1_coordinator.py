"""P1 Data Coordinator."""

from datetime import timedelta
import logging
import re
from typing import Any

import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import Throttle

from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


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
