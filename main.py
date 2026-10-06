#main-py - archivo ejecutable. Encargado de hacer la llama a la APP
 
from controller import MovieController
if __name__ == "__main__":
    #Arrancamos el controlador de la aplicación
    app = MovieController()
    app.run()


#versión original
#from controller_old import MovieController

#if __name__ == "__main__":
    # Arrancamos el controlador de la aplicación
 #   app = MovieController()
 #   app.run_options()

