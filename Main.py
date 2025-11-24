from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import Models
from Database import engine, get_db
import Schemas
import Crud

Models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CREATE
@app.post("/books", response_model=Schemas.Book)
def create_book(book: Schemas.BookCreate, db: Session = Depends(get_db)):
    return Crud.create_book(db, book)

# READ ALL
@app.get("/books", response_model=list[Schemas.Book])
def read_books(db: Session = Depends(get_db)):
    return Crud.get_books(db)

# READ ONE
@app.get("/books/{book_id}", response_model=Schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = Crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# UPDATE
@app.put("/books/{book_id}", response_model=Schemas.Book)
def update_book(book_id: int, book: Schemas.BookCreate, db: Session = Depends(get_db)):
    updated = Crud.update_book(db, book_id, book)
    if updated is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

# DELETE
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = Crud.delete_book(db, book_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
