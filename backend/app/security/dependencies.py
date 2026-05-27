from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.security.jwt_handler import verificar_token
from app.models.usuari import Usuari, RolUsuari

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_usuari_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuari:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invàlid o expirat",
        headers={"WWW-Authenticate": "Bearer"}
    )
    payload = verificar_token(token)
    if not payload:
        raise credentials_error
    
    usuari_id = payload.get("sub")
    if not usuari_id:
        raise credentials_error
    
    usuari = db.query(Usuari).filter(Usuari.id == int(usuari_id)).first()
    if not usuari:
        raise credentials_error
    return usuari

def requerir_admin(usuari: Usuari = Depends(get_usuari_actual)) -> Usuari:
    if usuari.rol != RolUsuari.ADMIN:
        raise HTTPException(status_code=403, detail="Accés restringit a administradors")
    return usuari

def requerir_mecanic(usuari: Usuari = Depends(get_usuari_actual)) -> Usuari:
    if usuari.rol not in [RolUsuari.MECANIC, RolUsuari.ADMIN]:
        raise HTTPException(status_code=403, detail="Accés restringit a mecànics")
    return usuari