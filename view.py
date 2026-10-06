from datetime import datetime

class MovieView:
    def show_menu(self):
        """Muestra el menú principal con 3 opciones."""
        print("\n==============================================")
        print("        BUSCADOR DE PELÍCULAS EN OMDB API       ")
        print("================================================")
        print("1 - Buscar película por título")
        print("2 - Buscar película por título y año")
        print("3 - Salir")
        print("=================================================")
        return input("Seleccione una opción: ").strip()

    def request_movie_name(self):
        return input("\nIntroduce el nombre de la película que estás buscando: ").strip()

    def request_year(self):
        actual_year = datetime.now().year
        while True:
            entrada = input("\nIntroduce el año que deseas buscar: ").strip()
            
            if len(entrada) != 4 or not entrada.isdigit():
                print("Error: El año debe tener exactamente 4 dígitos numéricos.\n")
                continue  
            
            year_int = int(entrada)
            if year_int < 1888 or year_int > actual_year:
                print(f"Error: El año debe estar entre 1888 y {actual_year}.\n")
                continue
                
            return entrada

    def request_optional_keyword(self):
        return input("Introduce una palabra clave que permita mejorar tu búsqueda para filtrar las películas (Ej: 'war', 'love', 'Harry') o pulsa ENTER para ver todas: ").strip()


    # No puedo listar más de 10 resultados porque es el máximo que pagina OMDb API
    # para controlar sus recursos y ancho de banda. 
    #Así que muestro el total de resultados posibles con la búsqueda realizada con "total_result"

    def show_movies_list(self, movies_list: list, total_results: str):
        print("\n=============================================")
        print(f" ¡GENIAL! Se han encontrado {total_results} resultados en total.")
        print(" Mostrando las 10 primeras coincidencias (si existiesen):")
        print("=============================================")
        for indice, movie in enumerate(movies_list, start=1):
            titulo = movie.get("Title", "Sin título")
            anio = movie.get("Year", "N/A")
            tipo = movie.get("Type", "N/A").upper()
            print(f"{indice} - {titulo} ({anio}) [{tipo}]")
        print("=============================================")

    def select_movie_from_list(self, total_movies: int):
        while True:
            
            entrada = input("\nSelecciona el número de la película para ver su detalle (o escribe 'salir' para volver al menú principal): ").strip()
            
            # Pregunto al usuario si en este punto quiere salir para volver al menú anterior. 
            if entrada.lower() == 'salir':
                print("\nVolviendo al menú anterior...")
                return None  # Devuelvo None para indicar que no se seleccionó ninguna película

            # Si dá enter sin escribir nada, lo controlamos
            if not entrada.isdigit():
                print("\nError: Por favor, introduce un número válido.")
                continue

            # Valida que el número introducido sea entre 1 y 10. 
            # No puedo listar más de 10 resultados porque es el máximo que pagina OMDb API
            # para controlar sus recursos y ancho de banda. 
            # Así que me muestra los primeros diez resultados (aunque puedan haber más). 

            opcion = int(entrada)
            if opcion < 1 or opcion > total_movies:
                print(f"\nError: Elige un número disponible en la lista (1 a {total_movies}).")
                continue
            
            return opcion - 1

    def show_movie_info(self, movie_data: dict):
        print("\n===================================")
        print("     INFORMACIÓN DE LA PELÍCULA     ")
        print("===================================")
        print(f"Título: {movie_data.get('Title', 'N/A').capitalize()}")         
        print(f"Año: {movie_data.get('Year', 'N/A')}")
        print(f"Clasificación: {movie_data.get('Rated', 'N/A')}")
        print(f"Estreno: {movie_data.get('Released', 'N/A')}")
        print(f"Duración: {movie_data.get('Runtime', 'N/A')}")
        print(f"Género: {movie_data.get('Genre', 'N/A')}")
        print(f"Director: {movie_data.get('Director', 'N/A')}")
        print(f"Guionista/s: {movie_data.get('Writer', 'N/A')}")
        print(f"Actores: {movie_data.get('Actors', 'N/A')}")
        print(f"Sinopsis: {movie_data.get('Plot', 'N/A')}")
        print(f"Idioma: {movie_data.get('Language', 'N/A')}")
        print(f"País: {movie_data.get('Country', 'N/A')}")
        print(f"Premios: {movie_data.get('Awards', 'N/A')}")
        print(f"Metascore: {movie_data.get('Metascore', 'N/A')}")
        print(f"imdbRating: {movie_data.get('imdbRating', 'N/A')}")
        print(f"imdbVotes: {movie_data.get('imdbVotes', 'N/A')}")
        print(f"imdbID: {movie_data.get('imdbID', 'N/A')}")
        print(f"Type: {movie_data.get('Type', 'N/A')}")
        print(f"DVD: {movie_data.get('DVD', 'N/A')}")
        print(f"BoxOffice: {movie_data.get('BoxOffice', 'N/A')}")
        print(f"Production: {movie_data.get('Production', 'N/A')}")
        print(f"Website: {movie_data.get('Website', 'N/A')}")

    def show_error(self, message: str):
        print(f"\n{message}")

    def show_goodbye(self):
        print("\nFin de la búsqueda de películas. ¡Chao!\n")
