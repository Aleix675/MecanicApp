from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base
import enum

class RolUsuari(enum.Enum):
    CLIENT = "CLIENT"
    MECANIC = "MECANIC"
    ADMIN = "ADMIN"

#Base es la clase especial de SQLAlchemy que convierte tus clases Python en tablas ORM.

class Usuari(Base):
    __tablename__ = "usuari"

    id = Column(Integer, primary_key=True, index=True) #index crea indice para acelerar busqueda
    nom = Column(String(100), nullable=False)# nullable = obligatorio
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    telefon = Column(String(20))
    rol = Column(
    SAEnum(RolUsuari, name="rol_usuari", native_enum=False),
    nullable=False
    )
    actiu = Column(Boolean, default=True)
    creat_el = Column(DateTime, server_default=func.now())

    vehicles = relationship("Vehicle", back_populates="usuari")
    cites_mecanic = relationship("Cita", back_populates="mecanic" ,foreign_keys="Cita.mecanic_id")

#En SQL puro Para obtener vehículos de un usuario:
#SELECT * FROM vehicle WHERE usuari_id = 1;
#Con relationship Puedes hacer: usuari.vehicles
#y SQLAlchemy hace el SQL automáticamente.