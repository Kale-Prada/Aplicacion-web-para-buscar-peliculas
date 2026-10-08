from fastapi import FastAPI #Query  #Body  #el "body" es una función de FastAPI para enviar el cuerpo de los datos en JSON
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

#Creo clase con los atributos de mi modelo con el ID
class ModelMoviesPost(BaseModel):
    id : int 
    title: str
    overview: str
    rating: float
    category: str

    #Creo clase con los atributos de mi modelo sin el ID
class ModelMoviesUpdate(BaseModel):
    title: str
    overview: str
    rating: float
    category: str

#class ModelBody:
#    def __init__(self,id,title,overview,rating,category):
#        self.id = id
#        self.title = title
#        self.overview = overview
#        self.rating = rating
#        self.category = category

movies = [
    {
        "id":1,
        "title":"Avatar",
        "overview":"En un planeta llamado Pandora...", 
        "category":"Aventura"
    },
    {
        "id":2,
        "title":"Titanic",
        "overview":"El barco más grande mundo jamás creado zarpa a EE. UU.",
        "category":"Romance"
    }
]

#Búsqueda con categoría
@app.get("/html/categoria/",tags=['Garden'])
def get_movie_by_category(category:str):
    for peli in movies:
        if peli['category'] == category:
            return peli
    return []

#Método post "Envío de datos" con append porque es una lista. 
#@app.post("/movies/post",tags=['Post'])
#def create_movie(id:int,title:str,overview:str,rating:float,category:str):
#    movies.append(
 #       {
#            "id":id,
#            "title":title,
 #           "overview":overview,
#            "rating":rating,
#            "category":category
#        }
#    )
 #   return movies



@app.post("/movies/post",tags=['Post'])
def create_movie_pydantic(body:ModelMoviesPost):
    movies.append(
        #con el model_dump convertimos a diccionario para que lo entienda 
        body.model_dump()   
    )
    return movies

@app.put("/movies/post/{id}",tags=['Post'])
def update_movie_pydantic(id:int, body:ModelMoviesUpdate):
    for peli in movies:
        if peli['id'] == id:
            #peli.update(body.model_dump())
            
            #la otra opción es pasarle los parámetros uno a uno. o con "update" (ver código arriba)
            peli['title'] = body.title
            peli['overview'] = body.overview
            peli['category'] = body.category
    
    return movies

#método DELETE - Borrado 
@app.delete("/movies/post/borrado/{id}",tags=['Post'])
def delete_movie_pydantic(id:int):
    for peli in movies:
            if peli['id'] == id:
                #remove es un método de diccionario
                movies.remove(peli)
    return movies


#Pasamos el BODY ENTERO - cuerpo entero de los datos en JSON y con un PYDANTIC (BASEMODEL)
#@app.post("/movies/post",tags=['Post'])
#def create_movie(body:ModelBody=Body()):
#    movies.append(
#        {
#        "id":body.id,
#        "title":body.title,
#        "overview":body.overview,
#        "rating":body.rating,
#        "category":body.category
#        }
#    )




#Pasamos el BODY PARÁMETRO POR PARÁMETRO - cuerpo de los datos en JSON y con un modelo llamado ModelBody
#@app.post("/movies/post",tags=['Post'])
#def create_movie(body:ModelBody=Body()):
#    movies.append(
#        {
 #       "id":body.id,
#       "title":body.title,
 #       "overview":body.overview,
#       "rating":body.rating,
 #       "category":body.category
 #       }
#    )


#Pasamos el BODY - cuerpo entero de los datos en JSON
#@app.post("/movies/post",tags=['Post'])
#def create_movie(id:int=Body(),title:str=Body(),overview:str=Body(),rating:float=Body(),category:str=Body()):
#    movies.append(
#        {
#           "id":id,
#            "title":title,
#            "overview":overview,
#            "rating":rating,
#            "category":category
#        }
#    )
 #   return movies

#Método PUT - actualizar datos 
@app.put("movies/{id}",tags=['Post'])
def update_movie():
    pass
    

#Etiquetas HTML
@app.get("/html",tags=['Garden'])
def movie():
    return movies
    #return HTMLResponse('<h1>Hola esto es una etiqueta HTML</h1>')

#Búsqueda con for
@app.get("/html/{id}",tags=['Garden'])
def get_movie_by_id(id:int):
    for peli in movies:
        if peli['id'] == id:
            return peli
    return []

#Parámetro query /movies/?id=89 Siempre hay que ponerle al final la barra porque si no da error
@app.get("/html/parametro/",tags=['Parametro'])
def get_movie_by_query(year:int,category:str):
    return f"{category},{year}"





#parametro en ruta 
#@app.get("/html/{id}",tags=['Garden'])
#def get_movie_by(id:int):
#    return id
    #return HTMLResponse('<h1>Hola esto es una etiqueta HTML</h1>')


#parametro en ruta 
@app.get("/html/{id}/{nombre}/{apellidos}",tags=['Garden'])
def get_movie_by(id:int, nombre:str, apellidos:str):
    return f"{id} {nombre} {apellidos}"


@app.get("/hola",tags=['Home'])
def index():
    return "hola mundo FastAPI"

@app.get("/adios/ve",tags=['Home'])
def index():
    return "hola mundo FastAPI Vé!"

@app.get("/adios",tags=['Garden'])
def index():
    return "Adiós mundo FastAPI"

