from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

#Importando los routers desde la carpeta 'app'
from app.routers import auth, peliculas, comentarios, calificaciones

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="API de búsqueda de películas y mostrar/dejar comentarios",
    description="Backend con Routers, MVC y FastAPI - By Kale",
    version="1.0.0"
)

# Montamos la carpeta frontend para servir el HTML y los JS estáticos
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Incluimos los enrutadores modulares
app.include_router(auth.router)
app.include_router(peliculas.router)
app.include_router(comentarios.router)
app.include_router(calificaciones.router)

@app.get("/")
def home():
    """
    Ruta raíz de bienvenida.
    """
    return {"mensaje": "¡Bienvenido/a a la API para buscar películas consumiendo OMBd API - By Kale! Accede a /frontend/index.html para ver la aplicación web"}