"""Joulo sensor platform."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import (
    JouloEnergyCoordinator,
    JouloSessionsCoordinator,
    JouloWidgetCoordinator,
)


# ---------------------------------------------------------------------------
# Sensor descriptions
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class JouloSensorEntityDescription(SensorEntityDescription):
    value_fn: Any = None


ENERGY_SENSORS: tuple[JouloSensorEntityDescription, ...] = (
    JouloSensorEntityDescription(
        key="total_kwh",
        name="Totaal geladen",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("total_kwh"),
    ),
    JouloSensorEntityDescription(
        key="total_ere_credits",
        name="Totale ERE-credits",
        native_unit_of_measurement="credits",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("total_ere_credits"),
    ),
    JouloSensorEntityDescription(
        key="total_sessions",
        name="Totaal aantal sessies",
        native_unit_of_measurement="sessies",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("total_sessions"),
    ),
)

SESSIONS_SENSORS: tuple[JouloSensorEntityDescription, ...] = (
    JouloSensorEntityDescription(
        key="last_session_kwh",
        name="Laatste sessie kWh",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d["sessions"][0]["kwh"] if d.get("sessions") else None,
    ),
    JouloSensorEntityDescription(
        key="last_session_ere",
        name="Laatste sessie ERE-credits",
        native_unit_of_measurement="credits",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d["sessions"][0].get("ere_credits") if d.get("sessions") else None,
    ),
    JouloSensorEntityDescription(
        key="last_session_started_at",
        name="Laatste sessie gestart",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda d: d["sessions"][0].get("started_at") if d.get("sessions") else None,
    ),
    JouloSensorEntityDescription(
        key="last_session_ended_at",
        name="Laatste sessie beëindigd",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda d: d["sessions"][0].get("ended_at") if d.get("sessions") else None,
    ),
    JouloSensorEntityDescription(
        key="last_session_charger",
        name="Laatste sessie laadpaal",
        value_fn=lambda d: d["sessions"][0].get("charger_nickname") if d.get("sessions") else None,
    ),
)

WIDGET_SENSORS: tuple[JouloSensorEntityDescription, ...] = (
    JouloSensorEntityDescription(
        key="widget_total_kwh",
        name="Widget totaal kWh",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("total_kwh"),
    ),
    JouloSensorEntityDescription(
        key="widget_total_ere",
        name="Widget totale ERE",
        native_unit_of_measurement="credits",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("total_ere"),
    ),
    JouloSensorEntityDescription(
        key="earnings_low",
        name="Verdiensten laag tarief",
        native_unit_of_measurement="EUR",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("earnings_low"),
    ),
    JouloSensorEntityDescription(
        key="earnings_mid",
        name="Verdiensten midden tarief",
        native_unit_of_measurement="EUR",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("earnings_mid"),
    ),
    JouloSensorEntityDescription(
        key="earnings_high",
        name="Verdiensten hoog tarief",
        native_unit_of_measurement="EUR",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("earnings_high"),
    ),
    JouloSensorEntityDescription(
        key="co2_saved_kg",
        name="CO₂ bespaard",
        native_unit_of_measurement="kg",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("co2_saved_kg"),
    ),
    JouloSensorEntityDescription(
        key="effective_fee_pct",
        name="Effectieve vergoeding",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("effective_fee_pct"),
    ),
    JouloSensorEntityDescription(
        key="ere_price_mid",
        name="ERE prijs midden",
        native_unit_of_measurement="EUR/credit",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("ere_price_mid"),
    ),
)


# ---------------------------------------------------------------------------
# Platform setup
# ---------------------------------------------------------------------------

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Joulo sensor entities."""
    data = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = []

    energy_coord: JouloEnergyCoordinator = data["energy"]
    for desc in ENERGY_SENSORS:
        entities.append(JouloSensor(energy_coord, desc, entry.entry_id))

    sessions_coord: JouloSessionsCoordinator = data["sessions"]
    for desc in SESSIONS_SENSORS:
        entities.append(JouloSensor(sessions_coord, desc, entry.entry_id))

    if "widget" in data:
        widget_coord: JouloWidgetCoordinator = data["widget"]
        for desc in WIDGET_SENSORS:
            entities.append(JouloSensor(widget_coord, desc, entry.entry_id))

    async_add_entities(entities)


# ---------------------------------------------------------------------------
# Entity class
# ---------------------------------------------------------------------------

class JouloSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Joulo sensor."""

    entity_description: JouloSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator,
        description: JouloSensorEntityDescription,
        entry_id: str,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name="Joulo",
            manufacturer="Joulo",
            model="REST API",
            configuration_url="https://joulo.nl/dashboard",
        )

    @property
    def native_value(self):
        """Return sensor value."""
        if self.coordinator.data is None:
            return None
        try:
            return self.entity_description.value_fn(self.coordinator.data)
        except (KeyError, IndexError, TypeError):
            return None
