#Comentarios sobre las peliculas asegurándose que el usuario está registrado

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.model import MovieModel

router = APIRouter(prefix="/api/comentarios", tags=["Comentarios"])
movie_model = MovieModel()

class ComentarioRequest(BaseModel):
    username: str       # Cambiamos 'persona' por 'username' para el login técnico
    comentario: str

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

    # Normalizamos el username a minúsculas y sin espacios (como se guarda al registrar)
    username_limpio = data.username.strip().lower()

    # Buscamos al usuario en la base de datos por su username único
    usuario_db = movie_model.buscar_usuario_por_username(username_limpio)
    
    if not usuario_db:
        raise HTTPException(
            status_code=403, 
            detail=f"Acceso denegado: El usuario con username '{username_limpio}' no está registrado."
        )

    # Extraemos el ID y el nombre visible de la base de datos
    usuario_id = usuario_db["id"] if isinstance(usuario_db, dict) else usuario_db[0]
    nombre_a_mostrar = usuario_db["nombre_a_mostrar"] if isinstance(usuario_db, dict) else usuario_db[2]

    # Guardamos asociando el id_usuario
    exito = movie_model.guardar_comentario(imdb_id, usuario_id, data.comentario)
    
    if exito:
        return {
            "status": "success", 
            "mensaje": "Comentario guardado correctamente.", 
            "usuario": nombre_a_mostrar  # Devolvemos el nombre visible para que la interfaz lo muestre bonito
        }
    else:
        raise HTTPException(status_code=500, detail="Error interno al guardar el comentario.")