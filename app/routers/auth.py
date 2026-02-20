from pydantic import BaseModel
from fastapi import router

from app import models, database

class PasswordEncryption():
    from datetime import datetime, timedelta
    from jose import JWTError, jwt
    from passlib.context import CryptContext

class RegisterRequest(BaseModel):
    phone_number: str
    username: str
    hashed_password: str

class LoginRequest(BaseModel):
    username: str
    hashed_password: str


@router.post("/register")
def register(data: RegisterRequest):
    db = database.get_db()
    db.