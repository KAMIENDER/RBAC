from enum import Enum

from domains.role.entity.value import RoleMemberUserKey, RoleMemberRoleKey


class ItemType(Enum):
    user = 0
    permission = 1
    role = 2
    resource = 3
    attribute = 4

    @classmethod
    def item_type2tree_key(cls, item_type) -> str:
        if item_type == cls.role:
            return RoleMemberRoleKey
        if item_type == cls.user:
            return RoleMemberUserKey
        raise Exception("[ItemType] item_type2tree_key: invalid item type to tree key")
        return ""


class ItemDisable(Enum):
    disable = 1
    able = 0


class ItemRefDisable(Enum):
    disable = 1
    able = 0
