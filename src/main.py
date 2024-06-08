# src/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from math import radians, cos, sin, sqrt, atan2

app = FastAPI()

# Models -------------------------------------------------------------------
# ==========================================================================

# Modelo de datos para las coordenadas
# --------------------------------------------------------------------------
class Coordinates(BaseModel):
    latitude: float
    longitude: float





# Endpoints ----------------------------------------------------------------
# ==========================================================================


# GET /get_coordinates -> Devuelve las coordenadas de una ciudad (latitud y
# longitud)
#
# -> city: str
#
# <- {"latitude": float, "longitude": float}
# --------------------------------------------------------------------------
@app.get("/get_coordinates")
def get_coordinates(city: str):
    response = requests.get(f"https://nominatim.openstreetmap.org/search?q={city}&format=json")
    if response.status_code != 200 or not response.json():
        raise HTTPException(status_code=404, detail="City not found or API error")
    
    data = response.json()[0]
    return {"latitude": float(data["lat"]), "longitude": float(data["lon"])}


# POST /get_distance -> Devuelve la distancia en kilómetros entre dos coor-
# denadas
#
# -> coords1: {"latitude": float, "longitude": float}
# -> coords2: {"latitude": float, "longitude": float}
#
# <- {"distance": float}
# --------------------------------------------------------------------------
@app.post("/get_distance")
def get_distance(coords1: Coordinates, coords2: Coordinates):
    lat1, lon1 = coords1.latitude, coords1.longitude
    lat2, lon2 = coords2.latitude, coords2.longitude

    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    return {"distance": distance}



# Functions ----------------------------------------------------------------
# ==========================================================================

# Calcula la distancia en kilómetros entre dos puntos geográficos
#
# -> lat1: float, lat2: float, lon1: float, lon2: float
#
# <- float
# --------------------------------------------------------------------------
def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radio de la Tierra en kilómetros

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
