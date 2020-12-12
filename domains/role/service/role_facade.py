from typing import List

from pydantic.main import BaseModel

from domains.role.entity.value import RoleType, RoleDisable
from domains.role.models.role import Role
from domains.role.repository.role_controller import get_role_controller
import domains.item.service.item_facade as item_facade

uc = get_role_controller()


class RoleModel(BaseModel):
    key: str
    name: str
    extra: str = None
    type: int
    level: int


def create_role(role: RoleModel) -> Role:
    new_role = uc.create_role(name=role.name, key=role.key, level=role.level,
                          role_type=RoleType(role.type))
    if new_role and item_facade.create_role(key=role.key, extra=role.extra):
        return role
    return None


def get_roles(
        keys: List[str] = None, name: str = None, level: int = None,
        role_type: RoleType = None, disable: RoleDisable = RoleDisable.able)\
        -> List[Role]:
    roles = uc.get_roles(keys=keys, name=name, role_type=role_type, disable=disable, level=level)
    return roles


def delete_roles(roles: List[Role]) -> bool:
    return uc.disable_roles(roles) and item_facade.disable_items([role.key for role in roles], item_type=item_facade.ItemType.role)


def update_role(role: Role, name: str = None,
                role_type: RoleType = None, level: int = None) -> bool:
    return uc.update_role(role=role, name=name, role_type=role_type, level=level)
