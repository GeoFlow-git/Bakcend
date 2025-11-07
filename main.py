from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar las rutas
from routes.auth import router as auth_router

# uvicorn main:app --reload

app = FastAPI(title="GeoFlow API - Login")

# =============================
# 🔒 CONFIGURAR CORS
# =============================
# Esto permite que tu frontend (por ejemplo React o GitHub Pages)
# pueda hacer solicitudes a tu backend.
# Cuando tengas tu dominio o URL final, cámbialo en "allow_origins".
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # para desarrollo local (Vite)
        "https://geoflow-git.github.io/GeoFlow-website",  # cuando publiques en GitHub Pages
        "https://geoflow-git.github.io",  #    cuando el backend este subido a railway.
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# 🚀 INCLUIR LAS RUTAS
# =============================
# Incluimos las rutas del archivo routes/auth.py
app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
# tags=["Autenticación"] = Ayuda a organizar los endpoints en Swagger (/docs).


# =============================
# 🧩 ENDPOINT PRINCIPAL (TEST)
# =============================
@app.get("/")
def root():
    return {"message": "API de GeoFlow funcionando correctamente 🚀"}
