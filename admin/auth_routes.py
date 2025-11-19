from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import AdminUser
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import os
from passlib.context import CryptContext

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    user: dict
    subscription: dict
    token: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Autenticación de usuario"""
    try:
        # Por ahora, usar credenciales de prueba
        # TODO: Implementar autenticación real con base de datos
        
        if request.email == "admin@ventas.com" and request.password == "admin123":
            token = create_access_token({"sub": request.email, "role": "admin"})
            
            return {
                "success": True,
                "user": {
                    "id": 1,
                    "email": request.email,
                    "name": "Administrador",
                    "role": "admin"
                },
                "subscription": {
                    "type": "Premium",
                    "hasAccess": True,
                    "daysLeft": 30
                },
                "token": token
            }
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error en el servidor"
        )

@router.post("/logout")
async def logout():
    """Cerrar sesión"""
    return {"success": True, "message": "Sesión cerrada"}

@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Obtener usuario actual"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        return {
            "success": True,
            "user": {
                "email": email,
                "name": "Administrador",
                "role": payload.get("role", "user")
            }
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str = None
    phone: str = None
    businessName: str = None

@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Registro de nuevo usuario"""
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(AdminUser).filter(AdminUser.email == request.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear nuevo usuario
        hashed_password = get_password_hash(request.password)
        new_user = AdminUser(
            email=request.email,
            password=hashed_password,
            name=request.name,
            phone=request.phone,
            business_name=request.businessName,
            created_at=datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Generar token
        token = create_access_token({"sub": new_user.email, "role": "user"})
        
        return {
            "success": True,
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "name": new_user.name,
                "role": "user"
            },
            "token": token,
            "requiresVerification": False
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error en registro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear usuario"
        )

class ForgotPasswordRequest(BaseModel):
    email: str

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Solicitar recuperación de contraseña"""
    try:
        user = db.query(AdminUser).filter(AdminUser.email == request.email).first()
        if not user:
            # Por seguridad, no revelar si el email existe
            return {"success": True, "message": "Si el email existe, recibirás instrucciones"}
        
        # TODO: Generar código y enviar email
        # Por ahora solo retornar éxito
        return {"success": True, "message": "Código enviado al email"}
    except Exception as e:
        print(f"Error en forgot-password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar solicitud"
        )

class ResetPasswordRequest(BaseModel):
    email: str
    code: str
    newPassword: str

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Resetear contraseña con código"""
    try:
        user = db.query(AdminUser).filter(AdminUser.email == request.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # TODO: Verificar código
        # Por ahora solo actualizar contraseña
        user.password = get_password_hash(request.newPassword)
        db.commit()
        
        return {"success": True, "message": "Contraseña actualizada"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error en reset-password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al resetear contraseña"
        )
