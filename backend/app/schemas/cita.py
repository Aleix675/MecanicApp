from pydantic import BaseModel, field_validator
from datetime import datetime

class CitaCreate(BaseModel):
    vehicle_id: int
    servei_id: int
    data_hora_inici: datetime
    observacions_client: str | None = None

class CitaUpdate(BaseModel):
    data_hora_inici: datetime | None = None
    data_hora_fi: datetime | None = None
    estat: str | None = None
    observacions_client: str | None = None
    preu_final: float | None = None

class CitaResponse(BaseModel):
    id: int
    vehicle_id: int
    servei_id: int
    mecanic_id: int
    data_hora_inici: datetime
    data_hora_fi: datetime
    estat: str
    observacions_client: str | None
    preu_final: float | None
    creat_el: datetime

    @field_validator('estat', mode='before')
    @classmethod
    def estat_to_str(cls, v):
        if hasattr(v, 'value'):
            return v.value
        return v

    class Config:
        from_attributes = True

class DisponibilitatRequest(BaseModel):
    servei_id: int
    data_hora_inici: datetime
    tipus_vehicle: str | None = "TURISME"