# Gestión de usuarios: Login y Registro separados

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.model import MovieModel

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios y Autenticación"])
movie_model = MovieModel()

# Esquema exclusivo para el Login
class LoginRequest(BaseModel):
    username: str
    password: str

# Esquema exclusivo para el Registro
class RegistroRequest(BaseModel):
    username: str
    nombre_a_mostrar: str
    password: str


@router.post("/login")
def login_usuario(data: LoginRequest):
    """
    Autentica a un usuario existente mediante su 'username' y 'password'.
    Si las credenciales son correctas, permite el acceso para comentar.
    """
    if not data.username.strip() or not data.password.strip():
        raise HTTPException(status_code=400, detail="El usuario y la contraseña no pueden estar vacíos.")

    username_limpio = data.username.strip().lower()

    # Buscamos si el usuario existe
    usuario_db = movie_model.buscar_usuario_por_username(username_limpio)
    
    if not usuario_db:
        raise HTTPException(status_code=404, detail="El usuario no existe. Por favor, regístrate primero.")

    # Verificamos la contraseña
    if movie_model.verificar_password(username_limpio, data.password):
        return {
            "status": "success",
            "mensaje": f"¡Bienvenido de nuevo, {usuario_db['nombre_a_mostrar']}!",
            "usuario": usuario_db['nombre_a_mostrar'],
            "username": usuario_db['username']
        }
    else:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta. Inténtalo de nuevo.")


@router.post("/registrar")
def registrar_usuario(data: RegistroRequest):
    """
    Registra un nuevo usuario en la base de datos si el 'username' no está en uso.
    """
    if not data.username.strip() or not data.nombre_a_mostrar.strip() or not data.password.strip():
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios.")

    username_limpio = data.username.strip().lower()
    nombre_mostrar_limpio = " ".join(data.nombre_a_mostrar.strip().split())

    # Comprobamos si el username ya está ocupado
    usuario_existente = movie_model.buscar_usuario_por_username(username_limpio)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El nombre de usuario (username) ya está registrado. Elige otro.")

    # Registramos el nuevo usuario
    exito = movie_model.registrar_usuario(username_limpio, nombre_mostrar_limpio, data.password)
    
    if exito:
        return {
            "status": "success",
            "mensaje": f"Usuario '{nombre_mostrar_limpio}' registrado con éxito. Ya puedes iniciar sesión.",
            "usuario": nombre_mostrar_limpio,
            "username": username_limpio
        }
    else:
        raise HTTPException(status_code=500, detail="Hubo un error al registrar el usuario en la base de datos.")