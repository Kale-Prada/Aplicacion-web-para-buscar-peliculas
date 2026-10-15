import sqlite3
#Librería para gestionar carpetas y rutas en el S.O donde se esté interactuando
import os

class DatabaseConnection:
    def __init__(self, db_path="app/bd/moviesearch.db"):
        # Con "os.makedirs" me aseguro que el directorio 'app/bd' exista en el equipo. 
        #Si no existe Python lo crea para evitar errores. 
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        #Crea tabla "comentario" y "usuario" si no existen en la BBDD 'app/bd/moviesearch.db'
        self._init_database()


    def _get_connection(self):
        """
        En lugar de escribir el código para conectar con SQLite en cada función,
        lo agrupo aquí para reutilizarlo tantas veces como se necesiten. 
        """
        conexion = sqlite3.connect(self.db_path)
        
        # 'row_factory' nos permite tratar los resultados de la base de datos como diccionarios
        # (pudiendo buscar las columnas por su nombre, por ejemplo: fila['nombre']).
        conexion.row_factory = sqlite3.Row  
        return conexion


    def fetch_query(self, sql_query, parametro=None):
        """
        Función exclusiva para leer o consultar datos (SELECT). 
        Ejemplo: mostrar los comentarios de una película.
        """
        if parametro is None:
            parametro = []
            
        # Abro la conexión usando la función 'get_connection'
        con = self._get_connection()
        cur = con.cursor()
        
        try:
            # Ejecuto la consulta SQL de lectura
            cur.execute(sql_query, parametro)
            
            # .fetchall() recoge TODOS los registros que coincidan con la búsqueda
            resultados = cur.fetchall()
            return resultados

        #Control de errores    
        except Exception as e:
            print(f"Hubo un error al leer los datos de la base de datos: {e}")
            return []
            
        finally:
            # Pase lo que pase (haya error o todo vaya bien), 
            # la conexión a la base de datos se cierra siempre de forma segura.
            con.close()


    def execute_query(self, sql_query, parametro=None):
        """
        Función exclusiva para modificar datos (INSERT, UPDATE, DELETE).
        Ejemplo: Registrar un nuevo usuario o guardar un comentario nuevo.
        """
        if parametro is None:
            parametro = []
            
        # Abrimos la conexión
        con = self._get_connection()
        cur = con.cursor()
        
        try:
            # Ejecutamos la acción de escritura
            cur.execute(sql_query, parametro)
            
            # .commit() es OBLIGATORIO en SQLite cuando modificas datos. 
            # Le dice a la base de datos: "Guarda los cambios de forma permanente".
            con.commit()
            return True
            
        except Exception as e:
            print(f"Hubo un error al modificar los datos: {e}")
            con.rollback() # Si algo falla a mitad, deshace los cambios para no dejar datos corruptos.
            return None
            
        finally:
            # Pase lo que pase (haya error o todo vaya bien), 
            # la conexión a la base de datos se cierra siempre de forma segura.
            con.close()


    def _init_database(self):
        """
        Crea las tablas 'comentario' y 'usuario' en la BBDD 'app/bd/moviesearch.db' al iniciar la App, si no existe en la base de datos.
        En mi ejercicio yo tengo creada la base de datos y las tablas 'comentario' y 'usuario' con SQlite. 
        Como es una acción de guardar/crear, utilizo la función 'execute_query'.
        """
        query_tabla_comentario = """
            CREATE TABLE IF NOT EXISTS comentario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pelicula TEXT NOT NULL,
                persona TEXT NOT NULL,
                comentario TEXT,
                fecha TEXT NOT NULL
            )
        """
        self.execute_query(query_tabla_comentario)

        #Creo la tabla 'usuario' para la autenticación e ingreso a la búsqueda de películas y poder dejar comentarios. 
        #Ya no les volverá a pedir el usuario o nombre cuando vayana introducir un comentario. 

        query_tabla_usuario = """
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """
        self.execute_query(query_tabla_usuario)

