from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from Auth import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import Models
from Database import engine, get_db
import Schemas
import Crud

Models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

