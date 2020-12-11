import os
import sys
from unittest import TestCase

sys.path.append(os.getcwd() + '/../../../')
from domains.role.respository.role_controller import get_role_controller
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/rbac')
session = sessionmaker()


class TestUserController(TestCase):
    def setUp(self):
        self.connection = engine.connect()
        self.trans = self.connection.begin()
        self.session = session(bind=self.connection)
        self.session.begin_nested()

    def tearDown(self):
        self.session.close()
        self.trans.rollback()
        self.connection.close()

    def test_role_controller(self):
        role_controller = get_role_controller(session=self.session)
        new_role = role_controller.create_role(name='tesfsdft',key='test')
        roles = role_controller.get_roles(name='tesfsdft')
        for role in roles:
            assert new_role == role
        result = role_controller.update_role(new_role, name='fdsfsfdsfsfsdf')
        assert result is True
        roles = role_controller.get_roles(name='fdsfsfdsfsfsdf', limit=1)
        for role in roles:
            assert new_role == role
        return
