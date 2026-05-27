from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.nota_tecnica import NotaTecnica
from app.models.cita import Cita
from app.models.usuari import Usuari
from app.schemas.nota import NotaCreate, NotaResponse
from app.security.dependencies import requerir_mecanic, get_usuari_actual

router = APIRouter()

# Afegir nota a una cita
@router.post("/cites/{cita_id}/notes", response_model=NotaResponse, status_code=201)
def afegir_nota(
    cita_id: int,
    dades: NotaCreate,
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(requerir_mecanic)
):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no trobada")
    if cita.mecanic_id != usuari_actual.id:
        raise HTTPException(status_code=403, detail="Només pots afegir notes a les teves cites")

    nota = NotaTecnica(
        cita_id=cita_id,
        mecanic_id=usuari_actual.id,
        contingut=dades.contingut
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    return nota

# Obtenir notes d'una cita
@router.get("/cites/{cita_id}/notes", response_model=list[NotaResponse])
def obtenir_notes(
    cita_id: int,
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(get_usuari_actual)
):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no trobada")
    return db.query(NotaTecnica).filter(NotaTecnica.cita_id == cita_id).all()