import os
import sys
from unittest import TestCase

sys.path.append(os.getcwd() + '/../../../')
from domains.user.repository.user_controller import get_user_controller
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

    def test_user_controller(self):
        user_controller = get_user_controller(session=self.session)
        new_user = user_controller.create_user(name='tesfsdft', phone=1, email='test', key='test', password='test')
        users = user_controller.get_users(name='tesfsdft', phones=[1], email='test')
        for user in users:
            assert new_user == user
        result = user_controller.update_user(new_user, name='fdsfsfdsfsfsdf')
        assert result is True
        users = user_controller.get_users(name='fdsfsfdsfsfsdf', phones=[1], email='test', limit=1)
        for user in users:
            assert new_user == user
        return
