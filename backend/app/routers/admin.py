from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.dependencies import get_db
from app.models.usuari import Usuari, RolUsuari
from app.models.servei import Servei
from app.security.dependencies import requerir_admin
from app.schemas.usuari import UsuariResponse

router = APIRouter(prefix="/admin")

@router.get("/estadistiques")
def obtenir_estadistiques(
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(requerir_admin)
):
    total_cites = db.execute(text("SELECT COUNT(*) FROM cita")).scalar()
    cites_completades = db.execute(text("SELECT COUNT(*) FROM cita WHERE estat::text = 'COMPLETADA'")).scalar()
    cites_pendents = db.execute(text("SELECT COUNT(*) FROM cita WHERE estat::text = 'PENDENT'")).scalar()
    cites_cancelades = db.execute(text("SELECT COUNT(*) FROM cita WHERE estat::text = 'CANCELADA'")).scalar()

    ingressos = db.execute(text(
        "SELECT COALESCE(SUM(preu_final), 0) FROM cita WHERE estat::text = 'COMPLETADA'"
    )).scalar()

    serveis_populars = db.execute(text("""
        SELECT s.nom, COUNT(c.id) as total
        FROM servei s
        LEFT JOIN cita c ON c.servei_id = s.id
        GROUP BY s.nom
        ORDER BY total DESC
        LIMIT 5
    """)).fetchall()

    total_clients = db.execute(text("SELECT COUNT(*) FROM usuari WHERE rol::text = 'CLIENT'")).scalar()
    total_mechanics = db.execute(text("SELECT COUNT(*) FROM usuari WHERE rol::text = 'MECANIC'")).scalar()

    return {
        "cites": {
            "total": total_cites,
            "completades": cites_completades,
            "pendents": cites_pendents,
            "cancelades": cites_cancelades
        },
        "ingressos_totals": float(ingressos),
        "serveis_populars": [{"nom": r[0], "total": r[1]} for r in serveis_populars],
        "usuaris": {
            "clients": total_clients,
            "mechanics": total_mechanics
        }
    }

@router.get("/mechanics", response_model=list[UsuariResponse])
def obtenir_mechanics(
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(requerir_admin)
):
    return db.query(Usuari).filter(Usuari.rol == RolUsuari.MECANIC).all()

@router.put("/usuaris/{usuari_id}/rol")
def canviar_rol(
    usuari_id: int,
    nou_rol: str,
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(requerir_admin)
):
    usuari = db.query(Usuari).filter(Usuari.id == usuari_id).first()
    if not usuari:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    usuari.rol = RolUsuari(nou_rol)
    db.commit()
    return {"missatge": f"Rol actualitzat a {nou_rol}"}