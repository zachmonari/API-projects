from sqlalchemy.orm import Session
import Models, Schemas
from Auth import hash_password, verify_password

def get_books(db: Session):
    return db.query(Models.Book).all()

def get_book(db: Session, book_id: int):
    return db.query(Models.Book).filter(Models.Book.id == book_id).first()

def create_book(db: Session, book: Schemas.BookCreate):
    db_book = Models.Book(
        title=book.title,
        author=book.author,
        pages=book.pages,
        description=book.description
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: Schemas.BookCreate):
    db_book = get_book(db, book_id)
    if db_book is None:
        return None

    db_book.title = book.title
    db_book.author = book.author
    db_book.pages = book.pages
    db_book.description = book.description

    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book is None:
        return None

    db.delete(db_book)
    db.commit()
    return db_book
