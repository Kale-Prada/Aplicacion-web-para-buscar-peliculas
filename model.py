# Se encarga en exclusiva de la lógica de datos y de la comunicación 
# directa con la API de OMDb. No sabe nada de pantallas ni de terminales.

import requests as consulta

class MovieModel:
    def __init__(self):
        self.api_key = "749ee767"
        self.base_url = "http://www.omdbapi.com/"

    def fetch_movie(self, nombre: str, year_string: str):
        """Hace la consulta a la API de OMDb y devuelve el diccionario JSON o None."""
        try:
            respuesta = consulta.get(
                f"{self.base_url}?t={nombre.lower()}&y={year_string}&apikey={self.api_key}"
            )
            if respuesta.status_code == 200:
                return respuesta.json()
            return None
        except Exception:
            return None