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