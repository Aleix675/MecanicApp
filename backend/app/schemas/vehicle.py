from pydantic import BaseModel,ConfigDict
from typing import Optional

# Per CREAR un vehicle (el client envia això)
class VehicleCreate(BaseModel):
    usuari_id: int
    marca: str
    model: str
    any_fabricacio: int | None
    matricula: str
    tipus: str | None

# Per ACTUALITZAR (tots els camps opcionals)
class VehicleUpdate(BaseModel):
    marca: str | None = None
    model: str | None = None
    any_fabricacio: int | None = None
    matricula: str | None = None
    tipus: str | None = None

# Per RESPONDRE (el que retorna l'API)
class VehicleResponse(BaseModel):
    # Esto sobreescribe cualquier conflicto y obliga a FastAPI/Pydantic v2
    # a mapear los objetos de SQLAlchemy correctamente.
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuari_id: int
    marca: str
    model: str
    any_fabricacio: Optional[int] = None
    matricula: str
    tipus: Optional[str] = None
