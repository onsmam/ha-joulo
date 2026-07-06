"""DataUpdateCoordinator for Joulo."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_BASE,
    CONF_API_TOKEN,
    CONF_WIDGET_TOKEN,
    DOMAIN,
    SCAN_INTERVAL_ENERGY,
    SCAN_INTERVAL_ERE_POSITION,
    SCAN_INTERVAL_SESSIONS,
    SCAN_INTERVAL_WIDGET,
    WIDGET_BASE,
)

_LOGGER = logging.getLogger(__name__)


class JouloEnergyCoordinator(DataUpdateCoordinator):
    """Coordinator for /energy endpoint."""

    def __init__(self, hass: HomeAssistant, token: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_energy",
            update_interval=timedelta(seconds=SCAN_INTERVAL_ENERGY),
        )
        self._token = token

    async def _async_update_data(self) -> dict:
        url = f"{API_BASE}/energy"
        headers = {"Authorization": f"Bearer {self._token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 401:
                        raise ConfigEntryAuthFailed("Authenticatie verlopen of gewijzigd. API key/token voor Joulo energy vernieuwen.")
                    if resp.status >= 500:
                        _LOGGER.warning("Joulo /energy HTTP %s, keeping last data", resp.status)
                        return self.data
                    if resp.status != 200:
                        raise UpdateFailed(f"Joulo /energy HTTP {resp.status}")
                    return await resp.json()
        except asyncio.TimeoutError:
            _LOGGER.warning("Joulo /energy timed out, keeping last data")
            return self.data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Joulo /energy connection error: {err}") from err


class JouloSessionsCoordinator(DataUpdateCoordinator):
    """Coordinator for /sessions endpoint."""

    def __init__(self, hass: HomeAssistant, token: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_sessions",
            update_interval=timedelta(seconds=SCAN_INTERVAL_SESSIONS),
        )
        self._token = token

    async def _async_update_data(self) -> dict:
        url = f"{API_BASE}/sessions?limit=10"
        headers = {"Authorization": f"Bearer {self._token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 401:
                        raise ConfigEntryAuthFailed("Authenticatie verlopen of gewijzigd. API key/token voor Joulo sessions vernieuwen.")
                    if resp.status >= 500:
                        _LOGGER.warning("Joulo /sessions HTTP %s, keeping last data", resp.status)
                        return self.data
                    if resp.status != 200:
                        raise UpdateFailed(f"Joulo /sessions HTTP {resp.status}")
                    return await resp.json()
        except asyncio.TimeoutError:
            _LOGGER.warning("Joulo /sessions timed out, keeping last data")
            return self.data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Joulo /sessions connection error: {err}") from err


class JouloEREPositionCoordinator(DataUpdateCoordinator):
    """Coordinator for /ere-position endpoint."""

    def __init__(self, hass: HomeAssistant, token: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_ere_position",
            update_interval=timedelta(seconds=SCAN_INTERVAL_ERE_POSITION),
        )
        self._token = token

    async def _async_update_data(self) -> dict:
        url = f"{API_BASE}/ere-position"
        headers = {"Authorization": f"Bearer {self._token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 401:
                        raise ConfigEntryAuthFailed("Authenticatie verlopen of gewijzigd. API key/token voor Joulo vernieuwen.")
                    if resp.status >= 500:
                        _LOGGER.warning("Joulo /ere-position HTTP %s, keeping last data", resp.status)
                        return self.data
                    if resp.status != 200:
                        raise UpdateFailed(f"Joulo /ere-position HTTP {resp.status}")
                    return await resp.json()
        except asyncio.TimeoutError:
            _LOGGER.warning("Joulo /ere-position timed out, keeping last data")
            return self.data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Joulo /ere-position connection error: {err}") from err


class JouloWidgetCoordinator(DataUpdateCoordinator):
    """Coordinator for /widget-badge endpoint."""

    def __init__(self, hass: HomeAssistant, token: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_widget",
            update_interval=timedelta(seconds=SCAN_INTERVAL_WIDGET),
        )
        self._token = token

    async def _async_update_data(self) -> dict:
        url = f"{WIDGET_BASE}?token={self._token}&format=json"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status >= 500:
                        _LOGGER.warning("Joulo /widget-badge HTTP %s, keeping last data", resp.status)
                        return self.data
                    if resp.status != 200:
                        raise UpdateFailed(f"Joulo /widget-badge HTTP {resp.status}")
                    return await resp.json()
        except asyncio.TimeoutError:
            _LOGGER.warning("Joulo /widget-badge timed out, keeping last data")
            return self.data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Joulo /widget-badge connection error: {err}") from err
