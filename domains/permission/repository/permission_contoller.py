from typing import List
import logging

from sqlalchemy.orm import Session

from domains.permission.entity.const import PermissionDisable
from domains.permission.models.permission import Permission
from infrastructure.config.database_config import db_session


class PermissionController(object):
    def __init__(self, session: Session, search_extra = None):
        self.session = session
        if search_extra:
            self.search_extra = search_extra

    def search_extra(self, extra: str, entities: List) -> List:
        # 后续需要传入，如果需要使用extra进行搜索的话
        return entities

    def create_permission(self, key: str, name: str,
                          disable: PermissionDisable = PermissionDisable.able,
                          level: int = 0, extra: str = None) -> Permission:
        permission = Permission(key=key, name=name, disable=disable.value, level=level)
        if extra:
            permission.extra = extra
        try:
            self.session.add(permission)
            self.session.commit()
        except Exception as e:
            logging.error(f"create user fail: {e}")
            return None
        return permission

    def get_permissions(self, keys: List[str] = [], ids: List[int] = [], name: str = None, offset: int = None,
                        limit: int = None, disable: PermissionDisable = None, level: int = None,
                        extra: str = None) -> List[Permission]:
        if not any([keys, ids, name, disable, level, extra]):
            return []
        query = self.session.query(Permission)
        if disable is not None:
            query = query.filter(Permission.disable == disable.value)
        if keys:
            query = query.filter(Permission.key.in_(keys))
        if ids:
            query = query.filter(Permission.id.in_(ids))
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        if level:
            query = query.filter(Permission.level == level)
        try:
            permissions = query.all()

            if name:
                temp_permissions = list()
                for user in permissions:
                    if name in user.name:
                        temp_permissions.append(user)
                permissions = temp_permissions

            if extra:
                permissions = self.search_extra(extra, permissions)

        except Exception as e:
            logging.error(f"get permissions fail: {e}")
            return list()
        return permissions
    
    def update_permission(self, permission: Permission, name: str = None, level: int = None,
                          extra: str = None) -> bool:
        if name:
            permission.name = name
        if level is not None:
            permission.level = level
        if extra is not None:
            permission.extra = extra
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"permission update fail: {e}")
            return False
        return True

    def disable_permission(self, permission: Permission) -> bool:
        permission.disable = PermissionDisable.disable.value
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"diable permission fail: {e}")
            return False
        return True

    def enable_permission(self, permission: Permission) -> bool:
        permission.disable = PermissionDisable.able.value
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"enable permission fail: {e}")
            return False
        return True


def get_permission_controller(session=db_session):
    return PermissionController(session=session)
