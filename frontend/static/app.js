// URL base de la API (al estar en el mismo servidor, podemos usar rutas relativas)
const API_URL = "/api";

// Al cargar la página, comprobamos si el usuario ya inició sesión previamente
document.addEventListener("DOMContentLoaded", () => {
    actualizarEstadoInterfaz();
});

/* ==========================================
   1. GESTIÓN DE SESIÓN Y UI
   ========================================== */

function actualizarEstadoInterfaz() {
    const username = localStorage.getItem("usernameActual");
    const nombreMostrar = localStorage.getItem("nombreMostrarActual");

    const loggedOutSection = document.getElementById("logged-out-section");
    const loggedInSection = document.getElementById("logged-in-section");
    const userDisplayName = document.getElementById("user-display-name");
    
    const commentLoginWarning = document.getElementById("comment-login-warning");
    const commentBox = document.getElementById("comment-box");

    if (username && nombreMostrar) {
        // Usuario logueado
        loggedOutSection.classList.add("d-none");
        loggedInSection.classList.remove("d-none");
        userDisplayName.textContent = nombreMostrar;

        if (commentLoginWarning) commentLoginWarning.classList.add("d-none");
        if (commentBox) commentBox.classList.remove("d-none");
    } else {
        // Usuario invitado / no logueado
        loggedOutSection.classList.remove("d-none");
        loggedInSection.classList.add("d-none");

        if (commentLoginWarning) commentLoginWarning.classList.remove("d-none");
        if (commentBox) commentBox.classList.add("d-none");
    }
}

function cerrarSesion() {
    localStorage.removeItem("usernameActual");
    localStorage.removeItem("nombreMostrarActual");
    actualizarEstadoInterfaz();
    mostrarAlerta("Has cerrado sesión correctamente.");
}


/* ==========================================
   2. AUTENTICACIÓN Y REGISTRO (Endpoints separados)
   ========================================== */

async function ejecutarLogin() {
    const usernameInput = document.getElementById("login-username").value.trim();
    const passwordInput = document.getElementById("login-password").value.trim();

    if (!usernameInput || !passwordInput) {
        mostrarAlerta("Por favor, rellena todos los campos.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/usuarios/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: usernameInput, password: passwordInput })
        });

        const data = await response.json();

        if (response.ok) {
            // Guardamos los datos en localStorage
            localStorage.setItem("usernameActual", data.username);
            localStorage.setItem("nombreMostrarActual", data.usuario);

            // Cerramos el modal de Bootstrap usando su API nativa
            const modalEl = document.getElementById("loginModal");
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.hide();

            actualizarEstadoInterfaz();
            //reemplazo alert() nativo por la ventana personalizada con bootstrap
            mostrarAlerta(data.mensaje);
        } else {
            mostrarAlerta(data.detail || "Error al iniciar sesión.");
        }
    } catch (error) {
        console.error("Error de red en login:", error);
        mostrarAlerta("No se pudo conectar con el servidor.");
    }
}

async function ejecutarRegistro() {
    const usernameInput = document.getElementById("reg-username").value.trim();
    const nombreMostrarInput = document.getElementById("reg-nombre").value.trim();
    const passwordInput = document.getElementById("reg-password").value.trim();

    if (!usernameInput || !nombreMostrarInput || !passwordInput) {
        mostrarAlerta("Todos los campos son obligatorios.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/usuarios/registrar`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: usernameInput,
                nombre_a_mostrar: nombreMostrarInput,
                password: passwordInput
            })
        });

        const data = await response.json();

        if (response.ok) {
            mostrarAlerta(data.mensaje);
            // Cerramos el modal de registro
            const modalEl = document.getElementById("registroModal");
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.hide();
        } else {
            mostrarAlerta(data.detail || "Error en el registro.");
        }
    } catch (error) {
        console.error("Error de red en registro:", error);
        mostrarAlerta("No se pudo conectar con el servidor.");
    }
}


/* ==========================================
   3. BÚSQUEDA DE PELÍCULAS (Ajustado a /buscar?titulo=...)
   ========================================== */

