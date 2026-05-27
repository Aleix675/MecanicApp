from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class NotaTecnica(Base):
    __tablename__ = "nota_tecnica"

    id = Column(Integer, primary_key=True, index=True)
    cita_id = Column(Integer, ForeignKey("cita.id", ondelete="CASCADE"), nullable=False)
    mecanic_id = Column(Integer, ForeignKey("usuari.id"), nullable=False)
    contingut = Column(Text, nullable=False)
    creat_el = Column(DateTime, server_default=func.now())

    cita = relationship("Cita", back_populates="notes")
    mecanic = relationship("Usuari", foreign_keys=[mecanic_id])