from __future__ import annotations
from typing import Any
from homeassistant.core import HomeAssistant

class SpeedTestClient:
    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass

    def _run_test_sync(self) -> dict[str, Any]:
        import speedtest  # provided by requirement in manifest
        st = speedtest.Speedtest()
        st.get_servers()
        st.get_best_server()
        st.download()
        st.upload(pre_allocate=False)
        return st.results.dict()

    async def async_run_test(self) -> dict[str, Any]:
        return await self._hass.async_add_executor_job(self._run_test_sync)
