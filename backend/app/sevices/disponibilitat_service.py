from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta
from app.models.servei import Servei
from app.models.usuari import Usuari, RolUsuari

def calcular_hora_fi(hora_inici: datetime, servei: Servei, tipus_vehicle: str) -> datetime:
    tipus_upper = tipus_vehicle.upper() if tipus_vehicle else "TURISME"
    if tipus_upper in ["SUV", "FURGONETA", "CAMIO"]:
        minuts = servei.duracio_suv_min or 60
    else:
        minuts = servei.duracio_base_min or 60
    hora_inici_naive = hora_inici.replace(tzinfo=None)
    return hora_inici_naive + timedelta(minutes=minuts)

def obtenir_mechanics_disponibles(db: Session, hora_inici: datetime, hora_fi: datetime) -> list:
    hora_inici = hora_inici.replace(tzinfo=None)
    hora_fi = hora_fi.replace(tzinfo=None)

    # SQL pur per evitar problemes amb l'enum de PostgreSQL
    result = db.execute(text("""
        SELECT id FROM usuari
        WHERE rol = 'MECANIC' AND actiu = true
        AND id NOT IN (
            SELECT mecanic_id FROM cita
            WHERE estat::text != 'CANCELADA'
            AND data_hora_inici < :hora_fi
            AND data_hora_fi > :hora_inici
        )
    """), {"hora_inici": hora_inici, "hora_fi": hora_fi})

    ids = [row[0] for row in result]
    if not ids:
        return []
    return db.query(Usuari).filter(Usuari.id.in_(ids)).all()

def obtenir_places_ocupades(db: Session, hora_inici: datetime, hora_fi: datetime) -> int:
    hora_inici = hora_inici.replace(tzinfo=None)
    hora_fi = hora_fi.replace(tzinfo=None)

    result = db.execute(text("""
        SELECT COUNT(*) FROM cita
        WHERE estat::text != 'CANCELADA'
        AND data_hora_inici < :hora_fi
        AND data_hora_fi > :hora_inici
    """), {"hora_inici": hora_inici, "hora_fi": hora_fi})

    return result.scalar()

def hi_ha_solapament(db: Session, mecanic_id: int, hora_inici: datetime, hora_fi: datetime, excloure_cita_id: int = None) -> bool:
    hora_inici = hora_inici.replace(tzinfo=None)
    hora_fi = hora_fi.replace(tzinfo=None)

    query = """
        SELECT COUNT(*) FROM cita
        WHERE mecanic_id = :mecanic_id
        AND estat::text != 'CANCELADA'
        AND data_hora_inici < :hora_fi
        AND data_hora_fi > :hora_inici
    """
    params = {"mecanic_id": mecanic_id, "hora_inici": hora_inici, "hora_fi": hora_fi}

    if excloure_cita_id:
        query += " AND id != :excloure_id"
        params["excloure_id"] = excloure_cita_id

    result = db.execute(text(query), params)
    return result.scalar() > 0