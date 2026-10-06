import requests as consulta

class MovieModel:
    def __init__(self):
        self.api_key = "749ee767"
        self.base_url = "http://www.omdbapi.com"

    def search_movies_by_name(self, nombre: str):
        """
        Busca películas por título o nombre de película sin importar el año.
        Uso el parámetro "s" sugerido por los requisitos de OMBd API para las búsquedas
        """
        try:
            respuesta = consulta.get(
                f"{self.base_url}?s={nombre.lower()}&apikey={self.api_key}"
            )
            if respuesta.status_code == 200:
                return respuesta.json()
            return {}
        except Exception:
            return {}

    #def search_movies_by_year(self, palabra_clave: str, year_string: str):
    #    """
    #    Busca películas filtrando obligatoriamente por un año específico.
    #    Para ello es necesario sumar a la búsqueda otro valor: buscar por una palabra clave. Ya que OMBd API 
    #    no permite buscar solo por año. 
    #    Uso el parámetro "s" sugerido por los requisitos de OMBd API para las búsquedas.
    #    """
    #    try:
    #        termino = palabra_clave.lower() if palabra_clave else "movie"
    #        respuesta = consulta.get(
    #            f"{self.base_url}?s={termino}&y={year_string}&apikey={self.api_key}"
    #        )
    #        if respuesta.status_code == 200:
    #            return respuesta.json()
    #        return {}
    #    except Exception:
    #        return {}

    # 
    def search_movies_by_name_and_year(self, nombre: str, year_string: str):
        """
        Busca películas combinando un título y un año específicos.
        Uso el parámetro "s" sugerido por los requisitos de OMBd API para las búsquedas.
        """
        try:
            respuesta = consulta.get(
                f"{self.base_url}?s={nombre.lower()}&y={year_string}&apikey={self.api_key}"
            )
            if respuesta.status_code == 200:
                return respuesta.json()
            return {}
        except Exception:
            return {}

    def fetch_movie_detail(self, imdb_id: str):
        """
        Obtiene la información detallada de una película mediante su ID único (IMDb ID)
        """
        try:
            respuesta = consulta.get(
                f"{self.base_url}?i={imdb_id}&apikey={self.api_key}"
            )
            if respuesta.status_code == 200:
                return respuesta.json()
            return None
        except Exception:
            return None
