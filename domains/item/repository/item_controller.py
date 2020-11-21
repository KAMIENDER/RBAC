import logging
from typing import List

from sqlalchemy.orm import Session

from domains.item.entity.const import ItemType, ItemDisable, ItemRefDisable
from domains.item.models.item import Item
from domains.item.models.item_ref import ItemRef
from infrastructure.config.database_config import db_session


class ItemController(object):
    def __init__(self, session: Session, search_extra = None, search_ref_extra = None):
        self.session = session
        if search_extra:
            self.search_extra = search_extra
        self.search_ref_extra = self.search_extra
        if search_ref_extra:
            self.search_ref_extra = search_ref_extra

    def search_extra(self, extra: str, entities: List) -> List:
        # 后续需要传入，如果需要使用extra进行搜索的话
        return entities

    def create_item(self, key: str, item_type: ItemType, disable: ItemDisable = ItemDisable.able, extra: str = None) -> Item:
        item = Item(key=key,type=item_type.value, disable=disable.value)
        if extra:
            item.extra = extra
        try:
            self.session.add(item)
            self.session.commit()
        except Exception as e:
            logging.error(f"create item fail: {e}")
            return None
        return item

    def delete_items(self, keys: List[str]) -> bool:
        try:
            items = self.session.query(Item).filter(Item.key.in_(keys)).all()
            [self.session.delete(item) for item in items]
            self.session.commit()
        except Exception as e:
            logging.error(f"delete items error: {e}, keys: {keys}")
            return False
        return True

    def get_items(self, item_type: ItemType, keys: List[str] = None, ids: int = None,
                  disable: ItemDisable = ItemDisable.able, extra: str = None, offset: int = None, limit: int = None)\
            -> List[Item]:
        query = self.session.query(Item).filter(Item.type == item_type.value, Item.disable == disable.value)
        if keys:
            query = query.filter(Item.key.in_(keys))
        if ids:
            query = query.filter(Item.id.in_(ids))
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        try:
            items = query.all()
            if extra:
                items = self.search_extra(extra, items)
        except Exception as e:
            logging.error(f"get items fail: {e}")
            return list()
        return items

    def disable_items(self, items: List[Item]) -> bool:
        for item in items:
            item.disable = ItemDisable.disable.value
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"diable item fail: {e}")
            return False
        return True

    def enable_items(self, items: List[Item]) -> bool:
        for item in items:
            item.disable = ItemDisable.able.value
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"enable item fail: {e}")
            return False
        return True

    def update_item(self, extra: str, item: Item) -> bool:
        item.extra = extra
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"update item fail: {e}")
            return False
        return True

    def update_item_ref(self, extra: str, item_ref: ItemRef) -> bool:
        item_ref.extra = extra
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"update item fail: {e}")
            return False
        return True

    def build_item_refs(self, main_item: Item, attach_items: List[Item], extra: str = None) -> List[ItemRef]:
        try:
            new_item_refs = list()
            for attach_item in attach_items:
                new_item_ref = ItemRef(main_id=main_item.id, attach_id=attach_item.id, disable=ItemRefDisable.able.value)
                if extra:
                    new_item_ref.extra = extra
                new_item_refs.append(new_item_ref)
                self.session.add(new_item_ref)
            self.session.commit()
        except Exception as e:
            logging.error(f"build item refs fail: {e}")
            return list()
        return new_item_refs

    def enable_item_refs(self, item_refs: List[ItemRef]) -> bool:
        for item_ref in item_refs:
            item_ref.disable = ItemRefDisable.able.value
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"enable item ref fail: {e}")
            return False
        return True

    def disable_item_refs(self, item_refs: List[ItemRef]) -> bool:
        for item_ref in item_refs:
            item_ref.disable = ItemRefDisable.disable.value
        try:
            self.session.commit()
        except Exception as e:
            logging.error(f"diable ref item fail: {e}")
            return False
        return True

    def get_item_refs(self, main_items: List[Item] = [], attach_items: List[Item] = [],
                      disable: ItemRefDisable = ItemRefDisable.able, extra: str = None,
                      offset: int = None, limit: int = None) -> List[ItemRef]:
        query = self.session.query(ItemRef).filter(ItemRef.disable == disable.value)
        if main_items:
            main_item_ids = [item.id for item in main_items]
            query = query.filter(ItemRef.main_id.in_(main_item_ids))
        if attach_items:
            attach_item_ids = [item.id for item in attach_items]
            query = query.filter(ItemRef.attach_id.in_(attach_item_ids))
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        try:
            item_refs = query.all()
            if extra:
                item_refs = self.search_ref_extra(extra, item_refs)
        except Exception as e:
            logging.error(f"get item refs fail: {e}")
            return list()
        return item_refs


def get_item_controller(session: Session = db_session, search_extra = None, search_ref_extra = None):
    return ItemController(session=session, search_extra=search_extra, search_ref_extra=search_ref_extra)

