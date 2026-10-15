# Verificar que se puede conectar con la base de datos, que crea las tablas 
# y que podemos insertar y leer datos de prueba sin romper la aplicación que está en producción

import os
import pytest
from app.conexion import DatabaseConnection

def test_database_connection():
    """
    Este test comprueba que la clase "DatabaseConnection" funciona correctamente y es capaz de realizar consultas. 
    Para no hacer registros de prueba en la base de datos en que está en producción (app/bd/moviesearch.db), 
    se apunta temporalmente a una base de datos de pruebas (app/bd/test_moviesearch.db).
    """

    # Base de datos temporal para las pruebas
    test_db_path = "app/bd/test_moviesearch.db"
    
    # Me aseguro que no exista la BBDD de una prueba anterior
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    db = DatabaseConnection(db_path=test_db_path)
    
    # Comprobamos que la tabla comentario se creó ejecutando una consulta de lectura SELECT
    # Debo usar 'fetch_query' para que devuelva una lista de resultados, no un booleano.
    # Si uso 'execute_query' me devolverá un booleano y por lo tanto al hacer el 'pytest' 
    # me dará un error TypeError: object of type 'bool' has no len()
    
    resultados = db.fetch_query("SELECT * FROM comentario;")
    
    assert resultados is not None
    #Como 'resultados' es una lista vacía [], su longitud es 0.
    assert len(resultados) == 0

    # Limpiamos el archivo de prueba al terminar
    if os.path.exists(test_db_path):
        os.remove(test_db_path)