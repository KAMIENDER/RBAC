from enum import Enum


class ItemType(Enum):
    user = 0
    permission = 1
    role = 2
    resource = 3
    attribute = 4


class ItemDisable(Enum):
    disable = 1
    able = 0


class ItemRefDisable(Enum):
    disable = 1
    able = 0
