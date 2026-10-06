from model import MovieModel
from view import MovieView

class MovieController:
    def __init__(self):
        self.model = MovieModel()
        self.view = MovieView()

    def run(self):
        while True:
            option = self.view.show_menu()

            # Opción 1: Buscar solo por el nombre / título de la película
            if option == "1":
                name_movie = self.view.request_movie_name()
                if not name_movie:
                    self.view.show_error("Introduce nombre de película. No lo has hecho.")
                    continue
                try:
                    api_response = self.model.search_movies_by_name(name_movie)
                    self._process_movie_selection(api_response)
                except Exception:
                    self.view.show_error("Ocurrió un error inesperado al procesar la solicitud.")

            # Opción: Buscar películas por año y una palabra clave (acerca del nombre o título de la película, por ejemplo)
            #elif option == "2":
            #    year_ok = self.view.request_year()
            #    palabra_filtro = self.view.request_optional_keyword()
            #    try:
            #        api_response = self.model.search_movies_by_year(palabra_filtro, year_ok)
            #        self._process_movie_selection(api_response)
            #    except Exception:
            #        self.view.show_error("Ocurrió un error inesperado al procesar la solicitud.")

            # Opción 2: Buscar por título y año de la película de forma simultánea 
            elif option == "2":
                name_movie = self.view.request_movie_name()
                if not name_movie:
                    self.view.show_error("Introduce nombre de película. No lo has hecho.")
                    continue
                year_ok = self.view.request_year()
                
                try:
                    # Solicitamos la combinación exacta de ambos filtros al modelo
                    api_response = self.model.search_movies_by_name_and_year(name_movie, year_ok)
                    self._process_movie_selection(api_response)
                except Exception:
                    self.view.show_error("Ocurrió un error inesperado al procesar la solicitud.")

            # Opción: Salir o terminar el programa
            elif option == "3":
                self.view.show_goodbye()
                break
            else:
                self.view.show_error("Opción incorrecta. Seleccione 1, 2 o 3.")

    def _process_movie_selection(self, api_response: dict):
        """
        Procesa la respuesta global de la API para gestionar metadatos y selección.
        """
        if not api_response or api_response.get("Response") == "False":
            self.view.show_error("No se encontraron películas que coincidan con los criterios.")
            return

        movies_found = api_response.get("Search", [])
        total_acumulado = api_response.get("totalResults", "0")

        self.view.show_movies_list(movies_found, total_acumulado)

        #Guardo la opción (puede ser el número de la película a ver sus detalles o None si escribió 'salir')
        indice_seleccionado = self.view.select_movie_from_list(len(movies_found))

        #Si el usuario decide salir, salgo del código con un return
        if indice_seleccionado is None:
            return  # Esto corta la función y vuelve directamente al bucle del menú principal sin generar errores de try except

        # Si no es None, el código continúa su ejecución sin generar mensajes de error de try except. 
        movie_elegida = movies_found[indice_seleccionado]
        imdb_id = movie_elegida.get("imdbID")

        
        movie_elegida = movies_found[indice_seleccionado]
        imdb_id = movie_elegida.get("imdbID")

        movie_detail = self.model.fetch_movie_detail(imdb_id)

        if movie_detail is None or movie_detail.get("Response") == "False":
            self.view.show_error("No se pudo recuperar la información detallada de la película.")
        else:
            self.view.show_movie_info(movie_detail)
