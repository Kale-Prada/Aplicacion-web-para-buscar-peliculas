# Se encarga de toda la interacción con la consola (menús, listados, detalles, mostrar 
# comentarios y solicitar nuevos comentarios).

from datetime import datetime

class MovieView:
    def request_user_credentials(self):
        """
        Solicita el nombre de usuario y contraseña (si no existe, se registrará).
        """
        print("\n==============================================")
        print("          ACCESO / REGISTRO DE USUARIO        ")
        print("================================================")
        print("💡 Nota: Si el usuario no existe, se creará automáticamente.")
        nombre = input("Introduce tu nombre de usuario: ").strip()
        password = input("Introduce tu contraseña: ").strip()
        return nombre, password

    def show_welcome_user(self, nombre_usuario: str):
        print(f"\n¡Bienvenido/a, {nombre_usuario}! Sesión iniciada correctamente.")
        
    def show_menu(self):
        """Muestra el menú principal con opciones."""
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

    # No puedo listar más de 10 resultados porque es el máximo que pagina OMDb API
    # para controlar sus recursos y ancho de banda. 
    # Así que muestro el total de resultados posibles con la búsqueda realizada con "total_result"
    
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
            
            if entrada.lower() == 'salir':
                print("\nVolviendo al menú anterior...")
                # Devuelvo None para indicar que no se seleccionó ninguna película
                return None  

            # Si dá ENTER sin introducir datos, lo controlamos
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
        """
        Muestra la información detalla de la película elegida por el usuario. 
        """
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

    def show_comments(self, comentarios: list):
        """
        Muestra la lista de comentarios formateados desde las filas del SQLite.
        """
        print("\n===================================")
        print("          COMENTARIOS              ")
        print("===================================")
        if not comentarios:
            print("No hay comentarios todavía para esta película. ¡Sé el primero en comentar!")
        else:
            for row in comentarios:
                print(f"[{row['fecha']}] {row['persona']} dijo:")
                print(f"  -> {row['comentario']}")
                print("-" * 35)
        print("===================================")

    

    def prompt_add_comment(self, usuario_actual: str):
        """
        Pregunta directamente al usuario autenticado si desea dejar un comentario 
        usando el usuario de la sesión.
        """
        desea_comentar = input(f"\n¿Deseas agregar un comentario sobre esta película como '{usuario_actual}'? (s/n): ").strip().lower()
        if desea_comentar == 's':
            texto = input("Escribe tu comentario: ").strip()
            return texto
        return None

    def show_error(self, message: str):
        print(f"\n{message}")

    def show_goodbye(self):
        print("\nFin de la búsqueda de películas. ¡Chao!\n")