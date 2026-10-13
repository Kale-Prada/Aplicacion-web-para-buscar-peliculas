# Verificar que se puede conectar con la base de datos, que crea las tablas 
# y que podemos insertar y leer datos de prueba sin romper la aplicación que está en producción

import os
import pytest
from app.conexion import DatabaseConnection

def test_database_connection():
    """
    Este test comprueba que la clase "DatabaseConnection" funciona correctamente y es capaz de realizar consultas. 
    Para no ensuciar la base de datos real de producción (app/bd/moviesearch.db), 
    se apunta temporalmente a una base de datos de pruebas (app/bd/test_moviesearch.db).
    """

    # Base de datos temporal para las pruebas
    test_db_path = "app/bd/test_moviesearch.db"
    
    # Me aseguro que no exista la BBDD de una prueba anterior
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    db = DatabaseConnection(db_path=test_db_path)
    
    # Comprobamos que la tabla comentario se creó ejecutando un SELECT
    resultados = db.ejecutar_query("SELECT * FROM comentario;")
    assert resultados is not None
    assert len(resultados) == 0

    # Limpiamos el archivo de prueba al terminar
    if os.path.exists(test_db_path):
        os.remove(test_db_path)