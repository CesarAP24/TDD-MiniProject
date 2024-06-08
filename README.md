# Diseño de la API de Coordenadas y Distancia

## Descripción General

Esta API permite a los clientes obtener coordenadas (latitud y longitud) de una ciudad y calcular la distancia entre dos puntos geográficos dados. Utiliza FastAPI para la creación de endpoints y consulta la API de OpenStreetMap para obtener las coordenadas.

## Endpoints

### 1. Obtener Coordenadas (`/get_coordinates`)

- **Método HTTP:** `GET`
- **Descripción:** Devuelve las coordenadas (latitud y longitud) de una ciudad especificada.
- **Parámetros de Entrada:**
  - `city` (str): El nombre de la ciudad en formato "ciudad,país", por ejemplo, "Lima,Peru".
- **Ejemplo de Solicitud:**
  ```
  GET /get_coordinates?city=Lima,Peru
  ```
- **Respuesta Exitosa (200):**
  ```json
  {
    "latitude": -12.046374,
    "longitude": -77.0427934
  }
  ```
- **Respuestas de Error:**
  - `404 Not Found`: Si la ciudad no se encuentra.
  - `400 Bad Request`: Si el parámetro de la ciudad está malformado.

### 2. Calcular Distancia (`/get_distance`)

- **Método HTTP:** `POST`
- **Descripción:** Calcula la distancia en kilómetros entre dos puntos dados sus coordenadas.
- **Parámetros de Entrada (en formato JSON):**
  ```json
  {
    "coords1": {
      "latitude": 34.0522,
      "longitude": -118.2437
    },
    "coords2": {
      "latitude": 36.1699,
      "longitude": -115.1398
    }
  }
  ```
- **Ejemplo de Solicitud:**
  ```
  POST /get_distance
  Content-Type: application/json
  {
    "coords1": {"latitude": 34.0522, "longitude": -118.2437},
    "coords2": {"latitude": 36.1699, "longitude": -115.1398}
  }
  ```
- **Respuesta Exitosa (200):**
  ```json
  {
    "distance": 368.5
  }
  ```
- **Respuestas de Error:**
  - `400 Bad Request`: Si los datos de las coordenadas están malformados o faltan.

## Detalles de Implementación

### Función `get_coordinates`

- **Descripción:** Obtiene las coordenadas de una ciudad utilizando la API de OpenStreetMap.
- **Ruta:** `/get_coordinates`
- **Parámetros:**
  - `city` (str): El nombre de la ciudad.
- **Retorno:** Un diccionario con `latitude` y `longitude`.

### Función `get_distance`

- **Descripción:** Calcula la distancia entre dos conjuntos de coordenadas usando la fórmula de Haversine.
- **Ruta:** `/get_distance`
- **Parámetros:**
  - `coords1` (dict): Diccionario con `latitude` y `longitude` para el primer punto.
  - `coords2` (dict): Diccionario con `latitude` y `longitude` para el segundo punto.
- **Retorno:** Un diccionario con la `distance` en kilómetros.

### Función Interna `calculate_haversine_distance`

- **Descripción:** Calcula la distancia en kilómetros entre dos puntos geográficos usando la fórmula de Haversine.
- **Parámetros:**
  - `lat1` (float): Latitud del primer punto.
  - `lon1` (float): Longitud del primer punto.
  - `lat2` (float): Latitud del segundo punto.
  - `lon2` (float): Longitud del segundo punto.
- **Retorno:** Distancia en kilómetros.
