from typing import List, Dict, Set

from pydantic.main import BaseModel

from domains.role.entity.value import RoleType, RoleDisable
from domains.role.models.role import Role
from domains.role.repository.role_controller import get_role_controller
import domains.item.service.item_facade as item_facade
import domains.user.service.facade as user_facade

rc = get_role_controller()


class RoleModel(BaseModel):
    owner_keys: List[str]
    key: str
    name: str
    extra: str = None
    type: int
    level: int


def set_roles_owners(roles: List[RoleModel], owner_keys: List[str]) -> bool:
    if not owner_keys:
        return True
    owners = user_facade.get_users(keys=owner_keys)
    if not owners:
        return False
    return item_facade.set_owners_of_roles(
        user_keys=[owner.key for owner in owners], role_keys=[role.key for role in roles])


def delete_roles_owners(roles: List[RoleModel], owner_keys: List[str]) -> bool:
    owners = user_facade.get_users(keys=owner_keys)
    if not owners:
        return False
    return item_facade.delete_roles_owners(
        role_keys=[role.key for role in roles], user_keys=[owner.key for owner in owners])


def update_roles_owners(roles: List[RoleModel], owner_keys: List[str]) -> bool:
    rolekey2ownerkey = item_facade.get_roles_owners(role_keys=[role.key for role in roles])
    test = dict(rolekey2ownerkey)
    for key, value in dict(rolekey2ownerkey).items():
        item_facade.delete_roles_owners(role_keys=[key], user_keys=value)
    return set_roles_owners(roles, owner_keys)


def get_roles_owners(roles: List[RoleModel]) -> Dict[str, List[str]]:
    return item_facade.get_roles_owners([role.key for role in roles])


def create_role(role: RoleModel) -> Role:
    owners = user_facade.get_users(keys=role.owner_keys)
    if not owners:
        return None
    if not item_facade.create_role(key=role.key, extra=role.extra):
        return None
    new_role = rc.create_role(name=role.name, key=role.key, level=role.level,
                              role_type=RoleType(role.type))
    if not new_role:
        item_facade.disable_items(keys=[role.key])
        return None
    if not item_facade.set_owners_of_roles(user_keys=[owner.key for owner in owners], role_keys=[role.key]):
        item_facade.disable_items(keys=[role.key])
        rc.disable_roles([new_role])
        return None
    return new_role


def get_roles(
        keys: List[str] = None, name: str = None, level: int = None,
        role_type: RoleType = None, disable: RoleDisable = RoleDisable.able) \
        -> List[Role]:
    roles = rc.get_roles(keys=keys, name=name, role_type=role_type, disable=disable, level=level)
    return roles


def delete_roles(roles: List[Role]) -> bool:
    return rc.disable_roles(roles) and item_facade.disable_items([role.key for role in roles],
                                                                 item_type=item_facade.ItemType.role)


def update_role(role: Role, name: str = None,
                role_type: RoleType = None, level: int = None) -> bool:
    return rc.update_role(role=role, name=name, role_type=role_type, level=level)


def delete_roles_members(role_keys: List[str], item_keys: List[str], item_type: item_facade.ItemType) -> bool:
    return item_facade.disable_old_refs(
        main_keys=role_keys, main_type=item_facade.ItemType.role,
        attach_keys=item_keys, attach_type=item_type)


def set_roles_members(role_keys: List[str], item_keys: List[str], item_type: item_facade.ItemType) -> bool:
    if not delete_roles_members(role_keys, item_keys, item_type):
        return False
    return item_facade.attach_in_items_to_mains(
        main_keys=role_keys, main_type=item_facade.ItemType.role,
        attach_keys=item_keys, attach_type=item_type)


def get_roles_members_direct(
        role_keys: List[str], item_type: item_facade.ItemType,
        disable: item_facade.ItemRefDisable = item_facade.ItemRefDisable.able) \
        -> Dict[str, List[str]]:
    return item_facade.get_items_attached_to_in_items(
        main_keys=role_keys, attach_item_type=item_type,
        disable=disable, main_item_type=item_facade.ItemType.role)


def judge_users_owned_roles(user_keys: List[str], role_keys: List[str]) -> Dict[str, List[str]]:
    return item_facade.judge_have_ref(main_keys=user_keys, main_type=item_facade.ItemType.user,
                                      attach_keys=role_keys, attach_type=item_facade.ItemType.role)


def get_role_members_flatten(role_key: List[str], role_member_keys: List[str], user_member_keys: List[str]) -> Dict[str, List[str]]:
    now_role_member_keys = get_roles_members_direct(role_keys=[role_key], item_type=item_facade.ItemType.role)[role_key]
    now_user_keys = get_roles_members_direct(role_keys=[role_key], item_type=item_facade.ItemType.user)[role_key]
    user_member_keys.extend(now_user_keys)
    delta_role_member_keys = list(set(now_role_member_keys) - set(role_member_keys))
    role_member_keys.extend(delta_role_member_keys)
    for now_role_key in delta_role_member_keys:
        get_role_members_flatten(now_role_key, role_member_keys, user_member_keys)
    return {
        'roles': role_member_keys,
        'users': user_member_keys
    }

