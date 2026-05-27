from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, Text, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base
import enum

class EstatCita(enum.Enum):
    PENDENT = "PENDENT"
    CONFIRMADA = "CONFIRMADA"
    EN_PROCES = "EN_PROCES"
    COMPLETADA = "COMPLETADA"
    CANCELADA = "CANCELADA"

class Cita(Base):
    __tablename__ = "cita"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicle.id", ondelete="CASCADE"), nullable=False)
    servei_id = Column(Integer, ForeignKey("servei.id"), nullable=False)
    mecanic_id = Column(Integer, ForeignKey("usuari.id"), nullable=False)
    data_hora_inici = Column(DateTime, nullable=False)
    data_hora_fi = Column(DateTime, nullable=False)
    estat = Column(
    SAEnum(EstatCita, name="estat_cita", native_enum=False),
    default=EstatCita.PENDENT
    )
    observacions_client = Column(Text)
    preu_final = Column(Numeric(10, 2))
    creat_el = Column(DateTime, server_default=func.now())

    vehicle = relationship("Vehicle", back_populates="cites")
    servei = relationship("Servei")
    mecanic = relationship("Usuari", back_populates="cites_mecanic" ,foreign_keys=[mecanic_id])
    notes = relationship("NotaTecnica", back_populates="cita")