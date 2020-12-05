from typing import List
import logging
from sqlalchemy.orm import Session

from domains.user.entity.value import UserType, UserDisable
from domains.user.models.user import User
from infrastructure.config.database_config import db_session


class UserController(object):
    def __init__(self, session: Session):
        self.session = session

    def get_users(self, keys: List[str] = [],ids: List[int] = [], name: str = None, phones: List[int] = None,
                  email:str = None, offset: int=None, limit: int=None,user_type: UserType = None,
                  disable: UserDisable = None, level: int = 0) -> List[User]:
        if not any([keys, ids, name, phones, email, user_type, disable, level]):
            return []
        query = self.session.query(User)
        if user_type:
            query = query.filter(User.type == user_type.value)
        if disable:
            query = query.filter(User.disable == disable.value)
        if keys:
            query = query.filter(User.key.in_(keys))
        if ids:
            query = query.filter(User.id.in_(ids))
        if phones:
            query = query.filter(User.phone.in_(phones))
        if level:
            query = query.filter(User.level == level)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        try:
            users = query.all()

            if name:
                temp_users = list()
                for user in users:
                    if name in user.name:
                        temp_users.append(user)
                users = temp_users

            if email:
                temp_users = list()
                for user in users:
                    if email in user.email:
                        temp_users.append(user)
                users = temp_users
        except Exception as e:
            logging.error(f"get users fail: {e}")
            return list()
        return users

    def update_user(self, user: User, name: str=None, phone: int=None, email:str=None,
                  user_type: UserType = UserType.Formal, level: int = None, password: str=None) -> bool:
        if not user:
            return False
        if password:
            user.password = password
        if name:
            user.name = name
        if phone:
            user.phone = phone
        if email:
            user.email = email
        if user_type:
            user.type = user_type.value
        if level is not None:
            user.level = level
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"user update fail: {e}")
            return False
        return True

    def disable_users(self, users: List[User]) -> bool:
        for user in users:
            user.disable = UserDisable.disable.value
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"diable user fail: {e}")
            return False
        return True

    def enable_user(self, user: User) -> bool:
        user.disable = UserDisable.able.value
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"enable user fail: {e}")
            return False
        return True

    def create_user(self, name: str, key: str, password: str, phone: int = None, email: str = None,
                    user_type: UserType = UserType.Formal, disable: UserDisable = UserDisable.able, level: int = 0) -> User:
        user = User(key=key, name=name, password=password, phone=phone, email=email, type=user_type.value, disable=disable.value, level=level)
        if email:
            user.email = email
        if phone:
            user.phone = phone
        try:
            self.session.add(user)
            self.session.commit()
        except Exception as e:
            logging.error(f"create user fail: {e}")
            return None
        return user


def get_user_controller(session=db_session):
    return UserController(session=session)
