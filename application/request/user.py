from pydantic import BaseModel


class UserRegisterRequestModel(BaseModel):
    key: int
    password: int
    name: str
    email: str = None
    phone: str = None
    type: int
    level: int

