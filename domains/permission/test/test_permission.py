import os
import sys
from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.append(os.getcwd() + '/../../../')

import domains.permission.repository.permission_contoller as pc

engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/rbac')
session = sessionmaker()


class TestPermission(TestCase):
    def setUp(self):
        self.connection = engine.connect()
        self.trans = self.connection.begin()
        self.session = session(bind=self.connection)
        self.session.begin_nested()

    def tearDown(self):
        self.session.close()
        self.trans.rollback()
        self.connection.close()

    def test_permission_controller(self):
        permission_controller = pc.get_permission_controller(session=self.session)
        permissions_ori0 = permission_controller.create_permission(key='p0', name='p0')
        permissions_ori1 = permission_controller.create_permission(key='p1', name='p1')
        permissions = permission_controller.get_permissions(keys=['p0', 'p1'])
        assert permissions == [permissions_ori0, permissions_ori1]
        permissions = permission_controller.get_permissions(name='p')
        assert permissions == [permissions_ori0, permissions_ori1]
        result = permission_controller.disable_permission(permission=permissions_ori0)
        assert result is True
        permission0 = permission_controller.get_permissions(keys=['p0'])
        assert permission0 == []
        result = permission_controller.enable_permission(permission=permissions_ori0)
        assert result is True
        permission0 = permission_controller.get_permissions(keys=['p0'])
        assert permission0[0].disable == 0
        result = permission_controller.update_permission(permission0[0], name='pp0')
        assert result is True
        permission0 = permission_controller.get_permissions(keys=['p0'])
        assert permission0[0].name == 'pp0'
        return
