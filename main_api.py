from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.model import MovieModel

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="API de Búsqueda de Películas y Comentarios",
    description="Backend profesional con FastAPI, SQLite y OMDb API - Incluye control de registro de usuarios - By Kale",
    version="1.0.0"
)

# Hago llamada al modelo 'MovieModel' para reutilizar toda la lógica de programa y base de datos
movie_model = MovieModel()

# ==========================================
# ESQUEMAS DE PYDANTIC (Validación de datos)
# ==========================================
class UsuarioRequest(BaseModel):
    nombre: str
    password: str

class ComentarioRequest(BaseModel):
    persona: str
    comentario: str


# ==========================================
# RUTAS (ENDPOINTS) DE USUARIOS Y AUTENTICACIÓN
# ==========================================
@app.post("/api/usuarios/login-o-registrar")
def login_o_registrar(data: UsuarioRequest):
    """
    Gestiona el flujo seguro de usuario aplicando la misma lógica estricta de la consola:
    - Valida que no estén vacíos.
    - Normaliza el nombre (elimina espacios múltiples y aplica formato título).
    - Si existe, verifica la contraseña con la función dedicada.
    - Si no existe, permite registrarlo de forma controlada.
    """
    # Validación de campos vacíos
    if not data.nombre.strip() or not data.password.strip():
        raise HTTPException(status_code=400, detail="El usuario y la contraseña no pueden estar vacíos.")

    # Normalización estricta (limpieza de espacios y formato título)
    nombre_limpio = " ".join(data.nombre.strip().split()).title()
    
    # Buscamos si el usuario ya existe en la base de datos
    usuario_db = movie_model.buscar_usuario(nombre_limpio)
    
    if usuario_db:
        # El usuario existe: comprobamos la contraseña con la función dedicada
        if movie_model.verificar_password(nombre_limpio, data.password):
            return {
                "status": "success", 
                "mensaje": f"Acceso concedido. Bienvenido de nuevo, {nombre_limpio}", 
                "usuario": nombre_limpio
            }
        else:
            raise HTTPException(status_code=400, detail="Contraseña incorrecta. Inténtalo de nuevo.")
    else:
        # El usuario NO existe: lo registramos automáticamente (equivalente a responder que sí al aviso de creación)
        exito = movie_model.registrar_usuario(nombre_limpio, data.password)
        if exito:
            return {
                "status": "success", 
                "mensaje": f"Usuario '{nombre_limpio}' creado y registrado con éxito.", 
                "usuario": nombre_limpio
            }
        else:
            raise HTTPException(status_code=500, detail="Hubo un error al registrar el usuario en la base de datos.")

# ==========================================
# 3. RUTAS DE BÚSQUEDA DE PELÍCULAS (OMDb API)
# ==========================================
@app.get("/api/peliculas/buscar")
def buscar_por_pelicula(titulo: str):
    """
    Apartado 1: Búsqueda exclusiva por el nombre o título de la película.
    Ejemplo: /api/peliculas/buscar?titulo=matrix
    """
    if not titulo.strip():
        raise HTTPException(status_code=400, detail="El título de la película no puede estar vacío.")

    respuesta = movie_model.search_movies_by_name(titulo)
    
    if not respuesta or respuesta.get("Response") == "False":
        raise HTTPException(status_code=404, detail="No se encontraron películas que coincidan con ese título.")
    return respuesta


@app.get("/api/peliculas/buscar-por-anio")
def buscar_por_pelicula_y_anio(titulo: str, year: str):
    """
    Apartado 2: Búsqueda combinada por título de la película y año específico.
    Ejemplo: /api/peliculas/buscar-por-anio?titulo=matrix&year=1999
    """
    if not titulo.strip() or not year.strip():
        raise HTTPException(status_code=400, detail="Debes indicar tanto el título como el año de la película.")

    respuesta = movie_model.search_movies_by_name_and_year(titulo, year)
        
    if not respuesta or respuesta.get("Response") == "False":
        raise HTTPException(status_code=404, detail="No se encontraron películas con esos criterios para el año indicado.")
    return respuesta


@app.get("/api/peliculas/detalle/{imdb_id}")
def detalle_pelicula(imdb_id: str):
    """
    Obtiene la información detallada y ampliada de una película mediante su ID único (imdbID).
    """
    detalle = movie_model.fetch_movie_detail(imdb_id)
    if not detalle or detalle.get("Response") == "False":
        raise HTTPException(status_code=404, detail="No se pudo recuperar la información detallada de la película.")
    return detalle


# ==========================================
# 4. RUTAS DE COMENTARIOS CON CONTROL DE USUARIO
# ==========================================
@app.get("/api/comentarios/{imdb_id}")
def obtener_comentarios(imdb_id: str):
    """
    Retorna la lista de comentarios asociados a una película ordenados por fecha/ID.
    """
    comentarios = movie_model.obtener_comentarios(imdb_id)
    return [dict(row) for row in comentarios]


@app.post("/api/comentarios/{imdb_id}")
def agregar_comentario(imdb_id: str, data: ComentarioRequest):
    """
    Guarda un nuevo comentario asegurándose estrictamente de que:
    1. El texto del comentario no esté vacío.
    2. El usuario que comenta esté registrado previamente en la base de datos (evita suplantaciones).
    """
    if not data.comentario.strip():
        raise HTTPException(status_code=400, detail="El texto del comentario no puede estar vacío.")

    # Normalizamos el nombre del usuario introducido
    nombre_usuario_limpio = " ".join(data.persona.strip().split()).title()

    # Verificamos de forma estricta si el usuario existe en la tabla 'usuario'
    usuario_existente = movie_model.buscar_usuario(nombre_usuario_limpio)
    
    if not usuario_existente:
        raise HTTPException(
            status_code=403, 
            detail=f"Acceso denegado: El usuario '{nombre_usuario_limpio}' no está registrado. Es obligatorio iniciar sesión para comentar."
        )

    # Si todo es correcto, guardamos el comentario vinculado al usuario validado
    exito = movie_model.guardar_comentario(imdb_id, nombre_usuario_limpio, data.comentario)
    
    if exito:
        return {
            "status": "success", 
            "mensaje": "Comentario guardado correctamente.", 
            "usuario": nombre_usuario_limpio
        }
    else:
        raise HTTPException(status_code=500, detail="Error interno al intentar guardar el comentario en la base de datos.")