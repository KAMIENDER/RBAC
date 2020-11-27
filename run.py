import sys
import os
import flask

from domains.item.entity.const import ItemType
from domains.item.repository.item_controller import get_item_controller

if __name__ == '__main__':
    item_controller = get_item_controller()
    new_item_main = item_controller.create_item(key='runm', item_type=ItemType.role)
    new_item_attach = item_controller.create_item(key='runa', item_type=ItemType.user)
    item_mains = item_controller.get_items(key='runm', item_type=ItemType.role)
    item_attachs = item_controller.get_items(key='runa', item_type=ItemType.user)
    new_item_ref = item_controller.build_item_refs(main_item=new_item_main, attach_items=item_attachs)
    item_refs = item_controller.get_item_refs(main_items=[new_item_main])
    print('fdsf')