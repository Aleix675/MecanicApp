import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Cargar las variables de entorno del archivo .env creado por Render
load_dotenv()

# 2. Obtener la URL de forma segura (sin escribirla aquí)
# Si estás en local usará tu .env local, si estás en Render usará su Secret File
DATABASE_URL = os.getenv("DATABASE_URL")

# Control de errores por seguridad
if not DATABASE_URL:
    raise ValueError("Error: La variable de entorno DATABASE_URL no está configurada.")

# 3. Configurar SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()