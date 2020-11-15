from typing import List
import logging
from sqlalchemy.orm import Session

from domains.user.entity.value import UserType, UserDisable
from domains.user.models.user import User
from infrastructure.config.database_config import db_session


class UserController(object):
    def __init__(self, session: Session):
        self.session = session

    def get_users(self, key: str = None,id: int = None, name: str = None, phone: int = None, email:str = None, offset: int=None, limit: int=None,
                  user_type: UserType = UserType.Formal, disable: UserDisable = UserDisable.able, level: int = 0) -> List[User]:
        query = self.session.query(User).filter(User.type == user_type.value, User.disable == disable.value)
        if key:
            query = query.filter(User.key == key)
        if id:
            query = query.filter(User.id == id)
        if phone:
            query = query.filter(User.phone == phone)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        if level:
            query = query.filter(User.level == level)
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

        return users

    def update_user(self, user: User, name: str, phone: int, email:str,
                  user_type: UserType = UserType.Formal, level: int = 0) -> bool:
        if name:
            user.name = name
        if phone:
            user.phone = phone
        if email:
            user.email = email
        if user_type:
            user.type = user_type.value
        if level:
            user.level = level
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"user update fail: {e}")
            return False
        return True

    def disable_user(self, user: User) -> bool:
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

    def create_user(self, name: str, phone: int, email:str, key:str,
                    user_type: UserType = UserType.Formal, disable: UserDisable = UserDisable.able, level: int = 0) -> User:
        user = User(key=key, name=name, phone=phone, email=email, type=user_type.value, disable=disable.value, level=level)
        try:
            self.session.add(user)
            self.session.commit()
        except Exception as e:
            logging.error(f"create user fail: {e}")
            return None
        return user


def get_user_controller(session=db_session):
    return UserController(session=session)
