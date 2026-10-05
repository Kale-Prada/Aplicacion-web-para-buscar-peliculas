# Actúa como puente. Recibe las órdenes de la Vista, 
# le pide los datos al Modelo y le ordena a la Vista qué debe mostrar en pantalla.

from model import MovieModel
from view import MovieView

class MovieController:
    def __init__(self):
        self.model = MovieModel()
        self.view = MovieView()

    def run(self):
        while True:
            option = self.view.show_menu()

            if option == "1":
                year_ok = self.view.request_year()
                name_movie = self.view.request_movie_name(year_ok)
                
                if not name_movie:
                    self.view.show_error("Introduce nombre de película. No lo has hecho.")
                    continue
                
                try:
                    finded = self.model.fetch_movie(name_movie, year_ok)

                    if finded is None:
                        self.view.show_error("Error de conexión. No se pudo conectar con el servidor.")
                    elif finded.get("Response") == "False":
                        error_detail = finded.get('Error', 'Comprueba el nombre introducido.')
                        self.view.show_error(f"Película no encontrada. Detalle: {error_detail}")
                    else:
                        self.view.show_movie_info(finded)

                except Exception:
                    self.view.show_error("Ocurrió un error inesperado al procesar los datos de la película.")

            elif option == "2":
                self.view.show_goodbye()
                break
            else:
                self.view.show_error("Opción incorrecta. Seleccione 1 o 2.")