from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Vehicle(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True, index=True)
    usuari_id = Column(Integer, ForeignKey("usuari.id", ondelete="CASCADE"), nullable=False)
    marca = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    any_fabricacio = Column(Integer)
    matricula = Column(String(20), unique=True, nullable=False)
    tipus = Column(String(50))

    usuari = relationship("Usuari", back_populates="vehicles")
    cites = relationship("Cita", back_populates="vehicle")