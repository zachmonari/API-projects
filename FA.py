from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app=FastAPI()

@app.get("/")
def home():
    return {"message":"Hello FastAPI Learner!"}

#GET Request with Path Parameter
@app.get("/student/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id}


#GET with Query Parameter
@app.get("/vibration/energy")
def compute_energy(amplitude: float, mass: float):
    return {"energy": 0.5 * mass * amplitude**2}


class Book(BaseModel):
    title: str
    author: str
    pages: int
@app.post("/add-book")
def add_book(book: Book):
    return {"message": "Book added!", "data": book}

# Full example
# ------------------------
# DATA MODEL
# ------------------------
class Book(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    description: Optional[str] = None

# Fake in-memory database
books_db: List[Book] = []

# ------------------------
# 1️⃣ CREATE (POST)
# ------------------------
@app.post("/books", response_model=Book)
def create_book(book: Book):
    # Check if ID already exists
    for b in books_db:
        if b.id == book.id:
            raise HTTPException(status_code=400, detail="Book with this ID already exists")

    books_db.append(book)
    return book

# ------------------------
# 2️⃣ READ ALL (GET)
# ------------------------
@app.get("/books", response_model=List[Book])
def get_all_books():
    return books_db

# ------------------------
# 3️⃣ READ ONE (GET by ID)
# ------------------------
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# ------------------------
# 5️⃣ DELETE (DELETE)
# ------------------------
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[index]
            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")