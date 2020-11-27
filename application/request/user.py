from pydantic import BaseModel


class UserRegisterRequestModel(BaseModel):
    key: str
    password: str
    name: str
    email: str = None
    phone: str = None
    extra: str = None
    type: int
    level: int

