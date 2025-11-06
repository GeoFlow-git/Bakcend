
# Conexión al servidor MySQL :

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv # para leer automáticamente el archivo .env y construir la conexión.              

# Carga el archivo .env
load_dotenv()

# ⚙️ Datos de conexión a MySQL
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# ==========================
# 🔹 Notas
# ==========================
# DATABASE_URL = os.getenv("DATABASE_URL")
# engine = create_engine(DATABASE_URL)
# 1. En desarrollo local, puedes usar DB_USER, DB_PASSWORD, etc. por separado.
# 2. En producción (Railway, Heroku), generalmente te pedirán DATABASE_URL.
# 3. Nunca subas este archivo a GitHub con tus credenciales reales.




# aqui usamos   PyMsql     

# "mysql+pymysql://..." significa:  usar MySQL con el driver PyMySQL para conectarse.
# SQLAlchemy delega la conexión real a PyMySQL, que implementa el protocolo de comunicación con el servidor MySQL.
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# Crear el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# # Dependencia para obtener sesión
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
