from pydantic import BaseModel

#api
class ServeiResponse(BaseModel):

    id : int
    nom : str
    descripcio : str
    duracio_base_min : int
    duracio_suv_min : int
    preu_orientatiu : float
    actiu : bool
    
    class Config:
        from_attributes = True

#update
class ServeiUpdate(BaseModel):
    nom : str | None = None
    descripcio : str | None = None
    duracio_base_min : int | None = None
    duracio_suv_min : int | None = None
    preu_orientatiu : float | None = None
    actiu : bool | None = None

#crear
class ServeiCreate(BaseModel):
    nom : str
    descripcio : str
    duracio_base_min : int
    duracio_suv_min : int
    preu_orientatiu : float
    actiu : bool