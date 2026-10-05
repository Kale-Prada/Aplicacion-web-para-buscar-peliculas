#main-py - archivo ejecutable

from controller import MovieController

if __name__ == "__main__":
    # Arrancamos el controlador de la aplicación
    app = MovieController()
    app.run()