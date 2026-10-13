#main-py - archivo ejecutable. Encargado de hacer la llama a la APP
 
from app.controller import MovieController
if __name__ == "__main__":
    #Arrancamos el controlador de la aplicación
    app = MovieController()
    app.run()

