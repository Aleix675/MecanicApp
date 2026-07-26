import os
from dotenv import load_dotenv

from fastapi import FastAPI
from app.database.connection import engine
from app.database import base, connection

from fastapi.middleware.cors import CORSMiddleware

# Importar models EN AQUEST ORDRE EXACTE
from app.models.usuari import Usuari
from app.models.servei import Servei
from app.models.vehicle import Vehicle
from app.models.cita import Cita
from app.models.nota_tecnica import NotaTecnica
from app.routers import usuaris,serveis,vehicles,cites,auth,admin,notes

from sqlalchemy.orm import Session

#INICIAR APP -->dins de backend -->[   python -m uvicorn app.main:app --reload    ]<--

# Cargar las variables de entorno (.env)
load_dotenv()

app = FastAPI(
    title="MecànicApp API",
    description="API REST per a gestió de taller mecànic",
    version="1.0.0",
    docs_url="/docs",      
    redoc_url="/redoc"     
)

# 1. Definir los orígenes locales por defecto (siempre se van a usar en desarrollo)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

# 2. Leer la URL del frontend en producción desde el .env si existe
frontend_prod_url = os.getenv("FRONTEND_URL")
if frontend_prod_url:
    origins.append(frontend_prod_url)

# 3. Aplicar el middleware con la lista dinámica
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(usuaris.router)
app.include_router(vehicles.router)
app.include_router(serveis.router)
app.include_router(cites.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"missatge": "MecànicApp API funcionant!"}
