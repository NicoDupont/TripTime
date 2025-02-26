from dataclasses import dataclass
import json
import asyncio
from typing import List
import googlemaps
import aiohttp

@dataclass
class Route:
    name: str
    origin: str  # adresse origine
    destination: str # adresse destination
    entity_id: str  # entity_id dans Home Assistant

@dataclass
class Config:
    google_maps_api_key: str
    home_assistant_url: str
    home_assistant_token: str

def load_config() -> Config:
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
        return Config(**config_data)

def load_routes() -> List[Route]:
    with open('travels.json', 'r') as f:
        routes_data = json.load(f)
        return [Route(**route) for route in routes_data]

def get_traval_time(gmaps: googlemaps.Client, origin: str, destination: str) -> int:
    try:
        result = gmaps.directions(origin, destination, mode="driving", departure_time="now")
        if result and len(result) > 0:
            res = result[0]['legs'][0]
            duration = res.get('duration_in_traffic', res['duration'])
            return duration['value'] // 60  # Convertir les secondes en minutes
        return 0
    except Exception as e:
        print(f"Erreur lors de la récupération du temps de trajet : {e}")
        return 0

async def post_ha(session: aiohttp.ClientSession, url: str, headers: dict, entity_id: str, travel_time: int):
    try:#payload pour api ha
        payload = {
            "state": travel_time,
            "attributes": {
                "unit_of_measurement": "minutes"
            }
        }
        async with session.post(f"{url}/api/states/sensor.{entity_id}", headers=headers, json=payload) as response:
            if response.status in (200,201):
                pass
                #print(f"Mis à jour de {entity_id} avec succès.")
            else:
                print(f"Échec de la mise à jour de {entity_id}. Statut: {response.status}")
    except Exception as e:
        print(f"Erreur lors de l'envoi des données à Home Assistant : {e}")

async def travel_times(gmaps: googlemaps.Client, session: aiohttp.ClientSession, config: Config, routes: List[Route]):
    headers = {
        "Authorization": f"Bearer {config.home_assistant_token}",
        "Content-Type": "application/json"
    }
    tasks = []
    for route in routes:
        travel_time = get_traval_time(gmaps, route.origin, route.destination)
        if travel_time >= 0:
            task = post_ha(session, config.home_assistant_url, headers, route.entity_id, travel_time)
            tasks.append(task)
            #print(f"Préparation de l'envoi pour {route.name}: {travel_time} minutes")
    # si google maps retourne des données
    if tasks:
        await asyncio.gather(*tasks)

async def main():
    config = load_config()
    routes = load_routes()
    gmaps = googlemaps.Client(key=config.google_maps_api_key)
    async with aiohttp.ClientSession() as session:
        await travel_times(gmaps, session, config, routes)

# lancer la fonction principale
if __name__ == "__main__":
    asyncio.run(main())
