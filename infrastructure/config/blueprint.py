from flask import Flask
from flask_restful import Api

from application.service.permission import PermissionBasicResource, PermissionAuthResource, PermissionUpdateResource
from application.service.role import RoleResource, RoleUpdateResource, RoleOwnerResource, RoleMemberResource
from application.service.user import UserResource, UserUpdateResource


def register(app):
    register_user(app, pre_url='/user/')
    register_permission(app, pre_url='/permission/')
    register_role(app, pre_url='/role/')


def register_user(app: Flask, pre_url: str = "/"):
    api = Api(app)
    api.add_resource(UserResource, pre_url+'resource/')
    api.add_resource(UserUpdateResource, pre_url+'update_user/')


def register_permission(app: Flask, pre_url: str = '/'):
    api = Api(app)
    api.add_resource(PermissionBasicResource, pre_url + 'resource/')
    api.add_resource(PermissionAuthResource, pre_url + 'auth/')
    api.add_resource(PermissionUpdateResource, pre_url + 'update/')


def register_role(app: Flask, pre_url: str = "/"):
    api = Api(app)
    api.add_resource(RoleResource, pre_url+'resource/')
    api.add_resource(RoleUpdateResource, pre_url+'update_role/')
    api.add_resource(RoleOwnerResource, pre_url+'owner/')
    api.add_resource(RoleMemberResource, pre_url+'member/')