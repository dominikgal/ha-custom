from __future__ import annotations
from datetime import timedelta
from typing import Any
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .speedtest_client import SpeedTestClient

_LOGGER = logging.getLogger(__name__)

class InternetSpeedCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.client = SpeedTestClient(hass)
        interval = entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
        super().__init__(
            hass,
            _LOGGER,
            name="Internet Speed",
            update_interval=timedelta(seconds=interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.client.async_run_test()
        except Exception as err:
            raise UpdateFailed(str(err)) from err
