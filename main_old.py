# Librería para hacer consultas HTTP con request. 
import requests as consulta
# Libreria para obtener automáticamente el año actual.
from datetime import datetime


def year_checking():
    """
    Función que comprueba si el año introducido por teclado cumple con los requisitos: 
    Largo de 4 dígitos numéricos, mayor o igual a 1888 y que no sea mayor al año actual. 
    No saldrá del bucle de pregunta hasta que no se introduzca un año correcto. 
    """
    actual_year = datetime.now().year

    while True:
        entrada = input("Introduce el año de la adaptación cinematográfica de la película: ").strip()
    
        # Valido que sean 4 dígitos y que sean numéricos
        if len(entrada) != 4 or not entrada.isdigit():
            print("Error: El año debe tener exactamente 4 dígitos numéricos.")
            continue  
    
        # Convierto a entero únicamente para validar el formato numérico de rangos
        year_int = int(entrada)
    
        # Limito el rango del año (que no sea anterior a 1888 ni que sea un año mayor al actual)
        if year_int < 1888 or year_int > actual_year:
            print(f"Error: El año debe estar entre 1888 y {actual_year}.")
            continue
    
        # SOLUCIÓN: Si cumple con los requisitos, devolvemos la 'entrada' como STRING
        print(f"¡Correcto! Has introducido el año: {entrada}\n")
        return entrada


# Método
def find_movies(nombre: str, year_string: str):
    """
    Hace "consulta" a OMDb omdbapi.com a través de librería HTTP de Python "request"
    En la consulta se le pasa parámetro "nombre", "year" como string y la API Key. 
    """
    try:
        # Hago la consulta a la URL 
        respuesta = consulta.get(
            f"http://www.omdbapi.com/?t={nombre.lower()}&y={year_string}&apikey=749ee767"
        )

        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            return None
    
    except Exception:
        # Si hay errores de red o conexión al servidor, devuelvo None. 
        return None


# Bucle principal del menú
while True:
    print("\n===================================")
    print("        BUSCADOR DE PELÍCULAS       ")
    print("===================================")
    print("1 - Buscar Película por título y año")
    print("2 - Salir")
    print("====================================")
    
    select_option = input("Seleccione una opción: ").strip()

    # Valida si el usuario ha elegido la opción 1
    if select_option == "1":
        
        # Compruebo que el año tenga el formato y longitud adecuados y guarda el STRING devuelto
        year_ok = year_checking()

        # Después de validar el año, seguimos con el nombre de la película
        name_movie = input(f"Introduce el nombre de la película que estás buscando del año {year_ok}: ").strip()
        
        if not name_movie:
            print("\nIntroduce nombre de película. No lo has hecho.")
            continue
        
        try:
            # Asignar variable "finded" a la búsqueda que hace la función find_movies
            finded = find_movies(name_movie, year_ok)

            # VALIDACIÓN: ¿La API respondió o hubo un problema de red?
            if finded is None:
                print("\nError de conexión. No se pudo conectar con el servidor.")

            # VALIDACIÓN: ¿La película existe en la base de datos del OMDb?
            elif finded.get("Response") == "False":
                print("\nPelícula no encontrada.")
                print(f"Detalle: {finded.get('Error', 'Comprueba el nombre introducido.')}")
                                
            else:
                # Al pasar todas las validaciones, se muestra la información del OMDb
                print("\n===================================")
                print("     INFORMACIÓN DE LA PELÍCULA     ")
                print("===================================")

                print(f"Título: {finded.get('Title', 'N/A').capitalize()}")         
                print(f"Año: {finded.get('Year', 'N/A')}")
                print(f"Clasificación: {finded.get('Rated', 'N/A')}")
                print(f"Estreno: {finded.get('Released', 'N/A')}")
                print(f"Duración: {finded.get('Runtime', 'N/A')}")
                
                # CORREGIDO: Cambiado de corchetes a .get() para evitar caídas imprevistas
                print(f"Género: {finded.get('Genre', 'N/A')}")
                
                print(f"Director: {finded.get('Director', 'N/A')}")
                print(f"Guionista/s: {finded.get('Writer', 'N/A')}")
                print(f"Actores: {finded.get('Actors', 'N/A')}")
                print(f"Sinopsis: {finded.get('Plot', 'N/A')}")
                print(f"Idioma: {finded.get('Language', 'N/A')}")
                print(f"País: {finded.get('Country', 'N/A')}")
                print(f"Premios: {finded.get('Awards', 'N/A')}")

                # Sección de Notas técnicas
                print(f"Metascore: {finded.get('Metascore', 'N/A')}")
                print(f"imdbRating: {finded.get('imdbRating', 'N/A')}")
                print(f"imdbVotes: {finded.get('imdbVotes', 'N/A')}")
                print(f"imdbID: {finded.get('imdbID', 'N/A')}")
                print(f"Type: {finded.get('Type', 'N/A')}")
                print(f"DVD: {finded.get('DVD', 'N/A')}")
                print(f"BoxOffice: {finded.get('BoxOffice', 'N/A')}")
                print(f"Production: {finded.get('Production', 'N/A')}")
                print(f"Website: {finded.get('Website', 'N/A')}")
                print(f"Response: {finded.get('Response', 'N/A')}")

        except Exception as validation_error: 
            print(f"\nOcurrió un error inesperado al procesar los datos de la película.")
            print("\n\n")

    elif select_option == "2":
        print("\nGracias por utilizar esta aplicación para buscar películas.\n")
        break

    else:
        print("\nOpción incorrecta.")
        print("Seleccione 1 o 2.")