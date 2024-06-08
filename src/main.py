from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from math import radians, cos, sin, sqrt, atan2

app = FastAPI()

# Models -------------------------------------------------------------------
# ==========================================================================


class Coordinates(BaseModel):
    """
    Modelo de datos para representar coordenadas geográficas.

    Attributes:
        latitude (float): La latitud de las coordenadas.
        longitude (float): La longitud de las coordenadas.
    """

    latitude: float
    longitude: float


# Endpoints ----------------------------------------------------------------
# ==========================================================================


@app.get("/get_coordinates")
def get_coordinates(city: str):
    """
    Obtiene las coordenadas geográficas de una ciudad usando el servicio de OpenStreetMap.

    Args:
        city (str): Nombre de la ciudad para buscar sus coordenadas.

    Returns:
        dict: Un diccionario con las claves 'latitude' y 'longitude'.

    Raises:
        HTTPException: Si la ciudad no se encuentra o hay un error en la API.
    """
    response = requests.get(
        f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
    )

    if response.status_code != 200 or not response.json():
        raise HTTPException(status_code=404, detail="City not found or API error")

    data = response.json()[0]
    return {"latitude": float(data["lat"]), "longitude": float(data["lon"])}


@app.post("/get_distance")
def get_distance(coords1: Coordinates, coords2: Coordinates):
    """
    Calcula la distancia en kilómetros entre dos coordenadas geográficas utilizando la fórmula de Haversine.

    Args:
        coords1 (Coordinates): Primeras coordenadas (latitud y longitud).
        coords2 (Coordinates): Segundas coordenadas (latitud y longitud).

    Returns:
        dict: Un diccionario con la clave 'distance' que representa la distancia en kilómetros.
    """
    lat1, lon1 = coords1.latitude, coords1.longitude
    lat2, lon2 = coords2.latitude, coords2.longitude

    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    return {"distance": distance}


# Functions ----------------------------------------------------------------
# ==========================================================================


def calculate_haversine_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Calcula la distancia en kilómetros entre dos puntos geográficos en la superficie de la Tierra
    utilizando la fórmula de Haversine.

    Args:
        lat1 (float): Latitud del primer punto.
        lon1 (float): Longitud del primer punto.
        lat2 (float): Latitud del segundo punto.
        lon2 (float): Longitud del segundo punto.

    Returns:
        float: Distancia en kilómetros entre los dos puntos dados.
    """
    R = 6371.0  # Radio de la Tierra en kilómetros

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
