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