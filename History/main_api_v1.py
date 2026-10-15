#'main_api.py' de prueba inicial para comprobar que mi código está bien estructurado 
# FastAPI muestra la interfaz gráfica de forma interactiva (Swagger UI) donde empiezo a 
# probar mis rutas. 


from fastapi import FastAPI
from app.model import MovieModel











# Inicializamos la aplicación de FastAPI
app = FastAPI(
    title="API de Búsqueda de Películas",
    description="Backend profesional desarrollado con FastAPI, SQLite y OMDb API by Kale",
    version="1.0.0"
)

# Instanciamos nuestro modelo para reutilizar toda la lógica que ya tenemos hecha
movie_model = MovieModel()

@app.get("/",tags=['Home'])
def home():
    """
    Ruta raíz de bienvenida. 
    Cuando entres a http://127.0.0.1:8000/ verás este mensaje en formato JSON.
    """
    return {"mensaje": "¡Bienvenido/a a la API de búsqueda de películas con FastAPI de Kale!"}

@app.get("/api/peliculas/{titulo}",tags=['Buscar Películas'])
def buscar_peliculas(titulo: str):
    """
    Endpoint para buscar películas por título utilizando directamente el modelo existente.
    Ejemplo: http://127.0.0.1:8000/api/peliculas/matrix
    """
    resultado_api = movie_model.search_movies_by_name(titulo)
    return resultado_api