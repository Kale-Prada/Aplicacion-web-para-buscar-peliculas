# Se encarga de la interfaz de usuario (en este caso, los input() y print() de la terminal). 
# No realiza cálculos lógicos ni llamadas HTTP.

from datetime import datetime

class MovieView:
    def show_menu(self):
        """
        Muestra el menú de opciones al principio del programa
        """
        print("\n===================================")
        print("        BUSCADOR DE PELÍCULAS       ")
        print("===================================")
        print("1 - Buscar Película por título y año")
        print("2 - Salir")
        print("====================================")
        return input("Seleccione una opción: ").strip()

    def request_year(self):
        """
            Función que comprueba si el año introducido por teclado cumple con los requisitos: 
            Largo de 4 dígitos numéricos, mayor o igual a 1888 (año en que empezaron a hacer películas) y 
            que no sea mayor al año actual. 
            No saldrá del bucle de pregunta hasta que no se introduzca un año correcto. 
            """
        
        #Guardo en una variable el año actual
        actual_year = datetime.now().year

        while True:
            entrada = input("Introduce el año de la adaptación cinematográfica de la película: ").strip()

            # Validación para comprobar que sean 4 dígitos y numéricos
            # isdigit() comprueba que todos los caracteres de una cadena de texto son números (dígitos del 0 al 9)
            if len(entrada) != 4 or not entrada.isdigit():
                print("Error: El año debe tener exactamente 4 dígitos numéricos.")
                continue  

            # Cambio de tipo str (que es lo que permite la API de OMDb) a entero int
            # Convierto a entero únicamente para validar el formato numérico de rangos
            year_int = int(entrada)

            # Limito el rango del año (que no sea anterior a 1888 ni que sea un año mayor al actual)
            if year_int < 1888 or year_int > actual_year:
                print(f"Error: El año debe estar entre 1888 y {actual_year}.")
                continue

            # Si cumple con los requisitos, devolvemos la 'entrada' como STRING    
            print(f"¡Correcto! Has introducido el año: {entrada}\n")
            return entrada

    def request_movie_name(self, year: str):
        """
        Función que retorna el nombre de la película introducida por teclado
        """
        # .strip() quita los espacios en blanco, tabulaciones y saltos de línea 
        # que están al principio y al final de una cadena de texto
        return input(f"Introduce el nombre de la película que estás buscando del año {year}: ").strip()
    

    def show_movie_info(self, movie_data: dict):
        """
        Muestra como diccionario la información de la película encontrada por 
        nombre y año llevaba a la gran pantalla. 
        Uso capitalize() para cambiar la priemra letra a mayúsculas, el resto minúsculas. 
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
        print(f"DVD: {movie_data.get('MovieView', 'N/A')}")
        print(f"BoxOffice: {movie_data.get('BoxOffice', 'N/A')}")
        print(f"Production: {movie_data.get('Production', 'N/A')}")
        print(f"Website: {movie_data.get('Website', 'N/A')}")

    def show_error(self, message: str):
        print(f"\n{message}")

    def show_goodbye(self):
        """
        Para cerrar el programa, al elegir la opción 2. 
        """
        print("\nGracias por utilizar esta aplicación para buscar películas.\n")