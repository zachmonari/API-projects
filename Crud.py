from sqlalchemy.orm import Session
import Models, Schemas
from Auth import hash_password, verify_password

def get_user_by_username(db: Session, username: str):
    return db.query(Models.User).filter(Models.User.username == username).first()
def create_user(db: Session, user: Schemas.UserCreate):
    hashed = hash_password(user.password)
    db_user = Models.User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_book(db: Session, book_data, user_id: int):
    new_book = Models.Book(
        title=book_data.title,
        author=book_data.author,
        pages=book_data.pages,
        description=book_data.description,
        owner_id=user_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_books(db: Session, user_id: int):
    return db.query(Models.Book).filter(Models.Book.owner_id == user_id).all()


def get_book(db: Session, book_id: int, user_id: int):
    return db.query(Models.Book).filter(
        Models.Book.id == book_id,
        Models.Book.owner_id == user_id
    ).first()

def update_book(db: Session, book_id: int, book_data, user_id: int):
    book = get_book(db, book_id, user_id)
    if not book:
        return None
    for key, value in book_data.dict().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int, user_id: int):
    book = get_book(db, book_id, user_id)
    if not book:
        return None
    db.delete(book)
    db.commit()
    return book