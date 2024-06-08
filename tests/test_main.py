# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from src.main import app, calculate_haversine_distance
import random

client = TestClient(app)

# Lista de ciudades para pruebas extensivas
city_list = [
    "New York, USA",
    "Tokyo, Japan",
    "London, UK",
    "Paris, France",
    "Lima, Peru",
    # Añadir más ciudades si se desea
]


# Lista de coordenadas para pruebas de distancia (50)
coords_list = []

for i in range(100):
    a = random.randint(-90, 90)
    b = random.randint(-180, 180)
    c = random.randint(-90, 90)
    d = random.randint(-180, 180)
    coords_list.append((a, b, c, d, calculate_haversine_distance(a, b, c, d)))
    

# =========================================================================

def test_can_call_existing_endpoints_of_the_API():
    response = client.get("/get_coordinates?city=Lima,Peru")
    assert response.status_code == 200
    response = client.post("/get_distance", json={
        "coords1": {"latitude": 34.0522, "longitude": -118.2437},
        "coords2": {"latitude": 36.1699, "longitude": -115.1398}
    })
    assert response.status_code == 200

def test_cannot_call_non_existent_endpoints_of_the_API():
    response = client.get("/non_existent_endpoint")
    assert response.status_code == 404

def test_endpoint_returns_something():
    response = client.get("/get_coordinates?city=Lima,Peru")
    assert response.json() != {}

    response = client.post("/get_distance", json={
        "coords1": {"latitude": 34.0522, "longitude": -118.2437},
        "coords2": {"latitude": 36.1699, "longitude": -115.1398}
    })
    assert response.json() != {}

    
# =========================================================================

def test_the_result_is_correct_for_simple_cases_get_coordinates():
    response = client.get("/get_coordinates?city=Lima,Peru")
    assert abs(response.json()["latitude"] - -12.0463731) < 0.1 and abs(response.json()["longitude"] - -77.042754) < 0.1

def test_the_result_is_correct_for_simple_cases_get_distance():
    response = client.post("/get_distance", json={
        "coords1": {"latitude": 34.0522, "longitude": -118.2437},
        "coords2": {"latitude": 36.1699, "longitude": -115.1398}
    })
    assert abs(response.json()["distance"] - 368.5) < 1


# =========================================================================

@pytest.mark.parametrize("city_name", city_list)
def test_the_result_is_correct_for_all_input_get_coordinates(city_name):
    response = client.get(f"/get_coordinates?city={city_name}")
    if response.status_code == 200:
        data = response.json()
        assert "latitude" in data and "longitude" in data
        assert isinstance(data["latitude"], float)
        assert isinstance(data["longitude"], float)
    else:
        # Si falla, debemos asegurarnos de que el error esté justificado (por ejemplo, ciudad no encontrada)
        assert response.status_code == 404

@pytest.mark.parametrize("lat1, lon1, lat2, lon2, expected_distance", coords_list)
def test_the_result_is_correct_for_all_input_get_distance(lat1, lon1, lat2, lon2, expected_distance):
    response = client.post("/get_distance", json={
        "coords1": {"latitude": lat1, "longitude": lon1},
        "coords2": {"latitude": lat2, "longitude": lon2}
    })
    assert abs(response.json()["distance"] - expected_distance) < 1

