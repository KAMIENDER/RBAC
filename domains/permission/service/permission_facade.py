from typing import List

from domains.item.service.item_facade import *
from domains.permission.models.permission import Permission
from domains.permission.repository.permission_contoller import get_permission_controller
import domains.item.service.item_facade as item_facade
import domains.user.service.facade as user_facade

pc = get_permission_controller()


def create_permission(
        owner_keys: List[str], permission_key: str, permission_name: str, permission_level: int, extra: str=None) -> bool:
    if not owner_keys:
        return False
    item = item_facade.create_permission(key=permission_key, extra=extra)
    if not item:
        return False
    permission = pc.create_permission(key=permission_key, name=permission_name, level=permission_level, extra=extra)
    if not permission:
        item_facade.disable_permissions([permission_key])
        return False
    if not item_facade.set_permissions_owners(user_keys=owner_keys, permission_keys=[permission_key]):
        item_facade.disable_permissions([permission_key])
        pc.disable_permission(permission)
        return False
    return True


def get_user_owned_permissions(
        owner_keys: List[str], permission_keys: List[str]=[], permission_name: str=None,
        permission_level: int=None, extra: str=None) -> List[Permission]:
    temp_permission_keys = list()
    temp_permission_keys.extend(permission_keys)
    userkey2permissionkeys = get_own_permissions_of_users(user_keys=owner_keys)
    if userkey2permissionkeys:
        [temp_permission_keys.extend(value) for value in userkey2permissionkeys.values()]
    return pc.get_permissions(keys=temp_permission_keys, name=permission_name, level=permission_level, extra=extra)


def get_user_had_but_not_owned_permissions(
        user_keys: List[str]=[], permission_keys: List[str]=[], permission_name: str=None,
        permission_level: int=None, extra: str=None) -> List[Permission]:
    temp_permission_keys = list()
    temp_permission_keys.extend(permission_keys)
    userkey2permissionkeys = get_had_not_owned_permissions_of_users(user_keys=user_keys)
    if userkey2permissionkeys:
        [temp_permission_keys.extend(value) for value in userkey2permissionkeys.values()]
    return pc.get_permissions(keys=temp_permission_keys, name=permission_name, level=permission_level, extra=extra)


def set_permissions_owners(permission_keys: List[str], owner_keys: List[str]) -> bool:
    if not owner_keys:
        return True
    owners = user_facade.get_users(keys=owner_keys)
    if not owners:
        return False
    return item_facade.set_permissions_owners(
        user_keys=[owner.key for owner in owners], permission_keys=permission_keys)


def delete_permissions_owners(permission_keys: List[str], owner_keys: List[str]) -> bool:
    owners = user_facade.get_users(keys=owner_keys)
    if not owners:
        return False
    return item_facade.delete_permissions_owners(
        permission_keys=[permission.key for permission in permissions], user_keys=[owner.key for owner in owners])


def update_permissions_owners(permission_keys: List[str], owner_keys: List[str]) -> bool:
    permissionkey2ownerkey = item_facade.get_permissions_owners(permission_keys=[permission.key for permission in permissions])
    test = dict(permissionkey2ownerkey)
    for key, value in dict(permissionkey2ownerkey).items():
        item_facade.delete_permissions_owners(permission_keys=[key], user_keys=value)
    return set_permissions_owners(permissions, owner_keys)
