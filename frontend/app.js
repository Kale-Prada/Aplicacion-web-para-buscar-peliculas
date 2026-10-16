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
    alert("Has cerrado sesión correctamente.");
}


/* ==========================================
   2. AUTENTICACIÓN Y REGISTRO (Endpoints separados)
   ========================================== */

async function ejecutarLogin() {
    const usernameInput = document.getElementById("login-username").value.trim();
    const passwordInput = document.getElementById("login-password").value.trim();

    if (!usernameInput || !passwordInput) {
        alert("Por favor, rellena todos los campos.");
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
            alert(data.mensaje);
        } else {
            alert(data.detail || "Error al iniciar sesión.");
        }
    } catch (error) {
        console.error("Error de red en login:", error);
        alert("No se pudo conectar con el servidor.");
    }
}

async function ejecutarRegistro() {
    const usernameInput = document.getElementById("reg-username").value.trim();
    const nombreMostrarInput = document.getElementById("reg-nombre").value.trim();
    const passwordInput = document.getElementById("reg-password").value.trim();

    if (!usernameInput || !nombreMostrarInput || !passwordInput) {
        alert("Todos los campos son obligatorios.");
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
            alert(data.mensaje);
            // Cerramos el modal de registro
            const modalEl = document.getElementById("registroModal");
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.hide();
        } else {
            alert(data.detail || "Error en el registro.");
        }
    } catch (error) {
        console.error("Error de red en registro:", error);
        alert("No se pudo conectar con el servidor.");
    }
}


/* ==========================================
   3. BÚSQUEDA DE PELÍCULAS (Ajustado a /buscar?titulo=...)
   ========================================== */

async function buscarPeliculas() {
    const query = document.getElementById("input-buscar").value.trim();
    if (!query) {
        alert("Introduce un título para buscar.");
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
                const poster = pelicula.Poster !== "N/A" ? pelicula.Poster : "https://via.placeholder.com/300x450?text=Sin+Imagen";
                
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
        alert("Hubo un error al realizar la búsqueda.");
    }
}

/* ==========================================
   4. BÚSQUEDA DE PELÍCULAS (Título / Título y Año)
   ========================================== */

async function buscarPeliculasPorTitulo() {
    const query = document.getElementById("input-buscar-titulo").value.trim();
    if (!query) {
        alert("Introduce un título para buscar.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/peliculas/buscar?titulo=${encodeURIComponent(query)}`);
        const data = await response.json();
        renderizarResultados(data);
    } catch (error) {
        console.error("Error al buscar películas:", error);
        alert("Hubo un error al realizar la búsqueda.");
    }
}

async function buscarPeliculasPorTituloYAnio() {
    const titulo = document.getElementById("input-buscar-titulo-anio").value.trim();
    const year = document.getElementById("input-buscar-anio").value.trim();

    if (!titulo || !year) {
        alert("Debes indicar tanto el título como el año de la película.");
        return;
    }

    try {
        // Conectamos con tu endpoint existente: /api/peliculas/buscar-por-anio?titulo=...&year=...
        const response = await fetch(`${API_URL}/peliculas/buscar-por-anio?titulo=${encodeURIComponent(titulo)}&year=${encodeURIComponent(year)}`);
        const data = await response.json();
        renderizarResultados(data);
    } catch (error) {
        console.error("Error al buscar por título y año:", error);
        alert("No se encontraron películas con esos criterios o hubo un error en la red.");
    }
}

// Función auxiliar para pintar las tarjetas de películas de forma limpia (DRY)
function renderizarResultados(data) {
    const moviesGrid = document.getElementById("movies-grid");
    moviesGrid.innerHTML = "";

    if (data.Search && Array.isArray(data.Search)) {
        data.Search.forEach(pelicula => {
            const poster = pelicula.Poster !== "N/A" ? pelicula.Poster : "https://via.placeholder.com/300x450?text=Sin+Imagen";
            
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
        moviesGrid.innerHTML = `<div class="col-12 text-center"><p class="text-muted">No se encontraron películas que coincidan con los criterios de búsqueda.</p></div>`;
    }
}


/* ==========================================
   5. DETALLE DE PELÍCULA Y COMENTARIOS (Ajustado a /detalle/{id})
   ========================================== */

let currentImdbId = null;

async function verDetallePelicula(imdbId) {
    currentImdbId = imdbId;

    // Ocultar sección de búsqueda y mostrar detalle
    document.getElementById("search-section").classList.add("d-none");
    document.getElementById("movies-grid").classList.add("d-none");
    document.getElementById("movie-detail-section").classList.remove("d-none");

    // 1. Obtener detalles de la película
    try {
        const resDetalle = await fetch(`${API_URL}/peliculas/detalle/${imdbId}`);
        const pelicula = await resDetalle.json();

        const detailContent = document.getElementById("movie-detail-content");
        const poster = pelicula.Poster !== "N/A" ? pelicula.Poster : "https://via.placeholder.com/300x450?text=Sin+Imagen";

        detailContent.innerHTML = `
            <div class="col-md-4 text-center">
                <img src="${poster}" class="img-fluid rounded shadow" alt="${pelicula.Title}">
            </div>
            <div class="col-md-8">
                <h2>${pelicula.Title} (${pelicula.Year})</h2>
                <p><strong>Director:</strong> ${pelicula.Director}</p>
                <p><strong>Género:</strong> ${pelicula.Genre}</p>
                <p><strong>Actores:</strong> ${pelicula.Actors}</p>
                <hr>
                <p><strong>Sinopsis:</strong> ${pelicula.Plot}</p>
            </div>
        `;
    } catch (error) {
        console.error("Error al cargar detalle:", error);
    }

    // 2. Cargar comentarios de la película
    cargarComentarios(imdbId);
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
                item.innerHTML = `
                    <div class="d-flex w-100 justify-content-between">
                        <h6 class="mb-1 text-primary fw-bold">👤 ${c.persona || 'Anónimo'}</h6>
                        <small class="text-muted">${c.fecha || ''}</small>
                    </div>
                    <p class="mb-1 mt-2">${c.comentario}</p>
                `;
                commentsList.appendChild(item);
            });
        } else {
            commentsList.innerHTML = `<p class="text-muted fst-italic">Aún no hay comentarios para esta película. ¡Sé el primero en opinar!</p>`;
        }
    } catch (error) {
        console.error("Error al cargar comentarios:", error);
    }
}

async function enviarComentario() {
    const textoComentario = document.getElementById("texto-comentario").value.trim();
    const usernameActual = localStorage.getItem("usernameActual");

    if (!textoComentario) {
        alert("El comentario no puede estar vacío.");
        return;
    }

    if (!usernameActual) {
        alert("Debes iniciar sesión para comentar.");
        return;
    }

    try {
        // Enviamos el comentario usando el campo 'username' adaptado en tu backend
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
            alert(data.detail || "Error al guardar el comentario.");
        }
    } catch (error) {
        console.error("Error de red al comentar:", error);
        alert("No se pudo enviar el comentario.");
    }
}

function volverInicio() {
    document.getElementById("movie-detail-section").classList.add("d-none");
    document.getElementById("search-section").classList.remove("d-none");
    document.getElementById("movies-grid").classList.remove("d-none");
    currentImdbId = null;
}