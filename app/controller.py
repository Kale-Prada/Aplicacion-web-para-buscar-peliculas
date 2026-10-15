# Controla o gestiona el flujo del programa conectando el modelo con la vista
# Incluye la visualización de los comentarios guardados a través del ID "imdb_id"

from app.model import MovieModel
from app.view import MovieView

class MovieController:
    def __init__(self):
         #Inicializo modelo y vista
        self.model = MovieModel()
        self.view = MovieView()
        self.usuario_actual = None

    
    #Lógica de selección de opciones
    def run(self):

        # Bucle de autenticación / registro obligatorio al arrancar
        while not self.usuario_actual:
            nombre, password = self.view.request_user_credentials()
                    
            if not nombre or not password:
                self.view.show_error("El usuario y la contraseña no pueden estar vacíos.")
                continue
                    
            nombre_limpio = " ".join(nombre.strip().split()).title()
            usuario_db = self.model.buscar_usuario(nombre_limpio)
            
            if usuario_db:
                # El usuario existe: llamo a la función dedicada a comprobar la contraseña
                if self.model.verificar_password(nombre_limpio, password):
                    self.usuario_actual = nombre_limpio
                    self.view.show_welcome_user(self.usuario_actual)
                else:
                    self.view.show_error("Contraseña incorrecta. Inténtalo de nuevo.")
            else:
                # El usuario NO existe: le pregunto si desea crearlo
                desea_crear = self.view.prompt_crear_usuario(nombre_limpio)
                if desea_crear:
                    exito = self.model.registrar_usuario(nombre_limpio, password)
                    if exito:
                        self.usuario_actual = nombre_limpio
                        self.view.show_welcome_user(self.usuario_actual)
                    else:
                        self.view.show_error("Hubo un error al registrar el usuario en la base de datos.")
                else:
                    self.view.show_error("No es posible acceder. Es necesario iniciar sesión para buscar películas y comentarlas.")
                    self.view.show_goodbye()
                    exit()


        
        # Bucle principal del menú de opciones para elegir película
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

            # Opción 2: Buscar por nombre y año de la película
            elif option == "2":
                name_movie = self.view.request_movie_name()
                #Si pulsa enter sin introducir datos, se comprueba. 
                if not name_movie:
                    self.view.show_error("Introduce nombre de película. No lo has hecho.")
                    continue
                year_ok = self.view.request_year()
                
                try:
                    api_response = self.model.search_movies_by_name_and_year(name_movie, year_ok)
                    self._process_movie_selection(api_response)
                except Exception:
                    self.view.show_error("Ocurrió un error inesperado al procesar la solicitud.")

            # Opción 3: Salir del programa. 
            elif option == "3":
                self.view.show_goodbye()
                break
            else:
                self.view.show_error("Opción incorrecta. Seleccione 1, 2 o 3.")

    
    def _process_movie_selection(self, api_response: dict):
        if not api_response or api_response.get("Response") == "False":
            self.view.show_error("No se encontraron películas que coincidan con los criterios.")
            return

        movies_found = api_response.get("Search", [])
        total_acumulado = api_response.get("totalResults", "0")

        self.view.show_movies_list(movies_found, total_acumulado)

        #Guardo la opción (puede ser el número de la película a ver sus detalles o None si escribió 'salir')
        indice_seleccionado = self.view.select_movie_from_list(len(movies_found))

        #Si es None retorno
        if indice_seleccionado is None:
            # Esto interrumpe la ejecución de la función y vuelve directamente al bucle del menú principal sin generar errores de try
            return   

        # Si no es None, el código continúa su ejecución sin generar mensajes de error de try except. 
        movie_elegida = movies_found[indice_seleccionado]

        #Capturo el ID de la película. Importante para luego asignarle un comentario y guardarlo en la BBDD 
        #haciendo que esté relacionado con el ID de la película. 
        imdb_id = movie_elegida.get("imdbID")

        movie_detail = self.model.fetch_movie_detail(imdb_id)

        if movie_detail is None or movie_detail.get("Response") == "False":
            self.view.show_error("No se pudo recuperar la información detallada de la película.")
        else:
            self.view.show_movie_info(movie_detail)


            
            # --- GESTIÓN DE COMENTARIOS CON BUCLE ---

            while True:
                # 1. Obtengo y muestro los comentarios actuales desde SQLite
                comentarios = self.model.obtener_comentarios(imdb_id)
                self.view.show_comments(comentarios)

                # 2. Pregunto si el usuario desea agregar un comentario
                texto_comentario = self.view.prompt_add_comment(self.usuario_actual)
                
                # Si el usuario responde 'n' o no introduce datos, salimos del bucle de comentarios
                if not texto_comentario:
                    break

                # 3. Guardar el comentario usando la sesión del registro de usuario
                exito = self.model.guardar_comentario(imdb_id, self.usuario_actual, texto_comentario)
                if exito:
                    print("\n¡Comentario guardado con éxito!")
                else:
                    self.view.show_error("Hubo un error al guardar el comentario en la base de datos.")