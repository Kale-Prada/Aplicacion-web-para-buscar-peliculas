# Proyecto final Bootcamp Aprender a programar desde cero XXVI: Aplicación web para buscar películas por nombre y año en que se llevó a la gran pantalla


## ¿Qué debe hacer mi programa?


**Crear una aplicación web donde se pueda:** 
- Buscar las películas por titulo y año.
- Ver el detalle de cada película con el API proporcionado desde https://www.omdbapi.com/
- Registrar comentarios sobre cada película dentro de la vista de detalle de la película.

**Opcional (como desafío extra):** 

- Se debe poder calificar la película de 1 a 5 puntos presentando en la vista Front-end (HTML, CSS, JavaScript).
- Obtener un promedio de todas las calificaciones en una vista de estrellas.


## Detalles del programa:

**FUNCIONALIDADES - PARTE 1:**
- Es necesario registrarse en https://www.omdbapi.com/ obtener una API key y así poder utilizar el OMDb de omdbapi.com que nos ayudará para obtener los datos para las funcionalidades para consumir la API con REQUEST:

    - Búsqueda de películas por titulo.
    - Búsqueda de películas por año.
    - Dentro de la lista al darle click poder visualizar el detalle de la película seleccionada.

**FUNCIONALIDADES - PARTE 2:**
- Utilizando el motor de base de datos SQLite creamos una base de datos con la tabla "comentario" con las columnas: 
    - id(int)
    - id_pelicula(int)
    - persona(str)
    - comentario(str)
    - fecha(date) 

    
    Donde debemos realizar :

    - Registrar comentarios sobre cada película dentro de la vista de detalle de película, todos los comentarios de una película se deben visualizar en la vista de su detalle.
    - En id_película guardar el id de la película para poder relacionar los datos guardados en nuestra base de datos y los del API.
    - En fecha guardamos la fecha actual/local del servidor.  


**FUNCIONALIDADES - PARTE 3:**
- Utilizando el motor de base de datos SQLite creamos una base de datos con la tabla "calificacion" con las columnas:
    - id(int)
    - id_pelicula(int)
    - persona(str)
    - calificacion(int)
    - fecha(date) 

    Donde debemos realizar:

    - Poder calificar la película de 1 a 5 puntos, esto lo podemos presentar en la vista Frontend de detalle sacando un promedio de todas las calificaciones hechas sobre una película, en una vista de estrellas.
    - En id_película guardar el id de la película para poder relacionar los datos guardados en nuestra base de datos y los de la API.
    - En fecha guardamos la fecha actual/local del servidor. 



## Especificaciones técnicas
- Framework FastAPI.
- Base de datos SQLite.
- Framework CSS Bootstrap.
- Link para API externa de información de películas https://www.omdbapi.com/
- Utilizar el patrón para la arquitectura del proyecto MVC.
- Implementar control de errores.


## Detalles para ejecutar la API en tu entorno


### Instalación y Ejecución

1. Clona o descarga el repositorio en tu equipo.
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
   
4. Instala las librerías necesarias ejecutando:
   ```bash
   # En Windows:
   pip install -r requirements.txt

   # En macOS/Linux:
   pip3 install -r requirements.txt
   ```


## Licencia

Autor = Kale-Prada siguiendo el bootcamp "Programación cero" de Keepcoding España S.L.U.
