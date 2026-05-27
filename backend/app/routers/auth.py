from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.usuari import Usuari, RolUsuari
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.security.hashing import hash_password, verify_password
from app.security.jwt_handler import crear_token

router = APIRouter(prefix="/auth")

@router.post("/register", status_code=201)
def register(dades: RegisterRequest, db: Session = Depends(get_db)):
    existent = db.query(Usuari).filter(Usuari.email == dades.email).first()
    if existent:
        raise HTTPException(status_code=400, detail="Aquest email ja està registrat")
    
    usuari = Usuari(
        nom=dades.nom,
        email=dades.email,
        password_hash=hash_password(dades.password),
        telefon=dades.telefon,
        rol=RolUsuari.CLIENT
    )
    db.add(usuari)
    db.commit()
    db.refresh(usuari)
    return {"missatge": "Usuari registrat correctament", "id": usuari.id}

@router.post("/login", response_model=TokenResponse)
def login(dades: LoginRequest, db: Session = Depends(get_db)):
    usuari = db.query(Usuari).filter(Usuari.email == dades.email).first()
    if not usuari or not verify_password(dades.password, usuari.password_hash):
        raise HTTPException(status_code=401, detail="Email o contrasenya incorrectes")
    
    token = crear_token({"sub": str(usuari.id), "rol": usuari.rol.value})
    return {
        "access_token": token,
        "token_type": "bearer",
        "rol": usuari.rol.value,
        "nom": usuari.nom,
        "id" : usuari.id
    }