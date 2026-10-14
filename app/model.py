# Este archivo gestiona las llamadas a la API de OMDb y utiliza la clase de conexión 
# para interactuar con SQLite mediante el imdb_id.

import requests as consulta
from datetime import datetime
from app.conexion import DatabaseConnection

class MovieModel:
    def __init__(self):
        self.api_key = "749ee767"
        self.base_url = "http://www.omdbapi.com"
        self.db = DatabaseConnection()

    
    def autenticar_o_registrar_usuario(self, nombre_usuario: str, password: str):
        """
        Busca al usuario. Si existe, verifica su contraseña. 
        Si no existe, lo registra automáticamente con esa contraseña.
        Retorna True si la autenticación/registro es exitosa, False si la contraseña es incorrecta.
        """
        nombre_limpio = nombre_usuario.strip().capitalize()
        if not nombre_limpio or not password:
            return False

        # 1. Comprobar si el usuario ya existe
        query_select = "SELECT * FROM usuario WHERE nombre = ?"
        resultado = self.db.ejecutar_query(query_select, (nombre_limpio,))

        if resultado:
            # El usuario existe, verificamos la contraseña
            usuario_db = dict(resultado[0])
            if usuario_db["password"] == password:
                return True # Login exitoso
            else:
                return False # Contraseña incorrecta
        else:
            # El usuario no existe, lo registramos como nuevo
            query_insert = "INSERT INTO usuario (nombre, password) VALUES (?, ?)"
            exito = self.db.ejecutar_query(query_insert, (nombre_limpio, password))
            return exito is not None
    
    
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


    def guardar_comentario(self, id_pelicula: str, persona: str, texto_comentario: str):
        """
        Guarda un comentario asociado al imdb_id de la película.
        """
        #Capturo la fecha actual del sistema
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = """
            INSERT INTO comentario (id_pelicula, persona, comentario, fecha)
            VALUES (?, ?, ?, ?)
        """
        resultado = self.db.ejecutar_query(query, (id_pelicula, persona, texto_comentario, fecha_actual))
        return resultado is not None

    def obtener_comentarios(self, id_pelicula: str):
        """
        Recupera los comentarios de todos los usuarios que hayan dejado comentario, 
        asociados a una película por su imdb_id. Muestra fecha, nombre de la persona 
        y el o los comentarios. 
        """
        
        #Se ordena en forma DESC - Descendente. Del más nuevo al más antiguo. 
        query = """
            SELECT persona, comentario, fecha 
            FROM comentario 
            WHERE id_pelicula = ? 
            ORDER BY id DESC
        """

        
        resultados = self.db.ejecutar_query(query, (id_pelicula,))
        return resultados if resultados is not None else []
