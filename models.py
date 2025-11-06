
# Refleja la tabla existente usuarios en tu base MySQL:


from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base  # o como lo tengas importado

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    apellidos = Column(String(100))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)