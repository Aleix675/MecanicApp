from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.usuari import Usuari
from app.schemas.usuari import UsuariResponse,UsuariCrear,UsuariUpdate
#endoints protegits per token jwt
from app.security.dependencies import get_usuari_actual,requerir_admin

router = APIRouter()

#Nomes admin pot veure tots els usuaris
@router.get("/usuaris", response_model=list[UsuariResponse])
def obtenir_usuaris( db: Session = Depends(get_db),usuari_actual : Usuari = Depends(requerir_admin) ):
    return db.query(Usuari).all()

# GET un per id
@router.get("/usuaris/{usuari_id}", response_model=UsuariResponse)
def obtenir_vehicle(usuari_id: int, db: Session = Depends(get_db)):
    usuari = db.query(Usuari).filter(Usuari.id == usuari_id).first()
    if not usuari:
        raise HTTPException(status_code=404, detail="usuari no trobat")
    return usuari

# Qualsevol autenticat pot veure el seu propi perfil
@router.get("/usuaris/me", response_model=UsuariResponse)
def obtenir_perfil(usuari_actual: Usuari = Depends(get_usuari_actual)):
    return usuari_actual

@router.post("/usuaris", response_model=UsuariResponse, status_code=201)
def crear_usuari(dades: UsuariCrear, db: Session = Depends(get_db), usuari_actual: Usuari = Depends(requerir_admin)):
    existent = db.query(Usuari).filter(Usuari.email == dades.email).first()
    if existent:
        raise HTTPException(status_code=400, detail="Ja existeix un usuari amb aquest email")
    
    user = Usuari(**dades.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# PUT actualitzar
@router.put("/usuaris/{usuari_id}", response_model=UsuariResponse)
def actualitzar_vehicle(usuari_id: int, dades: UsuariUpdate, db: Session = Depends(get_db)):
    user = db.query(Usuari).filter(Usuari.id == usuari_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="usuari no trobat")
    
    # Només actualitza els camps que s'envien
    for camp, valor in dades.model_dump(exclude_unset=True).items():
        setattr(user, camp, valor)
    
    db.commit()
    db.refresh(user)
    return user

# DELETE eliminar
@router.delete("/usuaris/{usuari_id}", status_code=204)
def eliminar_vehicle(usuari_id: int, db: Session = Depends(get_db)):
    user = db.query(Usuari).filter(Usuari.id == usuari_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="usuari no trobat")
    
    db.delete(user)
    db.commit()