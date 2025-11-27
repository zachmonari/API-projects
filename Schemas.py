from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True
    }
class Token(BaseModel):
    access_token: str
    token_type: str


class BookBase(BaseModel):
    title: str
    author: str
    pages: int
    description: str | None = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # replaces orm_mode
