"""Joulo integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_API_TOKEN, CONF_WIDGET_TOKEN, DOMAIN
from .coordinator import (
    JouloEREPositionCoordinator,
    JouloEnergyCoordinator,
    JouloSessionsCoordinator,
    JouloWidgetCoordinator,
)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Joulo from a config entry."""
    api_token = entry.data[CONF_API_TOKEN]
    widget_token = entry.data.get(CONF_WIDGET_TOKEN)

    energy_coordinator = JouloEnergyCoordinator(hass, api_token)
    sessions_coordinator = JouloSessionsCoordinator(hass, api_token)
    ere_position_coordinator = JouloEREPositionCoordinator(hass, api_token)

    await energy_coordinator.async_config_entry_first_refresh()
    await sessions_coordinator.async_config_entry_first_refresh()
    await ere_position_coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "energy": energy_coordinator,
        "sessions": sessions_coordinator,
        "ere_position": ere_position_coordinator,
    }

    if widget_token:
        widget_coordinator = JouloWidgetCoordinator(hass, widget_token)
        await widget_coordinator.async_config_entry_first_refresh()
        hass.data[DOMAIN][entry.entry_id]["widget"] = widget_coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Joulo config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
