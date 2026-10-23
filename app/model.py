# Este archivo gestiona las llamadas a la API de OMDb y utiliza la clase de conexión 
# para interactuar con SQLite mediante el imdb_id.

import requests as consulta
from datetime import datetime
from app.conexion import DatabaseConnection

class MovieModel:
    def __init__(self):
        self.api_key = "749ee767"    #con la biblioteca 'python-dotenv' puedo ocultar la API KEY. Lo dejo en pendings para la próxima rama de la API. 
        self.base_url = "http://www.omdbapi.com"
        self.db = DatabaseConnection()


    def buscar_usuario(self, username: str):
        """
        Para poder comentar una película y calificarla es necesario entrar con usuario y contraseña, 
        de no tenerlos, hay que registrarse primero y luego autenticarse.
        No es necesario estar autenticado para buscar las películas y ver comentarios de otros usuarios.   
        Esta función busca el usuario por su 'username' único.
        
        """
        return self.buscar_usuario_por_username(username)

    
    def verificar_password(self, nombre_usuario: str, password: str) -> bool:
        """
        Función que verifica si la contraseña introducida coincide con la del usuario registrado en la BBDD,
        en el caso que exista el usuario (previa comprobación).
        """
        usuario_db = self.buscar_usuario_por_username(nombre_usuario)
        if usuario_db and usuario_db["password"] == password:
            return True
        return False

    
    def registrar_usuario(self, username: str, nombre_a_mostrar: str, password: str):
        """
        Registra un nuevo usuario en la base de datos asegurando un username único y un nombre visible.
        Para acceder al buscador de películas es necesario entrar con usuario y contraseña, 
        de no tenerlos, hay que registrarse y así poder comentar las películas. 
        """
        try:
            query = """
                INSERT INTO usuario (username, nombre_a_mostrar, password)
                VALUES (?, ?, ?)
            """
            # Normalizamos el username a minúsculas y sin espacios para evitar colisiones
            self.db.execute_query(query, (username.strip().lower(), nombre_a_mostrar.strip(), password))
            return True
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False


    def buscar_usuario_por_username(self, username: str):
        """
        Busca al usuario estrictamente por su username de login.
        """
        try:
            query = "SELECT id, username, nombre_a_mostrar, password FROM usuario WHERE username = ?"
            return self.db.fetch_one(query, (username.strip().lower(),))
        except Exception as e:
            print(f"Error al buscar usuario: {e}")
            return None
    
    
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


    def guardar_comentario(self, id_pelicula: str, id_usuario: str, texto_comentario: str):
        """
        Guarda un comentario asociado al imdb_id de la película.
        """
        try:
            #Capturo la fecha actual del sistema
            #fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fecha_actual = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")

            query = """
                INSERT INTO comentario (id_pelicula, id_usuario, comentario, fecha)
                VALUES (?, ?, ?, ?)
            """
        
            # Uso fetch_query o execute_query según la clase de conexión
            self.db.execute_query(query, (id_pelicula, id_usuario, texto_comentario, fecha_actual))
            return True
        except Exception as e:
            print(f"Error al guardar el comentario: {e}")
            return False
    


    def obtener_comentarios(self, id_pelicula: str):
        """
        Obtiene los comentarios de una película haciendo un JOIN con la tabla usuario 
        para devolver el nombre del usuario junto al texto del comentario y su fecha.
        """
        try:
            query = """
                SELECT 
                    c.id,             -- ID único del comentario de la tabla 'comentario'(c)
                    c.id_pelicula,    -- ID de la película en OMDb API (c)
                    c.comentario,     -- El texto escrito por el usuario en la tabla 'comentario'(c)
                    c.fecha,          -- Fecha y hora en que se creó el comentario, se usa 'datetime' en la tabla 'comentario' (c)
                    u.nombre_a_mostrar as persona, -- Nombre del usuario en la tabla 'usuario' (u), renombrado como 'persona' para el Front-end
                    u.id as id_table_usuario   -- ID único del usuario (u), guardado como 'id_table_usuario'
                FROM comentario c       -- Declaro la tabla 'comentario' y le asignamos el alias 'c'
                JOIN usuario u ON c.id_usuario = u.id  -- Vincula ambas tablas donde el 'id_usuario' del comentario coincida con el 'id' del usuario
                WHERE c.id_pelicula = ?                -- Filtra solo los comentarios de esta película específica
                ORDER BY c.id DESC;                    -- Los ordena del más reciente al más antiguo
            """   
            
            return self.db.fetch_query(query, (id_pelicula,))
        except Exception as e:
            print(f"Error al obtener comentarios: {e}")
            return []


    
    def guardar_o_actualizar_calificacion(self, id_pelicula: str, username: str, puntuacion: int):
        """
        Inserta una calificación de 1 a 5 para una película y un usuario.
        Si el usuario ya había calificado esa película, actualiza la puntuación y la fecha.
        """
        from datetime import datetime
        # Obtenemos la fecha actual con la zona horaria o formato que ya se usa en la app
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        # ON CONFLICT ... DO UPDATE provecho la restricción UNIQUE creada en la tabla de base de datos 'calificacion'. 
        # Si el usuario vuelve a votar la misma película, en lugar de duplicar registros, actualiza su nota anterior.
        query = """
        INSERT INTO calificacion (id_pelicula, username, puntuacion, fecha)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id_pelicula, username) 
        DO UPDATE SET puntuacion = excluded.puntuacion, fecha = excluded.fecha;
        """
        try:
            # Asumiendo que usas tu método de escritura unificado (execute_query)
            return self.db.execute_query(query, (id_pelicula, username, puntuacion, fecha_actual))
        except Exception as e:
            print(f"Error al guardar calificación: {e}")
            return False

    
    
    def obtener_promedio_calificacion(self, id_pelicula: str):
        """
        Calcula el promedio de las puntuaciones de una película y cuenta el total de votos.
        Devuelve el promedio redondeado y el total de valoraciones.
        """

        # El método obtener_promedio_calificacion consulta de forma rápida el promedio matemático de las estrellas 
        # y el número total de personas que han valorado esa película en concreto.
        query = """
        SELECT AVG(puntuacion) as promedio, COUNT(*) as total_votos 
        FROM calificacion 
        WHERE id_pelicula = ?;
        """
        try:
            resultados = self.db.fetch_query(query, (id_pelicula,))
            if resultados and resultados[0]["promedio"] is not None:
                promedio = round(resultados[0]["promedio"], 1) # Redondeado a un decimal (ej. 4.2)
                total_votos = resultados[0]["total_votos"]
                return {"promedio": promedio, "total_votos": total_votos}
            return {"promedio": 0.0, "total_votos": 0}
        except Exception as e:
            print(f"Error al calcular el promedio de calificación: {e}")
            return {"promedio": 0.0, "total_votos": 0}