from sqlalchemy.orm import Session
import Models, Schemas
from Auth import hash_password, verify_password

def get_user_by_username(db: Session, username: str):
    return db.query(Models.User).filter(Models.User.username == username).first()
