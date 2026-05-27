from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.servei import Servei
from app.schemas.servei import ServeiResponse,ServeiCreate,ServeiUpdate

router = APIRouter()

#GET tots
@router.get("/serveis", response_model=list[ServeiResponse])
def obtenir_usuaris(db: Session = Depends(get_db)):
    servei = db.query(Servei).all()
    return servei

# GET un per id
@router.get("/serveis/{serveis_id}", response_model=ServeiResponse)
def obtenir_vehicle(serveis_id: int, db: Session = Depends(get_db)):
    serveiBuscar = db.query(Servei).filter(Servei.id == serveis_id).first()
    if not serveiBuscar:
        raise HTTPException(status_code=404, detail="Servei no trobat")
    return serveiBuscar

# POST crear
@router.post("/serveis", response_model=ServeiResponse, status_code=201)
def crear_vehicle(dades: ServeiCreate, db: Session = Depends(get_db)):
    
    servei = Servei(**dades.model_dump())
    db.add(servei)
    db.commit()
    db.refresh(servei)
    return servei

# PUT actualitzar
@router.put("/serveis/{servei_id}", response_model=ServeiResponse)
def actualitzar_vehicle(servei_id: int, dades: ServeiUpdate, db: Session = Depends(get_db)):
    vehicle = db.query(Servei).filter(Servei.id == servei_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="servei no trobat")
    
    # Només actualitza els camps que s'envien
    for camp, valor in dades.model_dump(exclude_unset=True).items():
        setattr(vehicle, camp, valor)
    
    db.commit()
    db.refresh(vehicle)
    return vehicle

# DELETE eliminar
@router.delete("/serveis/{servei_id}", status_code=204)
def eliminar_vehicle(servei_id: int, db: Session = Depends(get_db)):
    servei = db.query(Servei).filter(Servei.id == servei_id).first()
    if not servei:
        raise HTTPException(status_code=404, detail="serveu no trobat")
    
    db.delete(servei)
    db.commit()