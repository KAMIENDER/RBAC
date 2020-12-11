import datetime
import time
from typing import List
import logging
from sqlalchemy.orm import Session

from domains.role.entity.value import RoleType, RoleDisable
from domains.role.models.role import Role
from infrastructure.config.database_config import db_session


class RoleController(object):
    def __init__(self, session: Session):
        self.session = session

    def get_roles(self, keys: List[str] = [],ids: List[int] = [], name: str = None,
                  offset: int=None, limit: int=None,role_type: RoleType = None,
                  disable: RoleDisable = None, level: int = 0) -> List[Role]:
        if not any([keys, ids, name, role_type, disable, level]):
            return []
        query = self.session.query(Role)
        if role_type:
            query = query.filter(Role.type == role_type.value)
        if disable:
            query = query.filter(Role.disable == disable.value)
        if keys:
            query = query.filter(Role.key.in_(keys))
        if ids:
            query = query.filter(Role.id.in_(ids))
        if level:
            query = query.filter(Role.level == level)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        try:
            roles = query.all()

            if name:
                temp_roles = list()
                for role in roles:
                    if name in role.name:
                        temp_roles.append(role)
                roles = temp_roles
        except Exception as e:
            logging.error(f"get roles fail: {e}")
            return list()
        return roles

    def update_role(self, role: Role, name: str=None,
                  role_type: RoleType = RoleType.normal, level: int = None, password: str=None) -> bool:
        role.modifiedtime = time.localtime(time.time())
        if not role:
            return False
        if password:
            role.password = password
        if name:
            role.name = name
        if role_type:
            role.type = role_type.value
        if level is not None:
            role.level = level
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"role update fail: {e}")
            return False
        return True

    def disable_roles(self, roles: List[Role]) -> bool:
        for role in roles:
            role.disable = RoleDisable.disable.value
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"diable role fail: {e}")
            return False
        return True

    def enable_role(self, role: Role) -> bool:
        role.disable = RoleDisable.able.value
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"enable role fail: {e}")
            return False
        return True

    def create_role(self, name: str, key: str,
                    role_type: RoleType = RoleType.normal, disable: RoleDisable = RoleDisable.able, level: int = 0) -> Role:
        role = Role(key=key, name=name, type=role_type.value, disable=disable.value, level=level)
        role.modifiedtime = time.localtime(time.time())
        try:
            self.session.add(role)
            self.session.commit()
        except Exception as e:
            logging.error(f"create role fail: {e}")
            return None
        return role


def get_role_controller(session=db_session):
    return RoleController(session=session)
