# postgis-weather
Proof of Concept: Abruf von API-Wetterdaten, Speicherung in PostGIS-Datenbank und Web-Visualisierung.




## Was das Skript macht:
1. Es zieht sich aktuelle Wetterdaten über die kostenlose Open-Meteo API.
2. Es speichert diese Daten in einer lokalen PostgreSQL-Datenbank (mit PostGIS-Erweiterung), die ich über Podman laufen lasse.
3. Es generiert aus den Datenbank-Einträgen automatisch eine einfache HTML-Karte (`map.html`), um die Daten zu visualisieren.

**1. Datenbank-Container starten (Podman/Docker):**
Starten der PostGIS-Instanz für die Speicherung der Geometrien.
```bash
podman run --name postgis-db -e POSTGRES_PASSWORD=deinpasswort -p 5432:5432 -d postgis/postgis
