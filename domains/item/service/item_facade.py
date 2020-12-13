from collections import defaultdict
from typing import List, Dict

from domains.item.entity.const import ItemType, ItemDisable, ItemRefDisable
from domains.item.models.item import Item
from domains.item.models.item_ref import ItemRef
from domains.item.repository.item_controller import get_item_controller

item_controller = get_item_controller()


def create_user(key: str, extra: str = None) -> Item:
    item = item_controller.create_item(key=key, item_type=ItemType.user, extra=extra)
    return item


def create_role(key: str, extra: str = None) -> Item:
    item = item_controller.create_item(key=key, item_type=ItemType.role, extra=extra)
    return item


def create_permission(key: str, extra: str = None) -> Item:
    item = item_controller.create_item(key=key, item_type=ItemType.permission, extra=extra)
    return item


def get_roles_member_keys(role_keys: List[str]) -> Dict[str, List[str]]:
    role_items = item_controller.get_items(item_type=ItemType.role, keys=role_keys)
    role_user_refs = item_controller.get_item_refs(main_items=role_items, disable=ItemRefDisable.able)
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


def add_users_to_roles(user_keys: List[str], role_keys: List[str], extra: str = None) -> bool:
    if not delete_roles_members(user_keys=user_keys, role_keys=role_keys):
        return False
    role_items = item_controller.get_items(item_type=ItemType.role, keys=role_keys)
    user_items = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    for role_item in role_items:
        refs = item_controller.build_item_refs(main_item=role_item, attach_items=user_items, extra=extra)
        if len(refs) != len(user_items):
            return False
    return True


def delete_roles_members(user_keys: List[str], role_keys: List[str], extra: str = None) -> bool:
    role_items = item_controller.get_items(item_type=ItemType.role, keys=role_keys)
    if len(role_items) != len(role_keys):
        return False
    user_items = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    if len(user_keys) != len(user_items):
        return False
    old_refs = item_controller.get_item_refs(main_items=role_items, attach_items=user_items, disable=ItemRefDisable.able)
    return item_controller.disable_item_refs(old_refs)


def get_users_roles(user_keys: List[str]) -> Dict[str, List[str]]:
    users = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    refs = item_controller.get_item_refs(attach_items=users, disable=ItemRefDisable.able)
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
    refs = item_controller.get_item_refs(attach_items=roles, disable=ItemDisable.able)
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
    if not role_items:
        return False
    user_items = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    if not user_items:
        return False
    old_refs = item_controller.get_item_refs(main_items=user_items, attach_items=role_items, disable=ItemRefDisable.able)
    return item_controller.disable_item_refs(old_refs)


def get_roles_users_owned(user_keys: List[str]) -> Dict[str, List[str]]:
    users = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    refs = item_controller.get_item_refs(main_items=users, disable=ItemRefDisable.able)
    attach_ids = [ref.attach_id for ref in refs]
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


def delete_roles_or_users_owned_permissions(permission_keys: List[str],
                                           role_keys: List[str] = [], user_keys: List[str] = []) -> bool:
    if not role_keys and not user_keys:
        return True

    permissions = item_controller.get_items(item_type=ItemType.permission, keys=permission_keys)
    roles = item_controller.get_items(item_type=ItemType.role, keys=role_keys)
    users = item_controller.get_items(item_type=ItemType.user, keys=user_keys)
    if not roles and not users:
        return True

    if not permissions:
        return True

    refs = item_controller.get_item_refs(main_items=roles + users, attach_items=permissions, disable=ItemRefDisable.able)
    return item_controller.disable_item_refs(refs)


def set_permissions_owner_to_roles_or_users(permission_keys: List[str],
                                        role_keys: List[str] = [], user_keys: List[str] = []) -> bool:
    if not delete_roles_or_users_owned_permissions(permission_keys=permission_keys, role_keys=role_keys,
                                                  user_keys=user_keys):
        return False
    permissions = item_controller.get_items(item_type=ItemType.permission, keys=permission_keys)
    roles = item_controller.get_items(item_type=ItemType.role, keys=role_keys)
    users = item_controller.get_items(item_type=ItemType.user, keys=user_keys)

    for item in roles + users:
        if not item_controller.build_item_refs(main_item=item, attach_items=permissions):
            return False
    return True


def get_permissions_of_items_owned(keys: List[str], item_type: ItemType) -> Dict[str, List[str]]:
    if not keys:
        return dict()

    items = item_controller.get_items(item_type=item_type, keys=keys)
    id_to_items = {item.id: item for item in items}
    refs = item_controller.get_item_refs(main_items=items, disable=ItemRefDisable.able)
    attach_ids = [ref.attach_id for ref in refs]
    permissions = item_controller.get_items(item_type=ItemType.permission, ids=attach_ids)
    id_to_permissions = {permission.id: permission for permission in permissions}
    permission_ids = list(id_to_permissions.keys())
    out = defaultdict(list)
    for ref in refs:
        if ref.attach_id not in permission_ids:
            continue
        out[id_to_items[ref.main_id].key].append(id_to_permissions[ref.attach_id].key)
    return out


def get_own_permissions_of_roles(role_keys: List[str]) -> Dict[str, List[str]]:
    if not role_keys:
        return dict()
    return get_permissions_of_items_owned(keys=role_keys, item_type=ItemType.role)


def get_own_permissions_of_users(user_keys: List[str]) -> Dict[str, List[str]]:
    return get_permissions_of_items_owned(keys=user_keys, item_type=ItemType.user)


