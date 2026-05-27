from pydantic import BaseModel
from datetime import datetime

class NotaCreate(BaseModel):
    contingut: str

class NotaResponse(BaseModel):
    id: int
    cita_id: int
    mecanic_id: int
    contingut: str
    creat_el: datetime

    class Config:
        from_attributes = True