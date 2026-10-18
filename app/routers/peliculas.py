#Búsqueda de películas e información (detalles) 

from fastapi import APIRouter, HTTPException
from app.model import MovieModel

router = APIRouter(prefix="/api/peliculas", tags=["Películas y OMDb"])
movie_model = MovieModel()

@router.get("/buscar")
def buscar_por_pelicula(titulo: str):
    """Búsqueda exclusiva por el nombre o título de la película."""
    if not titulo.strip():
        raise HTTPException(status_code=400, detail="El título de la película no puede estar vacío.")

    respuesta = movie_model.search_movies_by_name(titulo)
    if not respuesta or respuesta.get("Response") == "False":
        raise HTTPException(status_code=404, detail="No se encontraron películas que coincidan con ese título.")
    return respuesta


@router.get("/buscar-por-anio")
def buscar_por_pelicula_y_anio(titulo: str, year: str):
    """Búsqueda combinada por título de la película y año específico."""
    if not titulo.strip() or not year.strip():
        raise HTTPException(status_code=400, detail="Debes indicar tanto el título como el año de la película.")

    respuesta = movie_model.search_movies_by_name_and_year(titulo, year)
    if not respuesta or respuesta.get("Response") == "False":
        raise HTTPException(status_code=404, detail="No se encontraron películas con esos criterios para el año indicado.")
    return respuesta


@router.get("/detalle/{imdb_id}")
def detalle_pelicula(imdb_id: str):
    """Obtiene la información detallada y ampliada de una película mediante su ID único."""
    detalle = movie_model.fetch_movie_detail(imdb_id)
    if not detalle or detalle.get("Response") == "False":
        raise HTTPException(status_code=404, detail="No se pudo recuperar la información detallada de la película.")
    return detalle