

# Define los modelos de datos (lo que se recibe/envía en JSON):
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



class User(BaseModel):
    nombre: str
    apellidos: str
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    nombre: str
    apellidos: str
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    nombre: str
    apellidos: str
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None