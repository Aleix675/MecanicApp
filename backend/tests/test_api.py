import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ── AUTH ─────────────────────────────────────────────
def test_register_usuari():
    response = client.post("/auth/register", json={
        "nom": "Test Usuari",
        "email": "test_pytest@test.com",
        "password": "1234",
        "telefon": "600000000"
    })
    assert response.status_code in [201, 400]  # 400 si ja existeix

def test_login_correcte():
    # Primer registre
    client.post("/auth/register", json={
        "nom": "Login Test",
        "email": "login_pytest@test.com",
        "password": "1234"
    })
    # Després login
    response = client.post("/auth/login", json={
        "email": "login_pytest@test.com",
        "password": "1234"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_incorrecte():
    response = client.post("/auth/login", json={
        "email": "noexisteix@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_login_retorna_rol():
    client.post("/auth/register", json={
        "nom": "Rol Test",
        "email": "rol_pytest@test.com",
        "password": "1234"
    })
    response = client.post("/auth/login", json={
        "email": "rol_pytest@test.com",
        "password": "1234"
    })
    data = response.json()
    assert data["rol"] == "CLIENT"

# ── HELPER ───────────────────────────────────────────
def get_token(email="token_pytest@test.com", password="1234"):
    client.post("/auth/register", json={
        "nom": "Token Test",
        "email": email,
        "password": password
    })
    response = client.post("/auth/login", json={
        "email": email,
        "password": password
    })
    return response.json().get("access_token")

def get_headers(email="token_pytest@test.com"):
    token = get_token(email)
    return {"Authorization": f"Bearer {token}"}

# ── VEHICLES ─────────────────────────────────────────
def test_crear_vehicle():
    headers = get_headers("vehicle_pytest@test.com")
    # Obtenir userId
    login = client.post("/auth/login", json={
        "email": "vehicle_pytest@test.com",
        "password": "1234"
    })
    usuari_id = login.json().get("id")

    response = client.post("/vehicles", json={
        "usuari_id": usuari_id,
        "marca": "Toyota",
        "model": "Corolla",
        "matricula": "TEST001",
        "any_fabricacio": 2020,
        "tipus": "TURISME"
    }, headers=headers)
    assert response.status_code in [201, 400]

def test_obtenir_vehicles_meus():
    headers = get_headers("meusvehicles_pytest@test.com")
    response = client.get("/vehicles/meus", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_vehicles_sense_token():
    response = client.get("/vehicles/meus")
    assert response.status_code == 401

# ── SERVEIS ───────────────────────────────────────────
def test_obtenir_serveis_public():
    response = client.get("/serveis")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_servei_sense_auth():
    response = client.post(
        "/serveis",
        json={
            "nom": "Test Servei",
            "descripcio": "Servei de prova",
            "duracio_base_min": 60,
            "duracio_suv_min": 90,
            "preu_orientatiu": 50.0,
            "actiu": True
        }
    )

    assert response.status_code == 401

# ── CITES ─────────────────────────────────────────────
def test_obtenir_cites_meves():
    headers = get_headers("cites_pytest@test.com")
    response = client.get("/cites/meves", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_cites_sense_token():
    response = client.get("/cites/meves")
    assert response.status_code == 401

# ── ADMIN ─────────────────────────────────────────────
def test_admin_requereix_rol():
    headers = get_headers("noadmin_pytest@test.com")
    response = client.get("/admin/estadistiques", headers=headers)
    assert response.status_code == 403

def test_admin_sense_token():
    response = client.get("/admin/estadistiques")
    assert response.status_code == 401

# ── ROOT ──────────────────────────────────────────────
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"missatge": "MecànicApp API funcionant!"}