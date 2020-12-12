from typing import List

from pydantic.main import BaseModel

from domains.user.entity.value import UserType, UserDisable
from domains.user.models.user import User
from domains.user.repository.user_controller import get_user_controller
import domains.item.service.item_facade as item_facade

uc = get_user_controller()


class UserModel(BaseModel):
    key: str
    password: str
    name: str
    email: str = None
    phone: str = None
    extra: str = None
    type: int
    level: int


def create_user(user: UserModel) -> User:
    new_user = uc.create_user(password=user.password, name=user.name, key=user.key, email=user.email, level=user.level,
                          user_type=UserType(user.type), phone=user.phone)
    if new_user and item_facade.create_user(key=user.key, extra=user.extra):
        return user
    return None


def get_users(
        keys: List[str] = None, name: str = None, level: int = None, email: str = None,
        phones: List[int] = None, user_type: UserType = None, disable: UserDisable = None)\
        -> List[User]:
    users = uc.get_users(keys=keys, name=name, phones=phones, email=email, user_type=user_type, disable=disable, level=level)
    return users


def delete_users(users: List[User]) -> bool:
    return uc.disable_users(users)


def update_user(user: User, name: str = None, phone: int = None, email: str = None,
                user_type: UserType = None, level: int = None, password: str = None) -> bool:
    return uc.update_user(user=user, name=name, phone=phone, email=email, user_type=user_type, level=level, password=password)
