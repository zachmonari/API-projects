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

get_student(1)
#GET with Query Parameter
@app.get("/vibration/energy")
def compute_energy(amplitude: float, mass: float):
    return {"energy": 0.5 * mass * amplitude**2}
compute_energy(3.0, 3.0)

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