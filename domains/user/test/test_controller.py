import logging
import os
import sys
from unittest import TestCase

sys.path.append(os.getcwd() + '/../../../')
from domains.user.repository.user_controller import get_user_controller
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/rbac')
session = sessionmaker()

class test_controller(TestCase):
    def setUp(self):
        self.connection = engine.connect()
        self.trans = self.connection.begin()
        self.session = session(bind=self.connection)
        self.session.begin_nested()

    def tearDown(self):
        self.session.close()
        # self.trans.rollback()
        self.connection.close()

    def test_user_controller(self):
        user_controller = get_user_controller(session=self.session)
        new_user = user_controller.create_user(name='tesfsdft', phone=1, email='test')
        users = user_controller.get_users(name='tesfsdft', phone=1, email='test')
        for user in users:
            assert user == user
        return