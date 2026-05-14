"""Constants for the Joulo integration."""

DOMAIN = "joulo"

CONF_API_TOKEN = "api_token"
CONF_WIDGET_TOKEN = "widget_token"

API_BASE = "https://api.joulo.nl/functions/v1/api"
WIDGET_BASE = "https://api.joulo.nl/functions/v1/widget-badge"

SCAN_INTERVAL_ENERGY = 3600    # 1 uur
SCAN_INTERVAL_SESSIONS = 600   # 10 minuten
SCAN_INTERVAL_WIDGET = 300     # 5 minuten
