from collections import defaultdict
from typing import List, Dict

from domains.item.entity.const import ItemType
from domains.item.models.item import Item
from domains.item.repository.item_controller import get_item_controller

item_controller = get_item_controller()


def create_user(key: str, extra: str = None) -> Item:
    item = item_controller.create_item(key=key, item_type=ItemType.user, extra=extra)
    return item


def create_role(key: str, extra: str = None) -> Item:
    item = item_controller.create_item(key=key, item_type=ItemType.role, extra=extra)
    return item


def get_roles_member_keys(role_keys: List[str]) -> Dict[str, List[str]]:
    role_items = item_controller.get_items(item_type=ItemType.role, keys=role_keys)
    role_user_refs = item_controller.get_item_refs(main_items=role_items)
    role_id_to_role_item = {item.id: item for item in role_items}
    out = defaultdict(list)
    user_item_ids = [ref.attach_id for ref in role_user_refs]
    user_items = item_controller.get_items(item_type=ItemType.user, ids=user_item_ids)
    user_id_to_item = {item.id: item for item in user_items}
    user_ids = list(user_id_to_item.keys())
    for ref in role_user_refs:
        if ref.attach_id not in user_ids:
            continue
        out[role_id_to_role_item[ref.main_id].key].append(user_id_to_item[ref.attach_id].key)
    return out


def add_users_to_roles(user_keys: List[str], role_keys: List[str], extra: str=None) -> bool:
    if not delete_roles_members(user_keys=user_keys, role_keys=role_keys):
        return False
    role_items = item_controller.get_items(item_type=ItemType.role, keys=role_keys)
    user_items = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    for role_item in role_items:
        refs = item_controller.build_item_refs(main_item=role_item, attach_items=user_items, extra=extra)
        if len(refs) != len(user_items):
            return False
    return True


def delete_roles_members(user_keys: List[str], role_keys: List[str], extra: str=None) -> bool:
    role_items = item_controller.get_items(item_type=ItemType.role, keys=role_keys)
    if len(role_items) != len(role_keys):
        return False
    user_items = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    if len(user_keys) != len(user_items):
        return False
    old_refs = item_controller.get_item_refs(main_items=role_items, attach_items=user_items)
    return item_controller.disable_item_refs(old_refs)


def get_users_roles(user_keys: List[str]) -> Dict[str, List[str]]:
    users = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    refs = item_controller.get_item_refs(attach_items=users)
    role_ids = [ref.main_id for ref in refs]
    out = defaultdict(list)
    roles = item_controller.get_items(item_type=ItemType.role, ids=role_ids)
    id_to_role = {role.id: role for role in roles}
    role_ids = list(id_to_role.keys())
    id_to_user = {user.id: user for user in users}
    for ref in refs:
        if ref.main_id not in role_ids:
            continue
        out[id_to_user[ref.attach_id].key].append(id_to_role[ref.main_id].key)
    return out


def set_owners_of_roles(user_keys: List[str], role_keys: List[str]) -> bool:
    delete_roles_owners(user_keys=user_keys, role_keys=role_keys)
    users = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    if len(user_keys) != len(users):
        return False
    roles = item_controller.get_items(item_type=ItemType.role, keys=role_keys)
    if len(role_keys) != len(roles):
        return False
    for user in users:
        item_controller.build_item_refs(main_item=user, attach_items=roles)
    return True


def get_roles_owners(role_keys: List[str]) -> Dict[str, List[str]]:
    roles = item_controller.get_items(item_type=ItemType.role, keys=role_keys)
    if len(role_keys) != len(roles):
        return False
    id_to_role = {role.id: role for role in roles}
    refs = item_controller.get_item_refs(attach_items=roles)
    user_ids = [ref.main_id for ref in refs]
    users = item_controller.get_items(item_type=ItemType.user, ids=user_ids)
    id_to_user = {user.id: user for user in users}
    user_ids = list(id_to_user.keys())
    out = defaultdict(list)
    for ref in refs:
        if ref.main_id not in user_ids:
            continue
        out[id_to_role[ref.attach_id].key].append(id_to_user[ref.main_id].key)
    return out


def delete_roles_owners(role_keys: List[str], user_keys: List[str]) -> bool:
    role_items = item_controller.get_items(item_type=ItemType.role, keys=role_keys)
    if len(role_items) != len(role_keys):
        return False
    user_items = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    if len(user_keys) != len(user_items):
        return False
    old_refs = item_controller.get_item_refs(main_items=user_items, attach_items=role_items)
    return item_controller.disable_item_refs(old_refs)


def get_roles_users_owned(user_keys: List[str]) -> Dict[str, List[str]]:
    users = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    refs = item_controller.get_item_refs(main_items=users)
    attach_ids = [ref .attach_id for ref in refs]
    roles = item_controller.get_items(item_type=ItemType.role, ids=attach_ids)
    id_to_user = {user.id: user for user in users}
    id_to_role = {role.id: role for role in roles}
    role_ids = list(id_to_role.keys())
    out = defaultdict(list)
    for ref in refs:
        if ref.attach_id not in role_ids:
            continue
        out[id_to_user[ref.main_id].key].append(id_to_role[ref.attach_id].key)
    return out
