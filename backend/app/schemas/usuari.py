from pydantic import BaseModel
from datetime import datetime

#Els schemas defineixen l'estructura de les dades que entren i surten de l'API. 
#Utilitzen Pydantic per validar les dades i serialitzar els objectes dels models.

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