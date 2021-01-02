from typing import List

import domains.item.service.item_facade as item_facade
from domains.attr.entity.const import AttrDisable
from domains.item.entity.const import ItemDisable
from domains.item.models.item import Item


def create_attr(key: str) -> bool:
    if item_facade.create_attribute(key):
        return True
    return False


def get_attrs_by_key(keys: List[str], disable: AttrDisable = AttrDisable.able) -> List[Item]:
    return item_facade.get_attributes_by_keys(keys, ItemDisable(disable.value))

