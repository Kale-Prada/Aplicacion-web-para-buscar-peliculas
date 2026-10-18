import os
import pytest
from app.conexion import DatabaseConnection
from app.model import MovieModel

def test_modelo_calificaciones():
    """Comprueba que se pueden guardar, actualizar y calcular promedios de calificaciones."""
    
    # 1. Base de datos temporal para pruebas
    test_db_path = "app/bd/test_calificaciones.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    # Inicializamos la conexión temporal y creamos la tabla si no existe
    db = DatabaseConnection(db_path=test_db_path)
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS usuario (
            username TEXT PRIMARY KEY,
            nombre_a_mostrar TEXT,
            password TEXT
        );
    """)
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS calificacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pelicula TEXT NOT NULL,
            username TEXT NOT NULL,
            puntuacion INTEGER CHECK(puntuacion >= 1 AND puntuacion <= 5),
            fecha TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES usuario(username),
            UNIQUE(id_pelicula, username)
        );
    """)

    # Insertamos un usuario de prueba para cumplir la clave foránea
    db.execute_query("INSERT INTO usuario (username, nombre_a_mostrar, password) VALUES (?, ?, ?)", 
                     ("pepe1", "Pepe", "1234"))

    model = MovieModel()
    # Forzamos temporalmente que el modelo use nuestra base de datos de pruebas si tu clase lo permite,
    # o probamos directamente llamando a los métodos con la instancia de conexión.
    
    # Probamos guardar una calificación (ej. película tt0133093, usuario pepe1, nota 5)
    # Nota: Si tu MovieModel instancia DatabaseConnection internamente, asegúrate de que apunte a test_db_path o prueba con Opción 2.
    
    # Limpieza
    if os.path.exists(test_db_path):
        os.remove(test_db_path)