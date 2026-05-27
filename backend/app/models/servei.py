from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text
from app.database.base import Base

class Servei(Base):
    __tablename__ = "servei"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    descripcio = Column(Text)
    duracio_base_min = Column(Integer, nullable=False)
    duracio_suv_min = Column(Integer, nullable=False)
    preu_orientatiu = Column(Numeric(10, 2))
    actiu = Column(Boolean, default=True)