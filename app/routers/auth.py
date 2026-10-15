#Gestión de usuarios y login

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.model import MovieModel

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios y Autenticación"])
movie_model = MovieModel()

class UsuarioRequest(BaseModel):
    nombre: str
    password: str

@router.post("/login-o-registrar")
def login_o_registrar(data: UsuarioRequest):
    """
    Gestiona el flujo seguro de usuario aplicando la validación estricta y normalización:
    - Valida que no estén vacíos.
    - Normaliza el nombre.
    - Verifica contraseña si existe, o lo registra si es nuevo.
    """
    if not data.nombre.strip() or not data.password.strip():
        raise HTTPException(status_code=400, detail="El usuario y la contraseña no pueden estar vacíos.")

    nombre_limpio = " ".join(data.nombre.strip().split()).title()
    usuario_db = movie_model.buscar_usuario(nombre_limpio)
    
    if usuario_db:
        if movie_model.verificar_password(nombre_limpio, data.password):
            return {
                "status": "success", 
                "mensaje": f"Acceso concedido. Bienvenido de nuevo, {nombre_limpio}", 
                "usuario": nombre_limpio
            }
        else:
            raise HTTPException(status_code=400, detail="Contraseña incorrecta. Inténtalo de nuevo.")
    else:
        exito = movie_model.registrar_usuario(nombre_limpio, data.password)
        if exito:
            return {
                "status": "success", 
                "mensaje": f"Usuario '{nombre_limpio}' creado y registrado con éxito.", 
                "usuario": nombre_limpio
            }
        else:
            raise HTTPException(status_code=500, detail="Hubo un error al registrar el usuario en la base de datos.")