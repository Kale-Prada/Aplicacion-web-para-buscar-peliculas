# Test para comprobar que el modelo puede guardar un comentario en la base de datos de prueba 
# y recuperarla correctamente utilizando un identificador de película que no es real. 

import os
import pytest
from app.model import MovieModel
from app.conexion import DatabaseConnection

def test_guardar_y_obtener_comentarios():
    # Configuro el modelo para que use una base de datos de test
    test_db_path = "app/bd/test_moviesearch.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    model = MovieModel()
    # Fuerzo durante la ejecución del test la ruta de la base de datos del modelo a la de test
    model.db = DatabaseConnection(db_path=test_db_path)

    # Datos para la prueba
    test_imdb_id = "pp0134561" # Ejemplo: Cadena perpetua / The Shawshank Redemption
    test_persona = "Usuario"
    test_comentario = "Una película interesante, ¡la recomiendo!"

    # 1. Pruebo guardar el comentario
    exito = model.guardar_comentario(test_imdb_id, test_persona, test_comentario)
    assert exito == True

    # 2. Pruebo recuperar los comentarios
    comentarios = model.obtener_comentarios(test_imdb_id)
    assert len(comentarios) == 1
    assert comentarios[0]["persona"] == test_persona
    assert comentarios[0]["comentario"] == test_comentario

    # Elimino la base de datos de prueba y sus registros. 
    if os.path.exists(test_db_path):
        os.remove(test_db_path)