def get_had_not_owned_permissions_of_users(user_keys: List[str]) -> Dict[str, List[str]]:
    return get_items_have_in_items(attach_keys=user_keys, attach_item_type=ItemType.user,
                                   main_item_type=ItemType.permission)


def get_items_have_in_items(attach_keys: List[str], attach_item_type: ItemType, main_item_type: ItemType) \
        -> Dict[str, List[str]]:
    if not attach_keys:
        return {}

    attaches = item_controller.get_items(item_type=attach_item_type, keys=attach_keys)
    id_to_attach = {attach.id: attach for attach in attaches}
    refs = item_controller.get_item_refs(attach_items=attaches, disable=ItemRefDisable.able)
    main_ids = [ref.main_id for ref in refs]
    mains = item_controller.get_items(item_type=main_item_type, ids=main_ids)
    id_to_main = {main.id: main for main in mains}
    attach_ids = list(id_to_attach.keys())

    out = defaultdict(list)
    for ref in refs:
        if ref.attach_id not in attach_ids:
            continue
        out[id_to_attach[ref.attach_id].key].append(id_to_main[ref.main_id].key)
    return out


def get_items_attached_to_in_items(main_keys: List[str], attach_item_type: ItemType, main_item_type: ItemType,
                                   disable: ItemDisable = ItemRefDisable.able) \
        -> Dict[str, List[str]]:
    if not main_keys:
        return {}

    mains = item_controller.get_items(item_type=main_item_type, keys=main_keys)
    id_to_main = {main.id: main for main in mains}
    refs = item_controller.get_item_refs(main_items=mains, disable=disable)
    attach_ids = [ref.attach_id for ref in refs]
    attaches = item_controller.get_items(item_type=attach_item_type, ids=attach_ids)
    id_to_attach = {attach.id: attach for attach in attaches}
    main_ids = list(id_to_main.keys())

    out = defaultdict(list)
    for ref in refs:
        if ref.main_id not in main_ids:
            continue
        out[id_to_main[ref.main_id].key].append(id_to_attach[ref.attach_id].key)
    return out


def get_roles_have_permissions(permission_keys: List[str]) -> Dict[str, List[str]]:
    return get_items_have_in_items(
        attach_keys=permission_keys, attach_item_type=ItemType.permission, main_item_type=ItemType.role)


def disable_old_refs(attach_keys: List[str], main_keys: List[str], attach_type: ItemType, main_type: ItemType) -> bool:
    if not attach_keys or not main_keys:
        return True
    attaches = item_controller.get_items(item_type=attach_type, keys=attach_keys)
    mains = item_controller.get_items(item_type=main_type, keys=main_keys)
    if not attaches or not mains:
        return True
    refs = item_controller.get_item_refs(attach_items=attaches, main_items=mains, disable=ItemRefDisable.able)
    return item_controller.disable_item_refs(refs)


def attach_in_items_to_mains(attach_keys: List[str], main_keys: List[str], attach_type: ItemType, main_type: ItemType,
                             extra=None) -> bool:
    if not attach_keys or not main_keys:
        return True
    if not disable_old_refs(
            attach_keys=attach_keys, main_keys=main_keys, attach_type=attach_type, main_type=main_type):
        return False
    attaches = item_controller.get_items(item_type=attach_type, keys=attach_keys)
    mains = item_controller.get_items(item_type=main_type, keys=main_keys)
    if not attaches or not mains:
        return True
    refs = list()
    for main in mains:
        t_refs = item_controller.build_item_refs(main_item=main, attach_items=attaches, extra=extra)
        if not t_refs:
            item_controller.disable_item_refs(refs)
            return False
        refs.extend(t_refs)
    return True


def set_permissions_owners(user_keys: List[str], permission_keys: List[str]) -> bool:

    return attach_in_items_to_mains(
        attach_keys=permission_keys, main_keys=user_keys, attach_type=ItemType.permission, main_type=ItemType.user)


def disable_items(keys: List[str], item_type: ItemType) -> bool:
    items = item_controller.get_items(keys=keys, item_type=item_type)
    if not items:
        return True
    return item_controller.disable_items(items)


def disable_permissions(keys: List[str]) -> bool:
    return disable_items(keys=keys, item_type=ItemType.permission)


def get_refs_by_attach_keys_and_main_keys(
        main_keys: List[str], main_type: ItemType, attach_keys: List[str], attach_type: ItemType, disable: ItemDisable) \
        -> Dict[str, List[str]]:
    main_items = item_controller.get_items(item_type=main_type, keys=main_keys)
    main_id2main = {main.id: main for main in main_items}
    attach_items = item_controller.get_items(item_type=attach_type, keys=attach_keys)
    attach_id2attach = {attach.id: attach for attach in attach_items}
    refs = item_controller.get_item_refs(main_items=main_items, attach_items=attach_items, disable=disable)
    out = defaultdict(list)
    for ref in refs:
        out[main_id2main[ref.main_id].key].append(attach_id2attach[ref.attach_id].key)
    return out


def judge_have_ref(main_keys: List[str], attach_keys: List[str], main_type: ItemType, attach_type: ItemType) -> Dict[str, List[str]]:
    main_items = item_controller.get_items(item_type=main_type, keys=main_keys)
    mainid2key = {item.id: item.key for item in main_items}
    attach_items = item_controller.get_items(item_type=attach_type, keys=attach_keys)
    attachid2key = {item.id: item.key for item in attach_items}
    refs = item_controller.get_item_refs(main_items=main_items, attach_items=attach_items, disable=ItemRefDisable.able)
    out = defaultdict(list)
    for ref in refs:
        out[mainid2key[ref.main_id]].append(attachid2key[ref.attach_id])
    return out


