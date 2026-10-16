#Comentarios sobre las peliculas asegurándose que el usuario está registrado

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.model import MovieModel

router = APIRouter(prefix="/api/comentarios", tags=["Comentarios"])
movie_model = MovieModel()

class ComentarioRequest(BaseModel):
    username: str
    comentario: str

@router.get("/{imdb_id}")
def obtener_comentarios_pelicula(imdb_id: str):
    """
    Obtiene todos los comentarios asociados a una película mediante su imdb_id.
    """
    try:
        comentarios = movie_model.obtener_comentarios(imdb_id)
        # Convertimos los resultados a formato lista de diccionarios si es necesario
        resultados_limpios = []
        for c in comentarios:
            resultados_limpios.append({
                "id": c["id"] if isinstance(c, dict) else c[0],
                "id_pelicula": c["id_pelicula"] if isinstance(c, dict) else c[1],
                "comentario": c["comentario"] if isinstance(c, dict) else c[2],
                "fecha": c["fecha"] if isinstance(c, dict) else c[3],
                "persona": c["persona"] if isinstance(c, dict) else c[4]
            })
        return resultados_limpios
    except Exception as e:
        print(f"Error al obtener comentarios: {e}")
        return []

@router.post("/{imdb_id}")
def agregar_comentario(imdb_id: str, data: ComentarioRequest):
    """
    Guarda un nuevo comentario validando estrictamente que el usuario 
    exista en la BBDD a través de su 'username' único.
    """
    if not data.comentario.strip():
        raise HTTPException(status_code=400, detail="El texto del comentario no puede estar vacío.")

    if not data.username.strip():
        raise HTTPException(status_code=400, detail="El identificador de usuario (username) es obligatorio.")

    username_limpio = data.username.strip().lower()
    usuario_db = movie_model.buscar_usuario_por_username(username_limpio)
    
    if not usuario_db:
        raise HTTPException(
            status_code=403, 
            detail=f"Acceso denegado: El usuario '{username_limpio}' no está registrado."
        )

    usuario_id = usuario_db["id"] if isinstance(usuario_db, dict) else usuario_db[0]
    nombre_a_mostrar = usuario_db["nombre_a_mostrar"] if isinstance(usuario_db, dict) else usuario_db[2]

    exito = movie_model.guardar_comentario(imdb_id, usuario_id, data.comentario)
    
    if exito:
        return {
            "status": "success", 
            "mensaje": "Comentario guardado correctamente.", 
            "usuario": nombre_a_mostrar
        }
    else:
        raise HTTPException(status_code=500, detail="Error interno al guardar el comentario.")