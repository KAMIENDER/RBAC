import os
import sys
from unittest import TestCase


sys.path.append(os.getcwd() + '/../../../')
from infrastructure.config.database_config import db_session
from domains.item.entity.const import ItemType
from domains.item.service.item_facade import create_user, create_role, add_users_to_roles, get_roles_member_keys, \
    delete_roles_members
import domains.item.service.item_facade as facade
from domains.item.repository.item_controller import get_item_controller

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/rbac')
session = sessionmaker()


class TestItemController(TestCase):
    def setUp(self):
        self.connection = engine.connect()
        self.trans = self.connection.begin()
        self.session = session(bind=self.connection)
        self.session.begin_nested()
        self.create_data()

    def create_data(self):
        self.user_keys = ['user1', 'user2']
        self.role_keys = ['role1', 'role2']
        self.users = dict()
        self.roles = dict()
        for key in self.user_keys:
            item = create_user(key=key)
            self.users[key] = item
        for key in self.role_keys:
            item = create_role(key=key)
            self.roles[key] = item

    def tearDown(self):
        item_controller = get_item_controller(session=db_session)
        item_controller.delete_items(self.role_keys+self.user_keys)
        self.session.close()
        self.trans.rollback()
        self.connection.close()

    def test_item_controller(self):
        item_controller = get_item_controller(session=self.session)
        new_item_main = item_controller.create_item(key='tmain', item_type=ItemType.role)
        new_item_attach = item_controller.create_item(key='tattach', item_type=ItemType.user)
        item_mains = item_controller.get_items(keys=['tmain'], item_type=ItemType.role)
        item_attaches = item_controller.get_items(keys=['tattach'], item_type=ItemType.user)
        assert item_mains == [new_item_main]
        assert item_attaches == [new_item_attach]
        new_item_ref = item_controller.build_item_refs(main_item=new_item_main, attach_items=item_attaches)
        item_refs = item_controller.get_item_refs(main_items=[new_item_main])
        assert item_refs == new_item_ref
        return

    def test_item_facade_create(self):
        item_controller = get_item_controller(session=db_session)
        users = item_controller.get_items(item_type=ItemType.user, keys=['user1', 'user2'])
        roles = item_controller.get_items(item_type=ItemType.role, keys=['role1', 'role2'])
        assert users == list(self.users.values())
        assert roles == list(self.roles.values())

        result = add_users_to_roles(role_keys=[role.key for role in roles], user_keys=[user.key for user in users])
        assert result is True
        role_members = get_roles_member_keys(role_keys=self.role_keys)
        assert role_members == {self.role_keys[0]: self.user_keys, self.role_keys[1]: self.user_keys}
        users_roles = facade.get_users_roles(user_keys=self.user_keys)
        assert users_roles == {self.user_keys[0]: self.role_keys, self.user_keys[1]: self.role_keys}
        result = delete_roles_members(role_keys=self.role_keys, user_keys=self.user_keys)
        assert result is True

        result = facade.set_owners_of_roles(user_keys=self.user_keys, role_keys=self.role_keys)
        assert result is True
        role_owners = facade.get_roles_owners(self.role_keys)
        assert role_owners == {self.role_keys[0]: self.user_keys, self.role_keys[1]: self.user_keys}
        roles_users_owned = facade.get_roles_users_owned(user_keys=self.user_keys)
        assert roles_users_owned == {self.user_keys[0]: self.role_keys, self.user_keys[1]: self.role_keys}
        result = facade.delete_roles_owners(role_keys=self.role_keys, user_keys=self.user_keys)
        assert result is True
        return
