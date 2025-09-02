from __future__ import annotations
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, MIN_SCAN_INTERVAL

def _minutes_to_seconds(minutes: int) -> int:
    return int(minutes) * 60

def _seconds_to_minutes(seconds: int) -> int:
    return max(1, int(round(seconds / 60)))

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            minutes = user_input[CONF_SCAN_INTERVAL]
            seconds = _minutes_to_seconds(minutes)
            if seconds < MIN_SCAN_INTERVAL:
                errors["base"] = "interval_too_short"
            else:
                return self.async_create_entry(
                    title="Internet Speed",
                    data={CONF_SCAN_INTERVAL: seconds},
                )

        data_schema = vol.Schema({
            vol.Required(CONF_SCAN_INTERVAL, default=_seconds_to_minutes(DEFAULT_SCAN_INTERVAL)): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440))
        })
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    async def async_step_import(self, user_input: dict) -> FlowResult:
        # Not supporting YAML import; UI-only
        return await self.async_step_user(user_input)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        current_seconds = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        if user_input is not None:
            minutes = user_input[CONF_SCAN_INTERVAL]
            seconds = _minutes_to_seconds(minutes)
            if seconds < MIN_SCAN_INTERVAL:
                errors["base"] = "interval_too_short"
            else:
                return self.async_create_entry(title="", data={CONF_SCAN_INTERVAL: seconds})

        data_schema = vol.Schema({
            vol.Required(CONF_SCAN_INTERVAL, default=_seconds_to_minutes(current_seconds)): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440))
        })
        return self.async_show_form(step_id="init", data_schema=data_schema, errors=errors)

async def async_get_options_flow(config_entry):
    return OptionsFlowHandler(config_entry)
