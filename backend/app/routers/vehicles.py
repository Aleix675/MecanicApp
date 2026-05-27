from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.vehicle import Vehicle
from app.models.usuari import Usuari,RolUsuari
from app.schemas.vehicle import VehicleResponse,VehicleCreate,VehicleUpdate

#seguretat endpoints
from app.security.dependencies import get_usuari_actual,requerir_admin
router = APIRouter()

#ENDPOPINTS GENERICS ULTIMS ELS ESPECIFICS PRIMER SINO DONA ERROR
# GET vehicles propis — qualsevol client autenticat
@router.get("/vehicles/meus", response_model=list[VehicleResponse])
def obtenir_vehicles_meus(
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(get_usuari_actual)
):
    return db.query(Vehicle).filter(Vehicle.usuari_id == usuari_actual.id).all()

# GET tots
#@router.get("/vehicles", response_model=list[VehicleResponse])
#def obtenir_vehicles(db: Session = Depends(get_db), usuari_actual: Usuari = Depends(requerir_admin)):
#    return db.query(Vehicle).all()



# POST crear
@router.post("/vehicles", response_model=VehicleResponse, status_code=201)
def crear_vehicle(dades: VehicleCreate, db: Session = Depends(get_db), usuari_actual : Usuari = Depends(get_usuari_actual)):
    # Comprovar matrícula duplicada
    existent = db.query(Vehicle).filter(Vehicle.matricula == dades.matricula).first()
    if existent:
        raise HTTPException(status_code=400, detail="Ja existeix un vehicle amb aquesta matrícula")
    
    vehicle = Vehicle(**dades.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle

# PUT actualitzar
@router.put("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def actualitzar_vehicle(vehicle_id: int, dades: VehicleUpdate, db: Session = Depends(get_db)):
    
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle no trobat")
    
    # Només actualitza els camps que s'envien
    for camp, valor in dades.model_dump(exclude_unset=True).items():
        setattr(vehicle, camp, valor)
    
    db.commit()
    db.refresh(vehicle)
    return vehicle

# DELETE eliminar
@router.delete("/vehicles/{vehicle_id}", status_code=204)
def eliminar_vehicle(vehicle_id: int, db: Session = Depends(get_db), usuari_actual : Usuari = Depends(get_usuari_actual)):
    
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle no trobat")
    
    es_propietari = vehicle.usuari_id == usuari_actual.id
   
    if usuari_actual.rol == RolUsuari.ADMIN or es_propietari:
        db.delete(vehicle)
        db.commit()
    else:
        raise HTTPException(status_code=403, detail="usuari sense permisos")
