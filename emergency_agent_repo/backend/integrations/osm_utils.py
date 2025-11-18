# Simple OSM Nominatim / Overpass helper to find nearby ambulance/police.
import httpx, os, asyncio

NOMINATIM = "https://nominatim.openstreetmap.org/reverse"
OVERPASS = "https://overpass-api.de/api/interpreter"

async def find_nearest_responder(lat, lon, responder_type="ambulance", radius_m=5000):
    # Use Overpass to find amenity=rescue_station or emergency services nearby - simplified example
    # NOTE: Overpass queries may be rate-limited. For production, consider using a cached dataset or paid service.
    query = f"""[out:json][timeout:25];
    (
      node(around:{radius_m},{lat},{lon})[emergency];
      node(around:{radius_m},{lat},{lon})[amenity=police];
      node(around:{radius_m},{lat},{lon})[amenity=hospital];
    );
    out center 1;
    """
    async with httpx.AsyncClient() as c:
        r = await c.post(OVERPASS, data={"data": query}, timeout=30.0)
        if r.status_code != 200:
            return None
        data = r.json()
        if not data.get("elements"):
            return None
        el = data["elements"][0]
        return {"id": el.get("id"), "lat": el.get("lat"), "lon": el.get("lon"), "tags": el.get("tags", {})}
