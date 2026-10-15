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
    test_imdb_id = "pp0134561" # Ejemplo de ID película
    test_username = "usuario_test"
    test_nombre_mostrar = "Usuario"
    test_comentario = "Una película interesante, ¡la recomiendo!"

    # IMPORTANTE: Se crea primero el usuario pasando los 3 argumentos requeridos: 
    # username, nombre_mostrar y password
    model.registrar_usuario(test_username, test_nombre_mostrar, "Password123")

    # Busco al usuario recién creado por su username para obtener su ID real autogenerado
    usuario_db = model.buscar_usuario_por_username(test_username)
    usuario_id = usuario_db["id"] if isinstance(usuario_db, dict) else usuario_db[0]

    # 1. Pruebo guardar el comentario (id_pelicula, id_usuario, comentario)
    exito = model.guardar_comentario(test_imdb_id, usuario_id, test_comentario)
    assert exito == True

    # 2. Pruebo recuperar los comentarios (el JOIN recuperará 'persona' usando el nombre_mostrar)
    comentarios = model.obtener_comentarios(test_imdb_id)
    assert len(comentarios) == 1
    assert comentarios[0]["persona"] == test_nombre_mostrar
    assert comentarios[0]["comentario"] == test_comentario

    # Elimino la base de datos de prueba al terminar. 
    if os.path.exists(test_db_path):
        os.remove(test_db_path)