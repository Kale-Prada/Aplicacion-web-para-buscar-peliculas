from fastapi import FastAPI
from app.routers import auth, peliculas, comentarios

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="API de búsqueda de películas y mostrar/dejar comentarios",
    description="Backend con Routers, MVC y FastAPI - By Kale",
    version="1.0.0"
)

# Incluimos los enrutadores modulares
app.include_router(auth.router)
app.include_router(peliculas.router)
app.include_router(comentarios.router)

@app.get("/")
def home():
    """Ruta raíz de bienvenida."""
    return {"mensaje": "¡Bienvenido/a a la API para buscar películas consumiendo OMBd API - By Kale!"}