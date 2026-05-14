"""Config flow for Joulo integration."""
from __future__ import annotations

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    API_BASE,
    CONF_API_TOKEN,
    CONF_WIDGET_TOKEN,
    DOMAIN,
    WIDGET_BASE,
)


async def _validate_api_token(hass: HomeAssistant, token: str) -> str | None:
    """Return None on success, or an error key string on failure."""
    url = f"{API_BASE}/energy"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 401 or resp.status == 403:
                    return "invalid_auth"
                if resp.status != 200:
                    return "cannot_connect"
    except aiohttp.ClientError:
        return "cannot_connect"
    return None


async def _validate_widget_token(hass: HomeAssistant, token: str) -> bool:
    """Return True if widget token is valid."""
    url = f"{WIDGET_BASE}?token={token}&format=json"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                return resp.status == 200
    except aiohttp.ClientError:
        return False


class JouloConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the Joulo config flow."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_API_TOKEN][:8])
            self._abort_if_unique_id_configured()

            error = await _validate_api_token(self.hass, user_input[CONF_API_TOKEN])
            if error:
                errors["base"] = error
            else:
                # Optioneel widget token valideren
                widget_token = user_input.get(CONF_WIDGET_TOKEN, "").strip()
                if widget_token:
                    valid = await _validate_widget_token(self.hass, widget_token)
                    if not valid:
                        errors[CONF_WIDGET_TOKEN] = "invalid_auth"

                if not errors:
                    data = {CONF_API_TOKEN: user_input[CONF_API_TOKEN]}
                    if widget_token:
                        data[CONF_WIDGET_TOKEN] = widget_token
                    return self.async_create_entry(title="Joulo", data=data)

        schema = vol.Schema(
            {
                vol.Required(CONF_API_TOKEN): str,
                vol.Optional(CONF_WIDGET_TOKEN, default=""): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
