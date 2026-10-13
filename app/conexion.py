import sqlite3
#Librería para gestionar carpetas y rutas en el S.O donde se esté interactuando
import os

class DatabaseConnection:
    def __init__(self, db_path="app/bd/moviesearch.db"):
        # Con "os.makedirs" me aseguro que el directorio 'app/bd' exista en el equipo. 
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        #Crea tabla "comentario" si no existe en la BBDD
        self._init_database()

    def ejecutar_query(self, sql_query, parametro=None):
        """
        Ejecuta una consulta SQL (SELECT, INSERT, UPDATE, DELETE).
        Retorna los resultados si es un SELECT, o hace commit si es una modificación.
        """
        if parametro is None:
            parametro = []
            
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row  # Para poder acceder a las columnas por nombre
        cur = con.cursor()
        
        try:
            cur.execute(sql_query, parametro)
            
            # Si es una consulta de lectura (SELECT)
            if sql_query.strip().upper().startswith("SELECT"):
                resultados = cur.fetchall()
                con.close()
                return resultados
            
            # Si es una modificación (INSERT, UPDATE, DELETE)
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(f"Error en la consulta SQL: {e}")
            con.close()
            return None

    def _init_database(self):
        """
        Crea la tabla 'comentario' si no existe en la base de datos.
        #En mi ejercicio yo tengo creada la base de datos y la tabla "comentario" con SQlite. 
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
        self.ejecutar_query(query_tabla_comentario)


    # Bloque de prueba local
#if __name__ == "__main__":
#    db = DatabaseConnection()
#    resultados = db.ejecutar_query('SELECT * FROM comentario;')
    
#    print("\nResultados de la tabla comentario:")
#    if not resultados:
#        print("La tabla está vacía.")
 #   else:
#        for row in resultados:
            # Convertimos cada fila Row a un diccionario estándar de Python para ver sus valores
#            print(dict(row))
            
            # O si prefieres mostrarlo de forma más personalizada:
             #print(f"ID: {row['id']} | Película: {row['id_pelicula']} | Persona: {row['persona']} | Comentario: {row['comentario']} | Fecha: {row['fecha']}")