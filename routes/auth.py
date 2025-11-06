from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, UserLogin, UserUpdate
from utils.auth_utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    verify_token, # función que decodifica JWT y retorna username
)

from fastapi.security import OAuth2PasswordBearer


#from datetime import timedelta
from passlib.context import CryptContext


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependencia para obtener una sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario o email ya existen
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario o correo ya están registrados."
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        nombre=user.nombre,
        apellidos=user.apellidos,
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "Usuario registrado exitosamente", "username": user.username}



@router.post("/login")
def login(usuario: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == usuario.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    if not pwd_context.verify(usuario.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Crear JWT
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}







@router.get("/me")
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    return {
        "username": user.username,
        "nombre": user.nombre,
        "apellidos": user.apellidos,
        "email": user.email,
    }



@router.put("/update")
def update_user(
    user_data: UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Obtenemos db dentro de verify_token automáticamente
    current_user = verify_token(token, db) 
    # db = next(get_db())  # ✅ Crea una sesión local aquí si la necesitas luego

    if not current_user:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    if user_data.nombre:
        current_user.nombre = user_data.nombre
    if user_data.apellidos:
        current_user.apellidos = user_data.apellidos
    if user_data.email:
        current_user.email = user_data.email

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Usuario actualizado exitosamente",
        "usuario": {
            "nombre": current_user.nombre,
            "apellidos": current_user.apellidos,
            "username": current_user.username,
            "email": current_user.email
        }
    }