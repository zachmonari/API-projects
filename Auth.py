from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
