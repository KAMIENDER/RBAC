import logging
from typing import List

import domains.item.service.item_facade as item_facade
from domains.attr.entity.const import AttrDisable
from domains.item.entity.const import ItemDisable, ItemType
from domains.item.models.item import Item
from domains.lex.service_supplier import SyntaxAnalyzeServiceSupplier


def create_attr(key: str) -> bool:
    if item_facade.create_attribute(key):
        return True
    return False


def get_attrs_by_key(like_key: str = None, keys: List[str] = None, disable: AttrDisable = AttrDisable.able)\
        -> List[Item]:
    return item_facade.get_attributes_by_keys(like_key=like_key, keys=keys, disable=ItemDisable(disable.value))


def get_items_by_attr(expression: str, item_type: ItemType, disable: ItemDisable.able = None) -> List[Item]:
    try:
        service = SyntaxAnalyzeServiceSupplier(expression)
        service.convert_to_sql()
    except Exception as e:
        logging.error(f"[get_item_by_expression]analyze expression err: {e}")
        return list()
    return item_facade.get_items_by_statement(service.tree, item_type, disable)


def set_attrs_to_items(item_keys: List[str], item_type: ItemType, attr_keys: List[str], value) -> bool:
    return item_facade.attach_in_items_to_mains(
        main_keys=item_keys, main_type=item_type, attach_keys=attr_keys, attach_type=ItemType.attribute, extra=value)


def disable_attrs_to_items(item_keys: List[str], item_type: ItemType, attr_keys: List[str], value) -> bool:
    return item_facade.disable_old_refs(
        main_keys=item_keys, main_type=item_type, attach_keys=attr_keys, attach_type=ItemType.attribute)