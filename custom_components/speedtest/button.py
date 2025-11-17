from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType

from .const import DOMAIN
from .coordinator import InternetSpeedCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    coordinator: InternetSpeedCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RunSpeedTestButton(coordinator)])

class RunSpeedTestButton(CoordinatorEntity[InternetSpeedCoordinator], ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = "Run speed test now"
    _attr_icon = "mdi:speedometer"
    _attr_unique_id = "speedtest_run_now"
    _attr_device_info = DeviceInfo(
        identifiers={(DOMAIN, "speedtestdotnet")},
        name="SpeedTest",
        manufacturer="Custom",
        entry_type=DeviceEntryType.SERVICE,
    )

    async def async_press(self) -> None:
        await self.coordinator.async_request_refresh()
