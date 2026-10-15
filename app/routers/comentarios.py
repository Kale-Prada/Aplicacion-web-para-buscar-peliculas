#Comentarios sobre las peliculas asegurándose que el usuario está registrado

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.model import MovieModel

router = APIRouter(prefix="/api/comentarios", tags=["Comentarios"])
movie_model = MovieModel()

class ComentarioRequest(BaseModel):
    persona: str
    comentario: str

@router.get("/{imdb_id}")
def obtener_comentarios(imdb_id: str):
    """Retorna la lista de comentarios asociados a una película."""
    comentarios = movie_model.obtener_comentarios(imdb_id)
    return [dict(row) for row in comentarios]


@router.post("/{imdb_id}")
def agregar_comentario(imdb_id: str, data: ComentarioRequest):
    """Guarda un nuevo comentario validando estrictamente que el usuario esté registrado."""
    if not data.comentario.strip():
        raise HTTPException(status_code=400, detail="El texto del comentario no puede estar vacío.")

    nombre_usuario_limpio = " ".join(data.persona.strip().split()).title()
    usuario_existente = movie_model.buscar_usuario(nombre_usuario_limpio)
    
    if not usuario_existente:
        raise HTTPException(
            status_code=403, 
            detail=f"Acceso denegado: El usuario '{nombre_usuario_limpio}' no está registrado. Es obligatorio iniciar sesión para comentar."
        )

    exito = movie_model.guardar_comentario(imdb_id, nombre_usuario_limpio, data.comentario)
    if exito:
        return {
            "status": "success", 
            "mensaje": "Comentario guardado correctamente.", 
            "usuario": nombre_usuario_limpio
        }
    else:
        raise HTTPException(status_code=500, detail="Error interno al intentar guardar el comentario en la base de datos.")