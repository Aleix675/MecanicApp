from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.cita import Cita,EstatCita
from app.models.vehicle import Vehicle
from app.models.servei import Servei
from app.models.usuari import Usuari, RolUsuari
from app.schemas.cita import CitaResponse,CitaCreate,CitaUpdate,CitaResponse,DisponibilitatRequest
from app.security.dependencies import get_usuari_actual, requerir_admin, requerir_mecanic

from app.sevices.disponibilitat_service import (
    calcular_hora_fi, hi_ha_solapament, obtenir_mechanics_disponibles, obtenir_places_ocupades
)

router = APIRouter()

# Consultar disponibilitat abans de reservar
@router.post("/cites/disponibilitat")
def consultar_disponibilitat(
    
    dades: DisponibilitatRequest,
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(get_usuari_actual)
):
    servei = db.query(Servei).filter(Servei.id == dades.servei_id).first()
    dades.data_hora_inici = dades.data_hora_inici.replace(tzinfo=None)
    if not servei:
        raise HTTPException(status_code=404, detail="Servei no trobat")

    hora_fi = calcular_hora_fi(dades.data_hora_inici, servei, dades.tipus_vehicle)
    mechanics = obtenir_mechanics_disponibles(db, dades.data_hora_inici, hora_fi)
    places_ocupades = obtenir_places_ocupades(db, dades.data_hora_inici, hora_fi)

    return {
        "hora_inici": dades.data_hora_inici,
        "hora_fi": hora_fi,
        "duracio_minuts": servei.duracio_base_min,
        "mechanics_disponibles": len(mechanics),
        "places_ocupades": places_ocupades,
        "disponible": len(mechanics) > 0
    }

# Crear cita
@router.post("/cites", response_model=CitaResponse, status_code=201)
def crear_cita(
    dades: CitaCreate,
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(get_usuari_actual)
):
    data_inici = dades.data_hora_inici.replace(tzinfo=None)
    data_inici.hour+1
    
    # Verificar que el vehicle és de l'usuari
    vehicle = db.query(Vehicle).filter(Vehicle.id == dades.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle no trobat")
    if vehicle.usuari_id != usuari_actual.id and usuari_actual.rol != RolUsuari.ADMIN:
        raise HTTPException(status_code=403, detail="No pots reservar amb un vehicle que no és teu")

    servei = db.query(Servei).filter(Servei.id == dades.servei_id).first()
    if not servei:
        raise HTTPException(status_code=404, detail="Servei no trobat")

    hora_fi = calcular_hora_fi(dades.data_hora_inici, servei, vehicle.tipus)

    # Obtenir mecànic disponible automàticament
    mechanics = obtenir_mechanics_disponibles(db, dades.data_hora_inici, hora_fi)
    if not mechanics:
        raise HTTPException(status_code=400, detail="No hi ha mecànics disponibles en aquest horari")

    hora_fi = calcular_hora_fi(data_inici, servei, vehicle.tipus)
    
    cita = Cita(
        vehicle_id=dades.vehicle_id,
        servei_id=dades.servei_id,
        mecanic_id=mechanics[0].id,
        data_hora_inici=data_inici,  # ← usa data_inici
        data_hora_fi=hora_fi,
        observacions_client=dades.observacions_client
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita

# Obtenir cites pròpies (client)
@router.get("/cites/meves", response_model=list[CitaResponse])
def obtenir_cites_meves(
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(get_usuari_actual)
):
    vehicles_ids = [v.id for v in db.query(Vehicle).filter(
        Vehicle.usuari_id == usuari_actual.id
    ).all()]
    return db.query(Cita).filter(Cita.vehicle_id.in_(vehicles_ids)).all()

# Obtenir totes les cites (admin)
@router.get("/cites", response_model=list[CitaResponse])
def obtenir_totes_cites(
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(requerir_admin)
):
    return db.query(Cita).all()

# Obtenir cites del mecànic
@router.get("/cites/meves-assignades", response_model=list[CitaResponse])
def obtenir_cites_assignades(
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(requerir_mecanic)
):
    return db.query(Cita).filter(Cita.mecanic_id == usuari_actual.id).all()

# Cancellar cita (client o admin)
@router.put("/cites/{cita_id}/cancellar", response_model=CitaResponse)
def cancellar_cita(
    cita_id: int,
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(get_usuari_actual)
):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no trobada")

    vehicle = db.query(Vehicle).filter(Vehicle.id == cita.vehicle_id).first()
    es_propietari = vehicle.usuari_id == usuari_actual.id
    es_admin = usuari_actual.rol == RolUsuari.ADMIN

    if not es_propietari and not es_admin:
        raise HTTPException(status_code=403, detail="No pots cancel·lar aquesta cita")

    if cita.estat == EstatCita.COMPLETADA:
        raise HTTPException(status_code=400, detail="No es pot cancel·lar una cita ja completada")

    cita.estat = EstatCita.CANCELADA
    db.commit()
    db.refresh(cita)
    return cita

# Completar cita (mecànic o admin)
@router.put("/cites/{cita_id}/completar", response_model=CitaResponse)
def completar_cita(
    cita_id: int,
    preu_final: float,
    db: Session = Depends(get_db),
    usuari_actual: Usuari = Depends(requerir_mecanic)
):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no trobada")
    if cita.estat == EstatCita.CANCELADA:
        raise HTTPException(status_code=400, detail="No es pot completar una cita cancel·lada")

    cita.estat = EstatCita.COMPLETADA
    cita.preu_final = preu_final
    db.commit()
    db.refresh(cita)
    return cita