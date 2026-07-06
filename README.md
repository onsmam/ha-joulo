# Joulo — Home Assistant integratie

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Custom component voor Home Assistant om Joulo laadpaal-data te integreren via de officiële REST API.

## Sensoren

### `/energy` (elk uur)
| Sensor | Eenheid |
|--------|---------|
| Totaal geladen | kWh |
| Totale ERE-credits | credits |
| Totaal aantal sessies | sessies |

### `/sessions` (elke 10 min)
| Sensor | Eenheid |
|--------|---------|
| Laatste sessie kWh | kWh |
| Laatste sessie ERE-credits | credits |
| Laatste sessie gestart | timestamp |
| Laatste sessie beëindigd | timestamp |
| Laatste sessie laadpaal | tekst |

### `/ere-position` (elk uur)
Identiek aan het **ERE-opbrengst** dashboard in het Joulo portaal.

| Sensor | Eenheid |
|--------|---------|
| ERE verwachte jaaropbrengst | EUR |
| ERE opbrengst dit jaar | EUR |
| ERE prognose rest jaar | EUR |
| ERE uitbetaald | EUR |
| ERE uitbetaald credits | ERE |
| ERE klaar voor uitbetaling | EUR |
| ERE klaar voor uitbetaling credits | ERE |
| ERE gereserveerd | EUR |
| ERE gereserveerd credits | ERE |
| ERE gereserveerd prijs | EUR/ERE |
| ERE nog te verkopen | ERE |
| ERE indicatieve prijs | EUR/ERE |
| ERE commissie | % |

### `/widget-badge` (elke 5 min, optioneel)
Vereist een apart widget-token.

| Sensor | Eenheid |
|--------|---------|
| Widget totaal kWh | kWh |
| Widget totale ERE | credits |
| Verdiensten laag tarief | EUR |
| Verdiensten midden tarief | EUR |
| Verdiensten hoog tarief | EUR |
| CO₂ bespaard | kg |
| Effectieve vergoeding | % |
| ERE prijs midden | EUR/credit |

## Installatie via HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=onsmam&repository=ha-joulo&category=integration)

Of handmatig:
1. HACS → Integraties → ⋮ → Aangepaste repositories
2. URL: `https://github.com/onsmam/ha-joulo` → categorie: **Integration**
3. Zoek op **Joulo** → Downloaden
4. Home Assistant herstarten

## Configuratie

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=joulo)

Of handmatig:
1. Instellingen → Apparaten & diensten → Integratie toevoegen → **Joulo**
2. Voer je API-token in (Joulo dashboard → Settings → API)
3. Optioneel: widget-token voor extra verdienstensensoren

## Tokens

- **API-token**: `https://joulo.nl/dashboard` → Settings → API → Bearer token
- **Widget-token**: URL-parameter `?token=...` van je widget-badge URL
