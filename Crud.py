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