from typing import List

from domains.item.service.item_facade import *
from domains.permission.entity.const import PermissionDisable
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


def get_permissions(keys: List[str] = [], name: str = None, level: int=None, disable: PermissionDisable = None):
    return pc.get_permissions(keys=keys,name=name,level=level,disable=disable)


def update_permissions(keys: List[str] = [], name: str = None, level: int = None, disable: PermissionDisable = None):
    permissions = pc.get_permissions(keys=keys)
    for permission in permissions:
        pc.update_permission(permission, name=name, level=level)
        if disable is not None:
            if disable == PermissionDisable.disable:
                pc.disable_permission(permission)
            else:
                pc.enable_permission(permission)
    return True


def get_permissions_items_ownerd(item_type: item_facade.ItemType, item_keys: List[str] = [], disable: PermissionDisable = None):
    item_key2permission_key = get_items_attached_to_in_items(
        main_keys=item_keys, attach_item_type=ItemType.permission, main_item_type=item_type)
    permission_keys = list()
    for _, permission_keys in item_key2permission_key.items():
        permission_keys.extend(permission_keys)
    permissions = get_permissions(keys=permission_keys, disable=disable)
    return permissions


def get_permissions_items_had(item_type: item_facade.ItemType, item_keys: List[str] = [], disable: PermissionDisable = None):
    item_key2permission_key = get_items_have_in_items(
        attach_keys=item_keys, attach_item_type=item_type, main_item_type=ItemType.permission)
    permission_keys = list()
    for _, permission_keys in item_key2permission_key.items():
        permission_keys.extend(permission_keys)
    permissions = get_permissions(keys=permission_keys, disable=disable)
    return permissions


def set_permissions_owners(permission_keys: List[str], owner_keys: List[str]) -> bool:
    if not owner_keys:
        return True
    owners = user_facade.get_users(keys=owner_keys)
    if not owners:
        return False
    return item_facade.set_permissions_owners(
        user_keys=[owner.key for owner in owners], permission_keys=permission_keys)


def get_permission_owners(permission_keys: List[str]) -> Dict[str, List[str]]:
    if not permission_keys:
        return {}
    return item_facade.get_items_have_in_items(attach_keys=permission_keys, attach_item_type=ItemType.permission,
                                               main_item_type=ItemType.user)


def delete_permissions_owners(permission_keys: List[str], owner_keys: List[str]) -> bool:
    return item_facade.delete_roles_or_users_owned_permissions(
        permission_keys=permission_keys, user_keys=owner_keys)


def clear_permission_owners(permission_keys: List[str]) -> bool:
    permissionkey2ownerkey = item_facade.get_items_have_in_items(
        attach_keys=permission_keys, attach_item_type=ItemType.permission, main_item_type=ItemType.user)
    for key, value in dict(permissionkey2ownerkey).items():
        item_facade.delete_roles_or_users_owned_permissions(permission_keys=[key], user_keys=value)
    return True


def update_permissions_owners(permission_keys: List[str], owner_keys: List[str]) -> bool:
    tets = clear_permission_owners(permission_keys)
    return  set_permissions_owners(permission_keys, owner_keys)


def grant_permissions_to_items(permission_keys: List[str], item_keys: List[str], item_type: ItemType) -> bool:
    return item_facade.attach_in_items_to_mains(
        main_keys=permission_keys, attach_keys=item_keys, main_type=ItemType.permission, attach_type=item_type)


def delete_permissions_items_had(permission_keys: List[str], item_keys: List[str], item_type: ItemType) -> bool:
    return item_facade.disable_old_refs(
        main_keys=permission_keys, attach_keys=item_keys, main_type=ItemType.permission, attach_type=item_type)


def judge_permissions_items_owned(permission_keys: List[str], item_keys: List[str], item_type: ItemType)\
        -> Dict[str, List[str]]:
    return item_facade.judge_have_ref(
        main_keys=item_keys, main_type=item_type, attach_keys=permission_keys, attach_type=ItemType.permission)