async function buscarPeliculas() {
    const query = document.getElementById("input-buscar").value.trim();
    if (!query) {
        mostrarAlerta("Introduce un título para buscar.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/peliculas/buscar?titulo=${encodeURIComponent(query)}`);
        const data = await response.json();

        const moviesGrid = document.getElementById("movies-grid");
        moviesGrid.innerHTML = "";

        // OMDb devuelve un objeto con la propiedad "Search" si encuentra resultados
        if (data.Search && Array.isArray(data.Search)) {
            data.Search.forEach(pelicula => {
                const poster = pelicula.Poster !== "N/A" ? pelicula.Poster : "/frontend/static/imgs/poster-pelicula-kale.jpg";
                
                const col = document.createElement("div");
                col.className = "col";
                col.innerHTML = `
                    <div class="card h-100 shadow-sm" style="cursor: pointer;" onclick="verDetallePelicula('${pelicula.imdbID}')">
                        <img src="${poster}" class="card-img-top" alt="${pelicula.Title}" style="height: 350px; object-fit: cover;">
                        <div class="card-body">
                            <h5 class="card-title fs-6 text-truncate">${pelicula.Title}</h5>
                            <p class="card-text text-muted small">${pelicula.Year}</p>
                        </div>
                    </div>
                `;
                moviesGrid.appendChild(col);
            });
        } else {
            moviesGrid.innerHTML = `<div class="col-12 text-center"><p class="text-muted">No se encontraron películas con ese título.</p></div>`;
        }
    } catch (error) {
        console.error("Error al buscar películas:", error);
        mostrarAlerta("Hubo un error al realizar la búsqueda.");
    }
}

/* ==========================================
   4. BÚSQUEDA DE PELÍCULAS (Título / Título y Año) / IMDb ID
   ========================================== */

/* Búsqueda de películas por título */   

async function buscarPeliculasPorTitulo() {
    const query = document.getElementById("input-buscar-titulo").value.trim();
    if (!query) {
        mostrarAlerta("Introduce un título para buscar.");
        return;
    }

    try {
        // Conexión con el endpoint existente
        const response = await fetch(`${API_URL}/peliculas/buscar?titulo=${encodeURIComponent(query)}`);
        const data = await response.json();
        renderizarResultados(data, "titulo");
    } catch (error) {
        console.error("Error al buscar películas:", error);
        mostrarAlerta("Hubo un error al realizar la búsqueda.");
    }
}

/* Búsqueda de películas por título y año */  

async function buscarPeliculasPorTituloYAnio() {
    const titulo = document.getElementById("input-buscar-titulo-anio").value.trim();
    const year = document.getElementById("input-buscar-anio").value.trim();

    if (!titulo || !year) {
        mostrarAlerta("Debes indicar tanto el título como el año de la película.");
        return;
    }

    try {
        // Conexión con el endpoint existente: /api/peliculas/buscar-por-anio?titulo=...&year=...
        const response = await fetch(`${API_URL}/peliculas/buscar-por-anio?titulo=${encodeURIComponent(titulo)}&year=${encodeURIComponent(year)}`);
        const data = await response.json();
        renderizarResultados(data, "titulo");
    } catch (error) {
        console.error("Error al buscar por título y año:", error);
        mostrarAlerta("No se encontraron películas con esos criterios o hubo un error en la red.");
    }
}

/* Búsqueda de películas por IMDb ID */

async function buscarPeliculaPorImdbId() {
    const inputImdb = document.getElementById("input-buscar-imdb");
    const imdbId = inputImdb ? inputImdb.value.trim() : "";

    if (!imdbId) {
        mostrarAlerta("Por favor, introduce un identificador válido de IMDb (ej. tt0133093).");
        return;
    }

    // Como es una búsqueda directa por ID, reutilizo verDetallePelicula para cargar la ficha técnica
    verDetallePelicula(imdbId);
}

// Función auxiliar unificada para pintar las tarjetas de películas y mostrar el contador de OMDb
function renderizarResultados(data, tipoBusqueda = "título") {
    const moviesGrid = document.getElementById("movies-grid");
    const counterContainer = document.getElementById("search-counter-container");
    const counterText = document.getElementById("search-counter-text");
    
    moviesGrid.innerHTML = "";

    if (data.Search && Array.isArray(data.Search)) {
        // OMDb devuelve el total de resultados globales en data.totalResults
        const totalResultados = data.totalResults || data.Search.length;
        
        // Mostramos el contenedor con el mensaje personalizado según la búsqueda
        if (counterContainer && counterText) {
            counterContainer.classList.remove("d-none");
            if (tipoBusqueda === "titulo-anio") {
                counterText.innerHTML = `¡Genial! Se han encontrado <strong>${totalResultados}</strong> resultados en total con el filtro de búsqueda aplicado. Mostrando las 10 primeras coincidencias.`;
            } else {
                counterText.innerHTML = `¡Genial! Se han encontrado <strong>${totalResultados}</strong> resultados en total en OMDb API. Mostrando las 10 primeras coincidencias.`;
            }
        }

        data.Search.forEach(pelicula => {
            // Si OMDb devuelve "N/A", uso mi propio poster
            const poster = pelicula.Poster !== "N/A" ? pelicula.Poster : "/frontend/static/imgs/poster-pelicula-kale.jpg";
            
            const col = document.createElement("div");
            col.className = "col";
            col.innerHTML = `
                <div class="card h-100 shadow-sm" style="cursor: pointer;" onclick="verDetallePelicula('${pelicula.imdbID}')">

                    <!-- onerror captura el error HTTP 404 de la imagen externa y carga mi poster con una imagen que indica: 'temporalmente no disponible' -->
                    <img src="${poster}" class="card-img-top" alt="${pelicula.Title}" style="height: 350px; object-fit: cover;" onerror="this.onerror=null; this.src='/frontend/static/imgs/poster-no-disponible-temporalmente.jpg';">
                    <div class="card-body">
                        <h5 class="card-title fs-6 text-truncate">${pelicula.Title}</h5>
                        <p class="card-text text-muted small">${pelicula.Year}</p>
                    </div>
                </div>
            `;
            moviesGrid.appendChild(col);
        });
    } else {
        // Si no hay resultados, ocultamos el contador y mostramos el aviso de que no hay coincidencias
        if (counterContainer) counterContainer.classList.add("d-none");
        /* Asegurarse de dejar limpia el campo para que no quede restos de búsquedas anteriores */
        moviesGrid.innerHTML = "";
        
        // Llamada a tu función personalizada para mostrar el aviso con los colores corporativos
        mostrarAlerta("No se encontraron películas que coincidan con los criterios de búsqueda.");
        
    }
}


/* ==========================================
   5. DETALLE DE PELÍCULA Y COMENTARIOS (Ajustado a /detalle/{id})
   ========================================== */

let currentImdbId = null;

async function verDetallePelicula(imdbId) {
    currentImdbId = imdbId;

    // 1. Obtener detalles completos de la película mediante el endpoint /api/peliculas/detalle/{imdbId}
    try {
        const resDetalle = await fetch(`${API_URL}/peliculas/detalle/${imdbId}`);
        const pelicula = await resDetalle.json();

        // Validamos si OMDb API devuelve que el ID no existe ("Response": "False") o no trae título
        if (pelicula.Response === "False" || !pelicula.Title) {
            mostrarAlerta("El identificador IMDb introducido no existe o no es válido. Por favor, comprueba el ID e inténtalo de nuevo.");
            volverInicio(); // Regresa al buscador principal para que pueda intentar con otro ID
            return;
        }

        // Ocultar sección de búsqueda, rejilla, contador y HERO BANNER. Mostrar la sección de detalle
       
        document.getElementById("search-section").classList.add("d-none");
        //document.getElementById("hero-banner-section").classList.add("d-none"); // <-- NUEVO
        document.getElementById("movies-grid").classList.add("d-none");
        const counterContainer = document.getElementById("search-counter-container");

        if (counterContainer) counterContainer.classList.add("d-none");
        document.getElementById("movie-detail-section").classList.remove("d-none");


        const detailContent = document.getElementById("movie-detail-content");
        // Si no existe la imagen en OMDb ('N/A'), asignamos tu imagen por defecto
        const poster = pelicula.Poster !== "N/A" ? pelicula.Poster : "/frontend/static/imgs/poster-pelicula-kale.jpg";

        // Renderizamos toda la ficha técnica detallada adaptada de forma responsiva
        detailContent.innerHTML = `
            <div class="col-12 col-md-4 text-center">
                <!-- onerror captura el error 404 si la URL de la API falla al descargar -->
                <img src="${poster}" class="img-fluid rounded shadow mb-3 mb-md-0" alt="${pelicula.Title}" style="max-height: 450px; object-fit: cover;" onerror="this.onerror=null; this.src='/frontend/static/imgs/poster-no-disponible-temporalmente.jpg';">
            </div>
            <div class="col-12 col-md-8">
                <h2 class="fw-bold mb-2">${pelicula.Title} <span class="text-muted fs-4">(${pelicula.Year})</span></h2>
                
                <div class="d-flex flex-wrap gap-2 mb-3">
                    <span class="badge badge-kale-main">Tipo: ${pelicula.Type || 'N/A'}</span>
                    <span class="badge badge-kale-deep">Género: ${pelicula.Genre || 'N/A'}</span>
                    <span class="badge badge-slate">Clasificación: ${pelicula.Rated || 'N/A'}</span>
                    <span class="badge badge-charcoal">Duración: ${pelicula.Runtime || 'N/A'}</span>
                    <span class="badge badge-emerald">⭐ IMDb: ${pelicula.imdbRating || 'N/A'} (${pelicula.imdbVotes || '0'} votos)</span>
                    <span class="badge badge-emerald">IMDb: ${pelicula.imdbID || 'N/A'} </span>
                </div>

                <p class="mb-1 fw-normal"><strong>Director:</strong> <span class="fw-normal small">${pelicula.Director || 'N/A'}</span></p>
                <p class="mb-2 fw-normal"><strong>Guionista/s:</strong> <span class="fw-normal small">${pelicula.Writer || 'N/A'}</span></p>
                <p class="mb-2 fw-normal"><strong>Actores:</strong> <span class="fw-normal small">${pelicula.Actors || 'N/A'}</span></p>
                <p class="mb-2 fw-normal"><strong>Idioma:</strong> <span class="fw-normal small">${pelicula.Language || 'N/A'}</span></p>
                <p class="mb-2 fw-normal"><strong>Estreno:</strong> <span class="fw-normal small">${pelicula.Released || 'N/A'}</span> | <strong>País:</strong> <span class="fw-normal small">${pelicula.Country || 'N/A'}</span></p>
                
                <hr class="my-3">
                
                <h5 class="fw-bold text-dark">Sinopsis:</h5>
                <p class="small text-muted fst-italic fw-normal">${pelicula.Plot || 'Sin sinopsis disponible.'}</p>
                
                <hr class="my-3">
                
                <p class="small text-muted mb-1"><strong>Premios:</strong> <span class="fw-normal small">${pelicula.Awards || 'Ninguno'}</span></p>
                <p class="small text-muted mb-0"><strong>Taquilla (BoxOffice):</strong> <span class="fw-normal small">${pelicula.BoxOffice || 'N/A'}</span></p>
            </div>

        <!-- SECCIÓN DE CALIFICACIONES Y ESTRELLAS -->
            <div class="card bg-light border-0 p-3 mb-3 rounded-3 shadow-sm">
                <div class="row align-items-center">
                    <div class="col-12 col-md-6 mb-2 mb-md-0">
                        <h6 class="fw-bold text-dark mb-1">⭐ Valoración Media</h6>
                        <div id="promedio-estrellas-container" class="fs-5 text-warning fw-bold">
                                Cargando valoraciones...
                        </div>
                        </div>
                        <div class="col-12 col-md-6 text-md-end">
                        <h6 class="fw-bold text-dark mb-1">¡Valora esta película!</h6>
                        <div class="btn-group" role="group" aria-label="Calificación de estrellas">
                            <button type="button" class="btn btn-outline-warning btn-sm" onclick="calificarPelicula('${pelicula.imdbID}', 1)">1 ⭐</button>
                            <button type="button" class="btn btn-outline-warning btn-sm" onclick="calificarPelicula('${pelicula.imdbID}', 2)">2 ⭐</button>
                            <button type="button" class="btn btn-outline-warning btn-sm" onclick="calificarPelicula('${pelicula.imdbID}', 3)">3 ⭐</button>
                             <button type="button" class="btn btn-outline-warning btn-sm" onclick="calificarPelicula('${pelicula.imdbID}', 4)">4 ⭐</button>
                            <button type="button" class="btn btn-outline-warning btn-sm" onclick="calificarPelicula('${pelicula.imdbID}', 5)">5 ⭐</button>
                        </div>
                    </div>
                </div>
            </div>


        `;
    } catch (error) {
        console.error("Error al cargar detalle de la película:", error);
        mostrarAlerta("Hubo un error de conexión al consultar el ID de IMDb.");
        volverInicio();
        return;
    }

    // 2. Cargar comentarios de la película seleccionada
    cargarComentarios(imdbId);

    // Cargar calificaciones de la película seleccionada
    cargarCalificacionPromedio(imdbId);
}

async function cargarComentarios(imdbId) {
    try {
        const res = await fetch(`${API_URL}/comentarios/${imdbId}`);
        const comentarios = await res.json();

        const commentsList = document.getElementById("comments-list");
        commentsList.innerHTML = "";

        if (comentarios && comentarios.length > 0) {
            comentarios.forEach(c => {
                // c.persona contendrá el 'nombre_a_mostrar' gracias al JOIN del backend
                const item = document.createElement("div");
                item.className = "list-group-item list-group-item-action flex-column align-items-start mb-2 rounded shadow-sm";
                
                // Función que pinta los comentarios
                item.innerHTML = `
                    <div class="d-flex w-100 justify-content-between">
                        <h6 class="mb-1 text-kale fw-bold small">👤 ${c.persona || 'Anónimo'}</h6>
                        <small class="text-muted" style="font-size: 0.75rem;">${c.fecha || ''}</small>
                    </div>
                    <p class="mb-1 mt-1 small text-dark fw-normal">${c.comentario}</p>
                `;
                commentsList.appendChild(item);
            });
        } else {
            commentsList.innerHTML = `<p class="text-muted fst-italic small">Aún no hay comentarios para esta película. ¡Sé el primero en opinar!</p>`;
        }
    } catch (error) {
        console.error("Error al cargar comentarios:", error);
    }
}

async function enviarComentario() {
    const textoComentario = document.getElementById("texto-comentario").value.trim();
    const usernameActual = localStorage.getItem("usernameActual");

    if (!textoComentario) {
        mostrarAlerta("El comentario no puede estar vacío.");
        return;
    }

    if (!usernameActual) {
        mostrarAlerta("Debes iniciar sesión para comentar.");
        return;
    }

    try {
        // Enviamos el comentario usando el campo 'username' adaptado en el backend
        const response = await fetch(`${API_URL}/comentarios/${currentImdbId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: usernameActual,
                comentario: textoComentario
            })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById("texto-comentario").value = "";
            cargarComentarios(currentImdbId); // Recargamos la lista de comentarios
        } else {
            mostrarAlerta(data.detail || "Error al guardar el comentario.");
        }
    } catch (error) {
        console.error("Error de red al comentar:", error);
        mostrarAlerta("No se pudo enviar el comentario.");
    }
}

/* ==========================================
   NAVEGACIÓN Y CONTROL DE VISTAS
   ========================================== */

// Vuelve a la lista de resultados de la búsqueda actual (mantiene las tarjetas visibles)
function volverAResultados() {
    document.getElementById("movie-detail-section").classList.add("d-none");
    document.getElementById("search-section").classList.remove("d-none");
    document.getElementById("movies-grid").classList.remove("d-none");
    currentImdbId = null;

    // Limpiar el contador del total de películas encontradas en OMDb API
    // document.getElementById("search-counter-container").classList.add("d-none");
}

// Vuelve al inicio absoluto: limpia campos de búsqueda y vacía la rejilla
function volverInicio() {
    // 1. Ocultar sección de detalle y mostrar sección de búsqueda y rejilla
    document.getElementById("movie-detail-section").classList.add("d-none");
    document.getElementById("search-section").classList.remove("d-none");
    document.getElementById("movies-grid").classList.remove("d-none");
    document.getElementById("movies-grid").innerHTML = "";

    // 2. Limpiar la rejilla de resultados de películas y del contador del total de películas encontradas en OMDb API
    /*document.getElementById("movies-grid").innerHTML = "";
    document.getElementById("search-counter-container").classList.add("d-none");*/

    // 3. Limpiar los inputs de búsqueda de las tres pestañas pestañas
    const inputTitulo = document.getElementById("input-buscar-titulo");
    const inputTituloAnio = document.getElementById("input-buscar-titulo-anio");
    const inputAnio = document.getElementById("input-buscar-anio");
    const inputImdb = document.getElementById("input-buscar-imdb");

    if (inputTitulo) inputTitulo.value = "";
    if (inputTituloAnio) inputTituloAnio.value = "";
    if (inputAnio) inputAnio.value = "";
    if (inputImdb) inputImdb.value = "";

    /* Oculta de forma dinámica el cuadro indicador del total de resultados (el contador que te dice cuántas 
    películas se han encontrado en total en OMDb) cuando el usuario decide volver a la pantalla de inicio 
    o reiniciar su búsqueda. */

    // Busca el elemento que muestra cuántas películas se encontraron consumiendo la API de OMDb API
    const counterContainer = document.getElementById("search-counter-container");

    //con el if (counterContainer) me aseguro que el contenedor existe em la página donde se intenta modificar
    // counterContainer.classList.add("d-none") Usa la clase de Bootstrap 'd-none' para que elemento
    // se oculte visualmente por completo de la pantalla. 
    //if (counterContainer) counterContainer.classList.add("d-none");

    // 4. Restablecer el ID actual de la película seleccionada
    currentImdbId = null;
}


/* ==========================================
   LIMPIEZA Y GESTIÓN DE PESTAÑAS DE BÚSQUEDA
   ========================================== */

// Se detecta (escuchando evento) cuando el usuario cambia de pestaña de búsqueda para limpiar campos y resultados
document.addEventListener("DOMContentLoaded", () => {
    const tabTituloBtn = document.getElementById("tab-titulo");
    const tabAnioBtn = document.getElementById("tab-anio");
    const tabImdb = document.getElementById("tab-imdb");

    if (tabTituloBtn && tabAnioBtn && tabImdb) {
        tabTituloBtn.addEventListener("click", () => {
            limpiarCamposBusqueda('anio'); // Limpia los de año al ir a título
        });

        tabAnioBtn.addEventListener("click", () => {
            limpiarCamposBusqueda('titulo'); // Limpia el de título al ir a año
        });

        tabImdb.addEventListener("click", () => {
            limpiarCamposBusqueda('titulo'); // Limpia el IMDb ID al ir a ID
        });
    }
});

/*
function limpiarCamposBusqueda(origen) {
    const inputTitulo = document.getElementById("input-buscar-titulo");
    const inputTituloAnio = document.getElementById("input-buscar-titulo-anio");
    const inputAnio = document.getElementById("input-buscar-anio");
    const moviesGrid = document.getElementById("movies-grid");

    if (origen === 'titulo') {
        if (inputTitulo) inputTitulo.value = "";
    } else if (origen === 'anio') {
        if (inputTituloAnio) inputTituloAnio.value = "";
        if (inputAnio) inputAnio.value = "";
    }
    
    // Opcional: si quieres que al cambiar de pestaña también se limpien los resultados anteriores:
    // if (moviesGrid) moviesGrid.innerHTML = "";
}
*/

function limpiarOtrasPestañas(pestañaActiva) {
    const inputTitulo = document.getElementById("input-buscar-titulo");
    const inputTituloAnio = document.getElementById("input-buscar-titulo-anio");
    const inputAnio = document.getElementById("input-buscar-anio");
    const inputImdb = document.getElementById("input-buscar-imdb");

    // Si estás en Título, limpiamos Año e IMDb
    if (pestañaActiva === 'titulo') {
        if (inputTituloAnio) inputTituloAnio.value = "";
        if (inputAnio) inputAnio.value = "";
        if (inputImdb) inputImdb.value = "";
    }
    // Si estás en Título y Año, limpiamos Título e IMDb
    else if (pestañaActiva === 'anio') {
        if (inputTitulo) inputTitulo.value = "";
        if (inputImdb) inputImdb.value = "";
    }
    // Si estás en IMDb ID, limpiamos Título y los campos de Año
    else if (pestañaActiva === 'imdb') {
        if (inputTitulo) inputTitulo.value = "";
        if (inputTituloAnio) inputTituloAnio.value = "";
        if (inputAnio) inputAnio.value = "";
    }
}


/* ==========================================
   MOSTRAR ALERTAS PERSONALIZADAS CON BOOTSTRAP
   ========================================== */

// Función auxiliar para mostrar alertas personalizadas con botón "Aceptar"
// invocando el Modal de Bootstrap par que muestre un mensaje bonito y así 
// reemplazar el 'alert()' de Javascript

function mostrarAlerta(mensaje) {
    const mensajeEl = document.getElementById("custom-alert-message");
    if (mensajeEl) {
        mensajeEl.textContent = mensaje;
    }
    const modalEl = document.getElementById("customAlertModal");
    if (modalEl) {
        const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
        modal.show();
    } else {
        mostrarAlerta(mensaje); // Fallback por seguridad si el modal no estuviera cargado
    }
}



/*
// Función para cargar y pintar el promedio de calificaciones de la película
async function cargarCalificacionPromedio(imdbId) {
    const contenedor = document.getElementById("promedio-estrellas-container");
    if (!contenedor) return;

    try {
        const response = await fetch(`${API_URL}/calificaciones/${imdbId}/calificacion`);
        const data = await response.json();

        if (response.ok) {
            const estrellasVisuales = "⭐".repeat(Math.round(data.promedio)) || "Sin valoraciones";
            contenedor.innerHTML = `${data.promedio} / 5 ${estrellasVisuales} <span class="text-muted small">(${data.total_votos} votos)</span>`;
        } else {
            contenedor.innerHTML = "No disponible";
        }
    } catch (error) {
        console.error("Error al cargar la calificación:", error);
        contenedor.innerHTML = "Error al cargar";
    }
}
*/

// Función para cargar y pintar el promedio de calificaciones de la película
async function cargarCalificacionPromedio(imdbId) {
    const contenedor = document.getElementById("promedio-estrellas-container");
    if (!contenedor) return;

    try {
        const response = await fetch(`${API_URL}/calificaciones/${imdbId}/calificacion`);
        const data = await response.json();

        if (response.ok) {
            const notaRedondeada = Math.round(data.promedio);
            let estrellasHTML = "";

            if (notaRedondeada > 0) {
                // Generamos tantas estrellas rellenas de Bootstrap como indique el promedio
                for (let i = 0; i < notaRedondeada; i++) {
                    estrellasHTML += `<i class="bi bi-star-fill text-warning"></i> `;
                }
            } else {
                estrellasHTML = `<span class="text-muted small">Sin valoraciones</span>`;
            }

            contenedor.innerHTML = `${data.promedio} / 5 &nbsp; ${estrellasHTML} <span class="text-muted small">(${data.total_votos} votos)</span>`;
        } else {
            contenedor.innerHTML = "No disponible";
        }
    } catch (error) {
        console.error("Error al cargar la calificación:", error);
        contenedor.innerHTML = "Error al cargar";
    }
}





// Función para enviar la puntuación del usuario autenticado
async function calificarPelicula(imdbId, puntuacion) {
    // CORREGIDO: Leemos correctamente la clave "usernameActual" con la que guardas la sesión
    const usernameActual = localStorage.getItem('usernameActual');

    if (!usernameActual) {
        mostrarAlerta("Debes iniciar sesión para poder calificar una película.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/calificaciones/${imdbId}/calificar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: usernameActual,  // Enviamos el username correcto
                puntuacion: puntuacion
            })
        });

        const data = await response.json();

        if (response.ok) {
            mostrarAlerta(`¡Gracias por tu voto! Has calificado con ${puntuacion} estrellas.`);
            // Recargamos el promedio actualizado al instante
            cargarCalificacionPromedio(imdbId);
        } else {
            mostrarAlerta(data.detail || "Error al enviar la calificación.");
        }
    } catch (error) {
        console.error("Error de red al calificar:", error);
        mostrarAlerta("No se pudo conectar con el servidor para guardar la calificación.");
    }
}