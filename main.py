import requests
import psycopg2
import folium


loc = {
    "Gießen": {"lat": 50.5841, "lon": 8.6784},
    "Neuberg": {"lat": 50.1980, "lon": 8.9890},
    "Frankfurt": {"lat": 50.1109, "lon": 8.6821}
}

Datenpunkte = []

print("Rufe gerade Wetterdaten ab, einen Augenblick bitte...")

for name, cords in loc.items():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={cords['lat']}&longitude={cords['lon']}&current_weather=true"
    rsp = requests.get(url).json()


    windspeed = rsp['current_weather']['windspeed']
    temperature = rsp['current_weather']['temperature']

    Datenpunkte.append((name, cords['lat'], cords['lon'], windspeed, temperature))

print("Speichere in PostGIS...")

conm = psycopg2.connect(
    dbname='geodata',
    user='agrario',
    password='supersecretpassword',
    host='localhost',
    port='5432'
)

cur = conm.cursor()


cur.execute("DROP TABLE IF EXISTS winddaten; ")


cur.execute("""
    CREATE TABLE winddaten (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),    
        windspeed FLOAT,
        temperature FLOAT,
        geom GEOMETRY(Point, 4326)
    );
""")


cur.execute("TRUNCATE TABLE winddaten;")

for name, lat, lon, speed, temperature in Datenpunkte:

    cur.execute("""
        INSERT INTO winddaten (name, windspeed, temperature, geom)
        VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326));
    """, (name, speed, temperature, lon, lat))

conm.commit()

print("Erstelle die Karte....")


cur.execute("SELECT name, windspeed, temperature,  ST_Y(geom), ST_X(geom) FROM winddaten;")
rows = cur.fetchall()

m = folium.Map(location=[50.3, 8.8], zoom_start=9, tiles='cartodbpositron')

for row in rows:
    name, speed, temperature, lat, lon = row


    folium.Marker(
        [lat, lon],
        popup=f"<b>{name}</b><br>Windgeschwindigkeit: {speed} km/h </b><br> Temperatur: {temperature} °C ",
        icon=folium.Icon(color='green', icon='leaf')
    ).add_to(m)

m.save("map.html")
print("Fertig, öffne die Datei im Browser.")

cur.close()
conm.close()