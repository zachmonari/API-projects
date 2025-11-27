from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from Auth import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import Models
from Database import engine, get_db
import Schemas
import Crud
from Schemas import BookCreate, Book
from Crud import create_book, get_books, get_book, update_book, delete_book


Models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ---------------------- AUTH HELPERS ---------------------- #
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    invalid = HTTPException(status_code=401, detail="Invalid authentication")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise invalid
    except JWTError:
        raise invalid

    user = Crud.get_user_by_username(db, username)
    if user is None:
        raise invalid
    return user


# ---------------------- ROUTES ---------------------------- #

@app.post("/register", response_model=Schemas.User)
def register(user: Schemas.UserCreate, db: Session = Depends(get_db)):
    existing = Crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    return Crud.create_user(db, user)


@app.post("/login", response_model=Schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = Crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/protected")
def protected_route(current_user: Schemas.User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you accessed a protected route!"}

@app.post("/books", response_model=Book)
def create_new_book(book: BookCreate, db: Session = Depends(get_db), current_user: Schemas.User = Depends(get_current_user)):
    return create_book(db, book, current_user.id)


@app.get("/books", response_model=list[Book])
def list_books(db: Session = Depends(get_db), current_user: Schemas.User = Depends(get_current_user)):
    return get_books(db, current_user.id)


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db), current_user: Schemas.User = Depends(get_current_user)):
    book = get_book(db, book_id, current_user.id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book