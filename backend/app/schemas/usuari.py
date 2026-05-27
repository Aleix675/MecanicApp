from pydantic import BaseModel
from datetime import datetime

class UsuariResponse(BaseModel):
    id:int
    nom:str
    email:str
    telefon:str | None
    rol:str
    actiu:bool
    creat_el: datetime

    class Config:
        from_attributes = True

#update
class UsuariUpdate(BaseModel):
    nom:str | None = None
    email:str | None = None
    telefon:str | None = None
    rol:str | None = None
    actiu:bool | None = None


#crear
class UsuariCrear(BaseModel):
    nom:str
    email:str
    telefon:str | None
    rol:str
    actiu:bool
    creat_el: datetime