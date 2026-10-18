from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.model import MovieModel

# Si utilizas un router específico o el objeto app principal:
router = APIRouter(prefix="/api/calificaciones", tags=["Calificaciones"])
movie_model = MovieModel()

class CalificacionRequest(BaseModel):
    username: str
    puntuacion: int

@router.post("/{imdb_id}/calificar")
def calificar_pelicula(imdb_id: str, data: CalificacionRequest):
    """
    Registra o actualiza la calificación (1 a 5 estrellas) de un usuario para una película.
    """
    if data.puntuacion < 1 or data.puntuacion > 5:
        raise HTTPException(status_code=400, detail="La puntuación debe ser un valor entero entre 1 y 5.")
    
    exito = movie_model.guardar_o_actualizar_calificacion(imdb_id, data.username, data.puntuacion)
    
    if exito:
        return {"status": "success", "mensaje": "Calificación guardada correctamente."}
    else:
        raise HTTPException(status_code=500, detail="Hubo un error al guardar la calificación en la base de datos.")

@router.get("/{imdb_id}/calificacion")
def obtener_calificacion_pelicula(imdb_id: str):
    """
    Obtiene el promedio de calificaciones y el total de votos para una película.
    """
    resultado = movie_model.obtener_promedio_calificacion(imdb_id)
    return resultado