from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext 

from app import models, database
from sqlalchemy.orm import Session
from fastapi import Depends

from dotenv import load_dotenv
import os

load_dotenv()
router =APIRouter()


class PasswordEncryption():
    
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = 'HS256'

    def hash_password(self, password: str) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)


class RegisterRequest(BaseModel):
    username: str
    password: str
    phone_number: str

class LoginRequest(BaseModel):
    username: str
    password: str

def validate_register_request(username: str, phone_number: str, db: Session = Depends(database.get_db)) -> bool:
        #check username
    existing_name = db.query(models.User).filter(models.User.username == username).first()
    #check phone_number
    existing_number = db.query(models.User).filter(models.User.phone_number == phone_number).first()

    if existing_name or existing_number: return False
    return True

def validate_login_request(username: str, password: str, db: Session = Depends(database.get_db)) -> models.User:
    user: models.User = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        return None
    if not PasswordEncryption().verify_password(password, user.hashed_password):
        return None

    return user


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(database.get_db)):
    to_register: RegisterRequest = data.copy()

    valid_data: bool = validate_register_request(to_register.username, to_register.phone_number, db=db)
    if not valid_data: raise HTTPException(status_code=400, detail="Username or phonenumber already exist.")

    hashed_password: str = PasswordEncryption().hash_password(to_register.password)

    new_user = models.User(
        username=to_register.username,
        phone_number=to_register.phone_number,
        hashed_password=hashed_password,
        is_verified=False
    )
    
    db.add(new_user)
    db.commit()

    return {"message" : f"Registered {new_user.username} successfully."}

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(database.get_db)):
    to_login = data.copy()

    user: models.User = validate_login_request(to_login.username, to_login.password, db=db)
    if not user: raise HTTPException(status_code=400, detail="Wrong username or password.")

    return {
        "message" : f"Welcome {to_login.username}, you are now logged.",
        "username": user.username,
        "user_id": user.id
    }
