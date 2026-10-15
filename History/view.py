# Se encarga de toda la interacción con la consola (menús, listados, detalles, mostrar 
# comentarios y solicitar nuevos comentarios).

from datetime import datetime

class MovieView:
    def request_user_credentials(self):
        """
        Solicita el nombre de usuario y contraseña (si no existe, se registrará).
        """
        print("\n========================================================")
        print("          BÚSQUEDA DE PELÍCULAS EN OMBd API        ")
        print("             ACCESO / REGISTRO DE USUARIO        ")
        print("========================================================")
        print("Nota: para buscar una película accede con tu usuario y contraseña.")
        print("Si el usuario que has introducido no existe, se creará automáticamente.")
        nombre = input("Introduce tu nombre de usuario: ").strip()
        password = input("Introduce tu contraseña: ").strip()
        return nombre, password

    
    def show_welcome_user(self, nombre_usuario: str):
        """
        Imprime el mensaje de bienvenida, sesión iniciada correctamente. 
        """
        print(f"\n¡Bienvenido/a, {nombre_usuario}! Sesión iniciada correctamente.")
        
    
    def show_menu(self):
        """
        Muestra el menú principal de búsqueda de películas con tres opciones.
        """
        print("\n==============================================")
        print("        BUSCADOR DE PELÍCULAS EN OMDB API       ")
        print("================================================")
        print("1 - Buscar película por título")
        print("2 - Buscar película por título y año")
        print("3 - Salir")
        print("=================================================")
        return input("Seleccione una opción: ").strip()

    
    def request_movie_name(self):
        """
        Función que solicita hacer un INPUT del nombre de la película que se está buscando
        """
        return input("\nIntroduce el nombre de la película que estás buscando: ").strip()

    
    def request_year(self):
        """
        Función que pregunta el año de la película a buscar
        """
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
        """
        Muestra el resultado total de las películas encontradas consumiendo la API de OMBd 
        y lista en pantalla, como máximo, las primeras 10 disponibles. 
        OMBd API no permite paginar más de 10 para ahorrar en recursos. 
        """
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
        """
        Función para controlar la elección de la película encontrada en base a la búsqueda del usuario. 
        Controla si el usuario ha elegido película o ha pulsado enter sin introducir una elección. 
        """
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
        Muestra la información detalla de la película elegida por el usuario
        y que obtengo consumiendo la API de OMBd API. 
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


    def prompt_crear_usuario(self, usuario_actual: str):
        """
        Pregunta si se desea crear el usuario introducido (porque no existe en la BBDD)
        para iniciar sesión.
        """
        desea_crear_usuario = input(f"\n¿Deseas crear el usuario: '{usuario_actual}' para acceder a la búsqueda de películas y comentarlas? (s/n): ").strip().lower()
        # Devuelve True si es 's', y False si es 'n' o cualquier otra cosa que haya introducido el usuario.
        return desea_crear_usuario == 's'

    
    def show_error(self, message: str):
        """
        Muestra mensaje de error en el caso que el login del usuario no sea válido
        """
        print(f"\n{message}")

    
    def show_goodbye(self):
        """
        Muestra en pantalla el mensaje de fin de búsqueda cuando se ha elegido en el ménú 
        de búsqueda de películas la opción 3 para salir. 
        """
        print("\nFin de la búsqueda de películas. ¡Chao!\n")