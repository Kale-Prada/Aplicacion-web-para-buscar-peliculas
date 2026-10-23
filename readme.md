# Proyecto final Bootcamp "Aprender a programar desde cero ed. XXVI con Keepcoding"

**Kale App** es una aplicación web de búsqueda, comentarios y valoración de películas desarrollada en Python para el Bootcamp de programación cero con Python de Keepcoding. La lógica se plantea bajo la estructura MVC (Modelo-Vista-Controlador) que combina el backend modular en FastAPI y base de datos SQLite, conectada con la OMDb API (https://www.omdbapi.com/), junto a una interfaz frontend responsiva construida con [Bootstrap](https://getbootstrap.com/) y JavaScript.

La aplicación cuenta con un diseño personalizado, un sistema de autenticación de usuarios, comentarios interactivos con calificaciones por estrellas y un mecanismo de control de errores para garantizar una experiencia visual clara y agradable para el usuario (UX).


## Aspecto visual: 

![Portada Kale App](/frontend/static/readme_imgs/vista_principal_kale_app.jpg)



## De acuerdo a las especificaciones del proyecto final del bootcamp

## ¿Qué debe hacer mi programa?


**Crear una aplicación web donde se pueda:** 
- Buscar las películas por titulo y año.
- Ver el detalle de cada película con el API proporcionado desde https://www.omdbapi.com/
- Registrar comentarios sobre cada película dentro de la vista de detalle de la película.

**Opcional (como desafío extra):** 

- Se debe poder calificar la película de 1 a 5 puntos presentando en la vista Front-end (HTML, CSS, JavaScript).
- Obtener un promedio de todas las calificaciones en una vista de estrellas.

## PLUS de mi proyecto final:

- Además de buscar películas por título, título y año, se pueden hacer búsquedas por el IMDb ID consumiendo la API de OMBd (http://www.omdbapi.com)

![Búsquedas por imbd_id](/frontend/static/readme_imgs/busqueda_por_imdb_id.jpg)

- Sistema de autenticación por login y contraseña para poder comentar y calificar con estrellas las películas en la sección detalles, creando una tabla ```'usuario'``` en la base de datos ```'moviesearch.db'```

![Autenticación de nuevo usuario](/frontend/static/readme_imgs/autenticacion_usuario_pw.jpg)

- Opción de registrarse con 'usuario' (es único), nombre visible (que se muestra en los comentarios) y contraseña para dejar un comentario o calificar una película.

![Registro de nuevo usuario](/frontend/static/readme_imgs/registro_nuevo_usuario.png)

- Para comentar y/o calificar del 1 al 5 con estrellas una película, es necesario autenticarse con las credenciales. Si no se tienen, primero hay que registrarse y luego ir a la ventana de autenticación. 

- Si el usuario vuelve a votar la misma película, en lugar de duplicar registros, se actualiza su nota anterior.

- ***IMPORTANTE: No es necesario estar autenticado para buscar las películas y ver comentarios de otros usuarios.***

- **UX (experiencia de usuario)** al presentar alertas al usuario en ventanas emergentes mostrando mensajes de acuerdo a la acción, pintado con Bootstrap 

![Mostrar alertas](/frontend/static/readme_imgs/mostrar_alertas.png)
![Mostrar alertas](/frontend/static/readme_imgs/mostrar_alertas_1.png)


- Si al buscar la película OMDb API me devuelve 'N/A' significa que no tiene póster disponible, le pongo uno personalizado:  

```const poster = pelicula.Poster !== "N/A" ? pelicula.Poster : "/frontend/static/imgs/poster-pelicula-kale.jpg";```. 

![Póster no disponible N/A](/frontend/static/imgs/poster-pelicula-kale.jpg)

- Si al consultar el póster de la película a la que quiero ver el detalle me devuelve un error HTTP 404 (o 404 Not Found) es un código de estado de HTTP que indica que el servidor logró conectarse, pero no encontró el recurso o la página web que se había solicitado. Muestro un póster personalizado: 

con ```'onerror'``` captura el error HTTP 404 de la imagen externa y carga mi poster con una imagen que indica: 'temporalmente no disponible'. 

   ```<img src="${poster}" class="card-img-top" alt="${pelicula.Title}" style="height: 350px; object-fit: cover;" onerror="this.onerror=null; this.src='/frontend/static/imgs/poster-no-disponible-temporalmente.jpg';">```

![Póster no disponible temporalmente Error HTTP 404](/frontend/static/imgs/poster-no-disponible-temporalmente.jpg)

- Al lanzar FastAPI desde la consola, la aplicación buscará si está creada la Base de datos y sus tablas. En este caso al descargar o clonar el repositorio ya tendrás una copia de la base de datos. 

- En el caso que, por alguna razón, no tengas la base de datos y la aplicación no te la haya creado, puedes crearlo manualmente copiando desde ```/app/bd/create_tables.sql```

- Por último y no menos importante, mi API tiene nombre y marca propia: "Kale App - Búsqueda de películas", además de logo, favicon y banner en portada.
<br>

**Logo en colores corporativos y blanco:** 

![Kale App logo](/frontend/static/readme_imgs/logo-kale-app-400px.jpg) <br>
![Kale App logo](/frontend/static/readme_imgs/logo-kale-app-blanco-400px.jpg) <br>


**Favicon:** 

![Favicon](/frontend/static/readme_imgs/favicon_150x.png) <br> 


**Banner de la portada:**   
<br>
![banner portada](/frontend/static/imgs/portada-banner.jpg)


## Detalles del programa + PLUS:

<br>

**FUNCIONALIDADES - PARTE 1:**
- En el caso que al probar mi aplicación, se hayan agotado las conexiones con mi API KEY, es necesario registrarse en https://www.omdbapi.com/ con tu correo electrónico y obtener una API key para poder utilizar el OMDb de omdbapi.com que nos ayudará a obtener los datos consumiendo la API con la librería *request*:

Modifica esta parte del código con la nueva API KEY (/app/model.py):

```
class MovieModel:
    def __init__(self):
        self.api_key = "********"    #Nueva API KEY
        self.base_url = "http://www.omdbapi.com"
        self.db = DatabaseConnection()
```

Una vez tengamos la API KEY, podemos: 

- Búsqueda de películas por titulo.
- Búsqueda de películas por título y año.
- Búsqueda de películas por ```'ombd_id'``` (ID de la película)
- Dentro de la lista al darle click poder visualizar el detalle de la película seleccionada.
- Si estás autenticado con usuario y contraseña, se puede dejar comentarios y calificar la película. 
- Realizar búsquedas y leer comentarios de una película sin tener que estar autenticado.  
<br> 

**FUNCIONALIDADES - PARTE 2:**
- Utilizando [BD Browser for SQLite](https://sqlitebrowser.org/) crear una BBDD llamada ```moviesearch.db```con la tabla ```comentario``` con las columnas: 
    - id(int)
    - id_pelicula(text)
    - id_usuario(int)
    - comentario(str)
    - fecha(date) 

    
    Donde se debe poder:

    - Registrar comentarios sobre cada película dentro de la vista de detalle de película, todos los comentarios de una película se deben visualizar en la vista de su detalle.
    - En ```id_película```, guardar el id de la película para poder relacionar los datos guardados en la base de datos y los de la API.
    - En ```fecha```, gaurdar la fecha y hora actual/local del servidor.  
<br>

**FUNCIONALIDADES - PARTE 3:**
- Utilizando [BD Browser for SQLite](https://sqlitebrowser.org/) crear en la misma base de datos ```moviesearch.db``` con la tabla ```calificacion``` las columnas:
    - id(int)
    - id_pelicula(text)
    - username(text)
    - puntuacion(int)
    - fecha(date) 

    Donde:

    - Poder calificar la película de 1 a 5 puntos, esto lo podemos presentar en la vista Frontend de detalle sacando un promedio de todas las calificaciones hechas sobre una película, en una vista de estrellas.
    - En ```id_película```, guardar el id de la película para poder relacionar los datos guardados en nuestra base de datos y los de la API.
    - En ```fecha```, guardar la fecha y hora actual/local del servidor.  
<br>


**FUNCIONALIDADES - PARTE 4 (PLUS):**
- Utilizando [BD Browser for SQLite](https://sqlitebrowser.org/) crear en la misma base de datos ```moviesearch.db``` con la tabla ```usuario``` las columnas:
    - id(int)
    - username(text)
    - nombre_a_mostrar (text)
    - password(text)

    Donde:

    - Sistema de autenticación por login y contraseña para poder comentar y calificar con estrellas las películas dentro de los detalles de la palícula.
    - Opción de registrarse con ```username``` (es único), nombre visible (que se muestra en los comentarios) y contraseña para dejar un comentario o calificar una película.
  <br>  


## Especificaciones técnicas
- Framework [FastAPI](https://fastapi.tiangolo.com/)
- Base de datos SQLite con [BD Browser for SQLite](https://sqlitebrowser.org/)
- Framework CSS [Bootstrap](https://getbootstrap.com/)    
- Link para API externa de información de películas https://www.omdbapi.com/
- Utilizar el patrón para la arquitectura del proyecto MVC.
- Implementación de control de errores.
- Implementación de carpeta ```test``` y pruebas con ```pytest```


## Detalles para ejecutar  *"Kale App - Buscador de películas"* en tu entorno


### Instalación y Ejecución

1. Desde Git Hub clona o descarga el repositorio en tu equipo.
2. Abre la carpeta del proyecto en Visual Studio Code.
3. Crea y activa un entorno virtual:
    ```bash
    # Para crear el entorno: 
    # En Windows: 
    python -m venv entorno
    
    #Otra opción: 
    py -m venv entorno 

    # En MacOS: 
    python3 -m venv entorno

    # Para activar el entorno: 
    # En Windows (PowerShell):
    .\entorno\Scripts\activate

    # En macOS/Linux:
    source entorno/bin/activate
    ```
    _Tu entorno estará activo cuando veas el nombre (entorno) al principio de la línea de comandos de tu terminal._

    3.1 Si da error al activar el entorno, para permisos de visual studio code 

    ```Set-ExecutionPolicy Unrestricted```

    3.2 Para ver las librerias que tengo instaladas en mi entorno 

    ```pip freeze```


4. Instala las librerías necesarias ejecutando (es muy importante este paso, ¡no lo saltes!):
   ```bash
   # En Windows:
   pip install -r requirements.txt

   # En macOS/Linux:
   pip3 install -r requirements.txt
   ```


5. Desactiva el entorno y vuelve a activarlo

    ```bash
     # Para desactivar el entorno: 
    deactivate (enter desde la terminal)

     # Para activar el entorno
    source entorno/bin/activate
    
     # En Windows: 
    .\entorno\Scripts\activate

    ¡Verifica que el entorno está activado! 
    ```


6. Ejecuta FastAPI

    **- Lanzar app en modo desarrollo (recomendable para que tome los cambios en tiempo real)**. 

    ```fastapi dev main.py```

    **- Lanzar app en modo producción**. 

    ```fastapi run main.py```

    **- Lanzar app en puerto específico**. 

    ```fastapi dev main.py --port 8090 ``` 

    Si el puerto 8000 está ocupado por otro servicio, puedo cambiar el puerto
    ejecutando ```--port 8090```, por ejemplo.  
    El puerto 8000 es el puerto que FastAPI usa por defecto. 


    Si las librerías están bien instaladas y corriendo sobre el entorno (que debe estar activado), la salida de FastAPI en consola es esta: 

    ```
    ⚡️ Starting FastAPI in development mode
 
     🐍 Using import string: main:app
 
    🌐 Server started at http://127.0.0.1:8000
    Documentation at http://127.0.0.1:8000/docs
    ```

8. Para acceder a Kale APP - Buscador de películas desde tu navegador (Chrome, Firefox, Safari...)

    http://127.0.0.1:8000/frontend/index.html


9. Para acceder a FastAPI y la documentación automática (Swagger UI). Se verán los endpoints creados para conectar con la API y la base de datos 

    http://127.0.0.1:8000/docs

    ![FastAPI & Swagger UI](/frontend/static/readme_imgs/fastapi_swagger_UI.jpg)

10. Disfruta del buscador de películas y todas sus funcionalidades. 



## Licencia

![Kale App logo](/frontend/static/readme_imgs/logo-kale-app-300x.png) <br>
Autor = Kale-Prada siguiendo el bootcamp "Programación cero" de Keepcoding España S.L.U.