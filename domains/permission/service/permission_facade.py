from typing import List

from domains.permission.repository.permission_contoller import get_permission_controller
import domains.item.service.item_facade as item_facade

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

