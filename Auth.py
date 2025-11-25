import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)