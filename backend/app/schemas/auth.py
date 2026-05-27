from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    nom: str
    email: str
    password: str
    telefon: str | None = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    rol: str
    nom: str
    id : int