from __future__ import annotations
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import UnitOfDataRate, UnitOfTime, ATTR_ATTRIBUTION
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType

from .const import DOMAIN
from .coordinator import InternetSpeedCoordinator

ATTR_SERVER = "server"
ATTR_IP = "ip"
ATTR_ISP = "isp"
ATTR_TIMESTAMP = "timestamp"
ATTR_BYTES_SENT = "bytes_sent"
ATTR_BYTES_RECEIVED = "bytes_received"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    coordinator: InternetSpeedCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = [
        DownloadSpeedSensor(coordinator),
        UploadSpeedSensor(coordinator),
        PingSensor(coordinator),
    ]
    async_add_entities(entities)

class BaseInternetSpeedSensor(CoordinatorEntity[InternetSpeedCoordinator], SensorEntity):
    _attr_has_entity_name = True
    _attr_device_info = DeviceInfo(
        identifiers={(DOMAIN, "speedtest-dom")},
        name="Internet Speed",
        manufacturer="Custom",
        entry_type=DeviceEntryType.SERVICE,
    )
    _attr_extra_state_attributes: dict[str, Any]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = self.coordinator.data or {}
        server = (data.get("server") or {}) if isinstance(data.get("server"), dict) else {}
        client = (data.get("client") or {}) if isinstance(data.get("client"), dict) else {}
        attrs = {
            ATTR_ATTRIBUTION: "Data provided by speedtest.net",
            ATTR_SERVER: {
                "id": server.get("id"),
                "name": server.get("name"),
                "sponsor": server.get("sponsor"),
                "country": server.get("country"),
                "host": server.get("host"),
            },
            ATTR_IP: client.get("ip"),
            ATTR_ISP: client.get("isp"),
            ATTR_TIMESTAMP: data.get("timestamp"),
            ATTR_BYTES_SENT: data.get("bytes_sent"),
            ATTR_BYTES_RECEIVED: data.get("bytes_received"),
        }
        return attrs

class DownloadSpeedSensor(BaseInternetSpeedSensor):
    _attr_name = "Download"
    _attr_icon = "mdi:download"
    _attr_unique_id = "speedtest-dom_download"
    _attr_native_unit_of_measurement = UnitOfDataRate.MEGABITS_PER_SECOND
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        data = self.coordinator.data or {}
        bps = data.get("download")
        if bps is None:
            return None
        return round(bps / 1_000_000, 2)

class UploadSpeedSensor(BaseInternetSpeedSensor):
    _attr_name = "Upload"
    _attr_icon = "mdi:upload"
    _attr_unique_id = "speedtest-dom_upload"
    _attr_native_unit_of_measurement = UnitOfDataRate.MEGABITS_PER_SECOND
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        data = self.coordinator.data or {}
        bps = data.get("upload")
        if bps is None:
            return None
        return round(bps / 1_000_000, 2)

class PingSensor(BaseInternetSpeedSensor):
    _attr_name = "Ping"
    _attr_icon = "mdi:timer-sand"
    _attr_unique_id = "speedtest-dom_ping"
    _attr_native_unit_of_measurement = UnitOfTime.MILLISECONDS
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        data = self.coordinator.data or {}
        ping = data.get("ping")
        if ping is None:
            return None
        return round(float(ping), 2)
